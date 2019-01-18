# 项目：   工作平台
# 模块：   履职报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-18 20:39

from orange.utils.sqlite import findone, findvalue, find, execute, executemany, trans
from orange import cstr, R


def fetch_period()-> str:
    d = findvalue('select period from report order by date desc limit 1')
    if not d:
        raise Exception('无数据记录')
    return d


def do_report():
    period = fetch_period()
    print('当前期次：%s' % (period))
    d = findone(
        'select count(br) as count from report where period=?', [period])
    if d:
        print(f'报告数量：{d[0]}')
    print('报送数据错误清单')
    print('-'*30)
    sql = ('select br,count(name) as count,group_concat(name)as names '
           'from report where period= ? '
           'group by br '
           'having count>1 order by br')
    for no, (jg, count, names) in enumerate(find(sql, [period]), 1):
        print(no, cstr(jg, 30), names, sep='\t')
    print(f'共计：{no}')
    print('\n未报送机构清单')
    print('-'*30)
    sql = ('select rowid,br,name from branch '
           'where br not in (select br from report where period=?) '
           'and name not in (select name from report where period=?)'
           'order by br')
    no = 0
    for no, (rowid, br, name) in enumerate(find(sql, [period, period]), 1):
        print(no, cstr("%03d-%s" % (rowid, br), 35), name, sep='\t')
    print(f'共计：{no}')


def delete_branchs(brs: list):
    period = fetch_period()
    branchs, ids = set(), set()
    Number = R / r'\d{1,4}'
    for br in brs:
        if Number == br:
            ids.add(br)
        else:
            branchs.add(br)
    brs = ",".join([f'"{x}"' for x in branchs])
    ids = ",".join(ids)
    sql = f'''select rowid,br from branch where (rowid in ({ids}) or br in ({brs}))
    and br not in (select br from report where period =?) order by br'''
    print('以下机构将被删除：')
    ids = []
    for row in find(sql, [period]):
        print(*row)
        ids.append([row[0]])
    with trans():
        executemany(f'delete from branch where rowid=?', ids)
