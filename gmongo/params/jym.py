# 项目：   交易码表
# 模块：   交易码参数
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-8-30 18:00

from . import loadcheck, insert, ROOT, execute, fetch, fetchvalue, transaction, load_file, HOME, get_param_ver
from orange import Path, R, extract, arg, tprint
from orange.utils.sqlite import executemany, fetchone
from orange.xlsx import Header
Version = '0.1'


def show_version():
    print(f'交易码查询程序 Ver {Version}')
    print(f'当前交易码参数版本：{get_param_ver("jym")[0]}\n')


QUERYJYM = (
    'select a.jymc,a.jym,a.jyz,b.name,a.yxj,a.wdsqjb,zssqjb,wdsq,zssqjg,zssq,jnjb,xzbz,wb,'
    'dets,dzdk,sxf,htjc,szjd,bssx,sc,mz,cesq,fjjyz,shbs,cdjy,c.yjcd,c.ejcd '
    'from jym a '
    'left join jyz b on a.jyz=b.jyz '
    'left join jycd c on a.jym=c.jym')

SQBZ = {'1': '主办授权', '2': '主管授权'}
SQJG = {'0': '总中心', '1': '分中心'}
SFXY = {'0': '不需要', '1': '需要'}
SFYX = {'0': '不允许', '1': '允许'}
SFSM = {'0': '不扫描', '1': '扫描'}
WB = {'1': '不需要', '2': '需要'}
SM = {'0': '不扫描', '1': '实时扫描', '2': '补扫'}
XZBZ = {
    "CashIn": "现金收",
    "CashOut": "现金付",
    "TransIn": "转账收",
    "TransOut": "转账付",
    "SelfCashIn": "自助现金收",
    "SelfCashOut": "自助现金付",
    "SelfTransIn": "自助转账收",
    "SelfTransOut": "自助转账付",
}
Converter = {
    5: SQBZ,
    6: SQBZ,
    8: SQJG,
    11: XZBZ,
    12: WB,
    13: SFXY,
    14: SFSM,
    15: SFXY,
    16: SFXY,
    17: SM,
    19: SFXY,
    20: SFYX,
}


def convert_row(row: "iterable") -> list:
    '对一行为数据进行转换'
    row = list(row)
    for i, d in Converter.items():
        v = row[i]
        row[i] = f'{v}-{d.get(v)}'
    return row


HEASER = [
    Header('交易名称', 44),
    Header('交易码'),
    Header('交易组'),
    Header('交易组名称', 18.4),
    Header('优先级'),
    Header('网点授权级别', 18.4),
    Header('中心授权级别', 18.4),
    Header('必须网点授权'),
    Header('中心授权机构'),
    Header('必须中心授权'),
    Header('技能级别'),
    Header('现转标志', 22.8),
    Header('是否外包', 13.8),
    Header('大额提示', 13.8),
    Header('是否扫描电子底卡', 13.8),
    Header('是否收手续费', 13.8),
    Header('是否需要后台监测', 13.8),
    Header('事中扫描方式', 13.8),
    Header('补扫的限时时间'),
    Header('是否需要审查', 13.8),
    Header('是否允许抹账', 13.8),
    Header('是否允许超额授权'),
    Header('附加交易组'),
    Header('事后补扫'),
    Header('磁道校验'),
    Header('一级菜单', 16.33),
    Header('二级菜单', 30.67)
]


def export_jym():
    "导出交易码参数表"
    data = fetch(f"{QUERYJYM} order by a.jym")
    if data:
        period = get_param_ver('jym')[0]
        with (HOME / f'交易码清单{period}.xlsx').write_xlsx(force=True) as book:
            book.add_table("A1",
                           sheet="交易码一览表",
                           data=[convert_row(x) for x in data],
                           columns=HEASER)
            book.add_table("A1", sheet="交易码参数", data=data, columns=HEASER)
        print('导入交易码文件成功！')


def query_jy(query):
    "查询交易列表"
    sql = 'select jym,jymc,jyz,fjjyz from jym'
    if R / r'\d{4}' == query:
        query_jym(query)
        return
    elif R / r'[A-Z]{2}((\d{3})?[A-Z])?' / query:
        rows = fetch(f'{sql} where jyz like "{query}%" order by jym')
    else:
        rows = fetch(f'{sql} where jymc like "%{query}%" order by jym')
    if rows:
        tprint(rows, format_spec={
            0: "6",
            1: '50',
            2: '8',
        })


def query_gw(gw):
    "查询交易岗位信息"
    for r in fetch(f'select * from jygw where name like "%{gw}%" '):
        print(f"岗位代码：{r[1]}   岗位名称：{r[2]}")
        for row in fetch(
                'select b.jyz,b.name from jyzgw a '
                'left join jyz b on a.jyz=b.jyz where a.gw=?', [r[0]]):
            print(*row, sep='\t')


def query_jyz(jyz):
    "查询交易组"
    row = fetchone('select * from jyz where jyz=?', [jyz])
    if row:
        print(f'交易组  ：{row[0]}\n交易组名：{row[1]}\n')
        for r in fetch(
                'select b.code,b.name from jyzgw a '
                'left join jygw b on a.gw=b.id where a.jyz=?', [jyz]):
            print(*r, sep='\t')


def query_jym(jym):
    "查询单个交易码"
    row = fetchone(f'{QUERYJYM} where a.jym=?', [jym])
    if row:
        data = zip([x['header'] for x in HEASER], convert_row(row))
        tprint(data, format_spec={0: '20'})


def test_jym(jym):
    '检查交易码是否已被使用'
    row = fetchone(
        'select  jym,jymc,"生产参数" from jym where jym =? '
        'union select jym,jymc,"科技菜单" from jycd where jym =? ', [jym, jym])
    if row:
        print(f'交易码 {jym} 已在 {row[2]} 使用\n交易名称为：{row[1]}')
    else:
        print(f'交易码 {jym} 未被使用')


@arg('-e', '--export', action='store_true', help='导入参数文件')
@arg('-z', '--jyz', nargs='?', help='查询指定交易组')
@arg('-g', '--gw', nargs='?', help='查询指定岗位')
@arg('-t', '--test', nargs='?', dest='tjym', help='检查指定交易码是否被占用')
@arg('query', nargs='?', help='查询交易码列表')
def main(gw=None, jyz=None, query=None, tjym=None, export=False):
    show_version()
    if tjym:
        test_jym(tjym)
    if jyz:
        query_jyz(jyz)
    if gw:
        query_gw(gw)
    if export:
        export_jym()
    if query:
        query_jy(query)
