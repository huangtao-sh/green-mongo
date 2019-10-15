# 项目：   参数管理
# 模块：   机构码表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 14:01
# 修订：2019-09-17 21:06 调整调用方式

from orange import R, extract, arg, tprint
from orange.utils.sqlite import connect
from contextlib import closing


def loadfile():
    from . import load_file, ROOT
    return load_file(ROOT.find('ggjgm.del'),
                     'ggjgm',
                     drop=True,
                     encoding='gbk',
                     errors='ignore',
                     converter={1: str.strip},
                     columns=(0, 1, 3, 7, 15, 16, 17))


BranchPattern = R / '(总行|.{2}分行)'


def get_branches():
    '获取机构对应分行的名称'
    sql = 'select a.jgm,b.mc from ggjgm a left join ggjgm b on a.hzjgm=b.jgm'
    def convert(obj): return (obj[0], extract(obj[1], BranchPattern, 1))
    conn = connect('~/Onedrive/db/params.db')
    with closing(conn):
        branches = dict(map(convert, conn.fetch(sql)))
        branches['331000000'] = '总行业务处理中心'
        branches['331000808'] = '总行营业中心'
        return branches


@arg('query', help='查询条件')
def main(query):
    db = connect('params')
    with closing(db):
        if R / r'\d{2}' == query:
            data = db.fetch('select * from ggjgm where jglx=?', [query])
        elif R / r'316\d{1,9}' == query:
            data = db.fetch(f'select * from ggjgm where zfhh like "{query}%"')
        elif R / r'\d{3,9}' == query:
            data = db.fetch(f'select * from ggjgm where jgm like "{query}%"')
        else:
            data = db.fetch(f'select * from ggjgm where mc like "%{query}%"')
        tprint(data, format_spec={1: '40', 2: '10'})
