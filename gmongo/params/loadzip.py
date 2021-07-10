# 项目：   参数导入模块
# 模块：   导入压缩包中的参数
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-07-10 08:24

from .loader import Loader, loadcheck
from zipfile import ZipFile
from orange import Path, info, fatal, decode, Data, limit, datetime, includer, decode, mapper, filterer
from orange.utils.sqlite import tran
Root = Path('~/Documents/参数备份')


@mapper
def stripper(row: list) -> list:
    return [x.strip()for x in row]


@mapper
def null2none(row: list) -> list:
    return [None if x == 'null' else x for x in row]


''' 
copy(d[:3], s[:3])
	copy(d[3:7], s[4:8])
	d[7] = strings.Join(s[8:length-26], ",")
	d[8] = s[length-26]
	copy(d[9:12], s[length-24:length-21])
	copy(d[12:19], s[length-11:length-4])
	copy(d[19:], s[length-3:])
	if len(d[15]) == 8  {
		d[15] = fmt.Sprintf("%s-%s-%s", d[15][:4], d[15][4:6], d[15][6:])
	}
    if len(d[16]) == 8  {
		d[16] = fmt.Sprintf("%s-%s-%s", d[16][:4], d[16][4:6], d[16][6:])
	}

'''


def teller_converter(row: list) -> list:
    nrow = [""]*22
    nrow[:3] = row[:3]
    nrow[3:7] = row[4:8]
    nrow[8] = ",".join(row[8:-26])
    nrow[9:12] = row[-24:-21]
    nrow[12:19] = row[-11:-4]
    nrow[19:] = row[-3:]
    return nrow


teller_loader = Loader('teller', 22, stripper, converter=teller_converter)


# 机构码导入


@mapper
def jg_conv(row: list) -> list:
    row[5] = row[5][:10]
    return row


jgm_loader = Loader('ggjgm', 7,
                    includer(0, 1, 3-43, 7-43, 15-43, 16-43, 17-43), stripper, jg_conv)

# 交易码


@mapper
def jy_conv(row: list) -> list:
    row += [""]*2
    return row[:22]


jym_loader = Loader('jym', 22, stripper, jy_conv)

# 内部账户


@mapper
def nbzh_conv(row: list) -> list:
    for i in range(14, 18):
        if len(row[i]) > 10:
            row[i] = row[i][:10]
    return row


nbzh_loader = Loader('nbzh', 25, stripper, nbzh_conv)
# 内部账户模板


@mapper
def nbzhmb_conv(row: list) -> list:
    row[1] = row[1][:10]
    return row


@filterer
def cdjyfilter(row):
    return row[1] == '8'


zhmb_loader = Loader('nbzhmb', 10, stripper, nbzhmb_conv)
zzzz_loader = Loader('zzzz', 11, stripper)
dzzz_loader = Loader('dzzz', 17, stripper, null2none)
shbs_loader = Loader('shbs', 1, includer(0))
cdjy_loader = Loader('cdjy', 1, cdjyfilter, includer(0))
xxbm_loader = Loader('xxbm', 3, includer(0, 1, 2), stripper)
kmzd_loader = Loader('kmzd', 9, includer(2, 1, 3, 4, 5, 6, 7), stripper)

filelist = {
    'users_output': teller_loader,
    'YUNGUAN_MONTH_STG_ZSRUN_GGJGM': jgm_loader,
    'transactions_output': jym_loader,
    'YUNGUAN_MONTH_STG_ZSRUN_FHNBHZZ': nbzh_loader,
    'YUNGUAN_MONTH_STG_ZSRUN_GGNBZHMB': zhmb_loader,
    'YUNGUAN_MONTH_STG_TELLER_ZZZZCSB': zzzz_loader,
    'YUNGUAN_MONTH_STG_TELLER_DZZZCSB': dzzz_loader,
    'YUNGUAN_MONTH_STG_TELLER_SCANVOUCHER': shbs_loader,
    'YUNGUAN_MONTH_STG_TELLER_TRANSCONTROLS': cdjy_loader,
    'YUNGUAN_MONTH_STG_ZSRUN_GGXXBMDZB': xxbm_loader,
    'YUNGUAN_MONTH_STG_ZSRUN_GGKMZD': kmzd_loader,
}


def loadzip():
    path = Root.find('运营参数*.zip')
    if not path:
        print(f'没有找到 运营参数*.zip 文件')
        exit(1)

    info(f'找到文件 {path}')
    with ZipFile(path)as zf:
        files = {}
        ver = path.pname[-7:]
        for fileinfo in zf.filelist:
            if not (fileinfo.flag_bits & 0x0800):
                fileinfo.filename = fileinfo.filename.encode(
                    'cp437').decode('gbk')
                zf.NameToInfo[fileinfo.filename] = fileinfo
            files[Path(fileinfo.filename).pname] = fileinfo

        def read(fileinfo, name):
            with zf.open(fileinfo)as f:
                for row in f:
                    encoding = 'utf8' if name in (
                        'transactions_output', 'users_output') else 'gbk'
                    yield row.decode(encoding, errors='ignore').split(',')

        @tran
        def load(fname: str, loader: Loader):
            if fileinfo := files.get(fname):
                path = Path(fileinfo.filename)
                mtime = datetime(*fileinfo.date_time) % '%F %H:%M:%S'
                loadcheck(loader.table, path.name, mtime, ver)
                loader.data = read(fileinfo, fname)
                r = loader.load()
                if r:
                    print(f'导入文件 {fname} 成功，行数：{r.rowcount}')
                else:
                    raise Exception('执行SQL错误')
            else:
                Warning(f'没有在压缩包中找到：{name}')

        def test(name):
            if fileinfo := files.get(name):
                loader = filelist.get(name)
                loader.data = read(fileinfo, name)
                loader.test()
        #test('YUNGUAN_MONTH_STG_ZSRUN_GGXXBMDZB')
        #exit()
        for name, loader in filelist.items():
            try:
                load(name, loader)
            except Exception as e:
                print(e)
