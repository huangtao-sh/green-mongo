# 项目：   交易码表
# 模块：   交易码参数
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-08-25 10:09

from . import loadcheck, insert, ROOT, execute, fetch, fetchvalue, transaction, load_file, HOME
from orange import Path, R, extract, arg, tprint
from orange.utils.sqlite import executemany, fetchone


def convert(row):
    row[0] = row[0].strip()
    row[3] = row[3].strip()
    if len(row) < 22:
        row.append(None)
    return row


def loadfile():
    def exec():
        print('更新磁道信息')
        cdjyfile = ROOT.find('是否校验磁道信息.*')
        executemany("update jym set cdjy='TRUE' where jym=?",
                    cdjyfile.iter_csv())
        print('更新事后补扫')
        shbsfile = ROOT.find('是否需要事后补扫.*')
        executemany("update jym set shbs='FALSE' where jym=?",
                    shbsfile.iter_csv())

    return load_file(
        ROOT.find('transactions_output.csv'),
        "jym",
        fields=
        "jym,jymc,jyz,yxj,wdsqjb,zssqjb,wdsq,zssqjg,zssq,jnjb,xzbz,wb,dets,dzdk,sxf,htjc,szjd,bssx,sc,mz,cesq,fjjyz"
        .split(","),
        encoding='gbk',
        errors='ignore',
        exec=exec,
        converter=convert)


def loadmenu():
    file = (HOME / 'OneDrive/工作/参数备份/交易菜单').find('menu*.xml')

    def procfile(file):
        for d in file:
            if d.tag == 'SubMenu':
                menu = d.attrib['DisplayName']
                for sd in d:
                    if sd.tag == 'Trade':
                        yield sd.attrib['Code'], sd.attrib[
                            'DisplayName'], menu, None
                    elif sd.tag == 'SubMenu':
                        submenu = sd.attrib['DisplayName']
                        for td in sd:
                            if td.tag == 'Trade':
                                yield td.attrib['Code'], td.attrib[
                                    'DisplayName'], menu, submenu

    return load_file(file, "jycd", proc=procfile, method='insert or replace')


def loadjyz():
    file = (HOME / 'OneDrive/工作/参数备份/岗位与交易组').find('岗位及组*.xls*')

    @loadcheck
    def _(file):
        data = file.sheets(0)
        jyz, gw, gx = [], [], []
        data = iter(data)
        jyz_name = next(data)
        jyz_code = next(data)
        jyz = [(code, name) for code, name in zip(jyz_code, jyz_name)
               if code and name]
        start = jyz_code.index(jyz[0][0])
        for i, row in enumerate(data):
            gw.append((i, row[start - 2], row[start - 1]))
            for h, k in enumerate(row[start:]):
                if k:
                    gx.append((i, jyz[h][0]))
        execute('delete from jyz;')
        execute('delete from jygw;')
        execute('delete from jyzgw;')
        insert('jyz', data=jyz)
        insert('jygw', data=gw)
        insert('jyzgw', data=gx)
        print('导入岗位及交易组参数成功')

    return _(file)


TRANSFER = {
    'wdsqjb': {
        '1': '1-主办授权',
        '2': '2-主管授权'
    },
    'zxsqjb': {
        '1': '1-主办授权',
        '2': '2-主管授权'
    },
    'zxsqjg': {
        '0': '0-总中心',
        '1': '1-分中心'
    },
    'dets': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'dzdk': {
        '0': '0-不扫描',
        '1': '1-扫描'
    },
    'sxf': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'htjc': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'sc': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'wb': {
        '2': '2-需要',
        '1': '1-不需要'
    },
    'mz': {
        '0': '0-不允许',
        '1': '1-允许'
    },
    'jdfs': {
        '0': '0-不扫描',
        '1': '1-实时扫描',
        '2': '2-补扫'
    },
    'xzbz': {
        "CashIn": "CashIn-现金收",
        "CashOut": "CashOut-现金付",
        "TransIn": "TransIn-转账收",
        "TransOut": "TransOut-转账付",
        "SelfCashIn": "SelfCashIn-自助现金收",
        "SelfCashOut": "SelfCashOut-自助现金付",
        "SelfTransIn": "SelfTransIn-自助转账收",
        "SelfTransOut": "SelfTransOut-自助转账付",
    }
}


def trans(tp, value):
    if tp in TRANSFER:
        return TRANSFER[tp].get(value)
    else:
        return value


QUERYJYM = (
    'select a.jymc,a.jym,a.jyz,b.name,a.yxj,a.wdsqjb,zssqjb,wdsq,zssqjg,zssq,jnjb,xzbz,wb,'
    'dets,dzdk,sxf,htjc,szjd,bssx,sc,mz,cesq,fjjyz,shbs,cdjy,c.yjcd,c.ejcd '
    'from jym a '
    'left join jyz b on a.jyz=b.jyz '
    'left join jycd c on a.jym=c.jym')


def convert_row(row):
    row = list(row)
    row[5] = trans('wdsqjb', row[5])
    row[6] = trans('zxsqjb', row[6])
    row[8] = trans('zxsqjg', row[8])
    row[11] = trans('xzbz', row[11])
    row[12] = trans('wb', row[12])
    row[13] = trans('dets', row[13])
    row[14] = trans('dzdk', row[14])
    row[15] = trans('sxf', row[15])
    row[16] = trans('htjc', row[16])
    row[17] = trans('jdfs', row[17])
    row[19] = trans('sc', row[19])
    row[20] = trans('mz', row[20])
    return row


HEASER = [
    {
        'header': '交易名称',
        'width': 44
    },
    {
        'header': '交易码'
    },
    {
        'header': '交易组'
    },
    {
        'header': '交易组名称',
        'width': 18.4
    },
    {
        'header': '优先级'
    },
    {
        'header': '网点授权级别',
        'width': 18.4
    },
    {
        'header': '中心授权级别',
        'width': 18.4
    },
    {
        'header': '必须网点授权'
    },
    {
        'header': '中心授权机构'
    },
    {
        'header': '必须中心授权'
    },
    {
        'header': '技能级别'
    },
    {
        'header': '现转标志',
        'width': 22.8
    },
    {
        'header': '是否外包',
        'width': 13.8
    },
    {
        'header': '大额提示',
        'width': 13.8
    },
    {
        'header': '是否扫描电子底卡',
        'width': 13.8
    },
    {
        'header': '是否收手续费',
        'width': 13.8
    },
    {
        'header': '是否需要后台监测',
        'width': 13.8
    },
    {
        'header': '事中扫描方式',
        'width': 13.8
    },
    {
        'header': '补扫的限时时间'
    },
    {
        'header': '是否需要审查',
        'width': 13.8
    },
    {
        'header': '是否允许抹账',
        'width': 13.8
    },
    {
        'header': '是否允许超额授权'
    },
    {
        'header': '附加交易组'
    },
    {
        'header': '事后补扫'
    },
    {
        'header': '磁道校验'
    },
    {
        'header': '一级菜单',
        'width': 16.33
    },
    {
        'header': '二级菜单',
        'width': 30.67
    },
]


def main(jym=None, gw=None, jyz=None, query=None, tjym=None, export=False):
    if jym:
        row = fetchone(f'{QUERYJYM} where a.jym=?', [jym])
        if row:
            data = zip([x['header'] for x in HEASER], convert_row(row))
            tprint(data, format_spec={0: '20'})
    if tjym:
        row = fetchone(
            'select  jym,jymc,"生产参数" from jym where jym =? '
            'union select jym,jymc,"科技菜单" from jycd where jym =? ',
            [tjym, tjym])
        if row:
            print(f'交易码 {tjym} 已在 {row[2]} 使用\n交易名称为：{row[1]}')
        else:
            print(f'交易码 {tjym} 未被使用')
    if jyz:
        row = fetchone('select * from jyz where jyz=?', [jyz])
        if row:
            print(f'交易组  ：{row[0]}\n交易组名：{row[1]}\n')
            for r in fetch(
                    'select b.code,b.name from jyzgw a '
                    'left join jygw b on a.gw=b.id where a.jyz=?', [jyz]):
                print(*r)
    if gw:
        for r in fetch(f'select * from jygw where name like "%{gw}%" '):
            print(f"岗位代码：{r[1]}   岗位名称：{r[2]}")
            for row in fetch(
                    'select b.jyz,b.name from jyzgw a '
                    'left join jyz b on a.jyz=b.jyz where a.gw=?', [r[0]]):
                print(*row)
    if export:
        data = fetch(f"{QUERYJYM} order by a.jym")
        if data:
            period = fetchvalue(
                'select period from param_period where name="jym" ')
            with (HOME / f'交易码清单{period}.xlsx').write_xlsx(force=True) as book:
                book.add_table("A1",
                               sheet="交易码一览表",
                               data=[convert_row(x) for x in data],
                               columns=HEASER)
                book.add_table("A1", sheet="交易码参数", data=data, columns=HEASER)
            print('导入交易码文件成功！')