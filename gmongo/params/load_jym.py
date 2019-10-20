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
    row[9] = '%02d' % int(row[9])
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
        fields=("jym,jymc,jyz,yxj,wdsqjb,zssqjb,wdsq,zssqjg,zssq,jnjb,xzbz,wb,"
                "dets,dzdk,sxf,htjc,szjd,bssx,sc,mz,cesq,fjjyz").split(","),
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
