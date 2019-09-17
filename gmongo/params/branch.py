# 项目：   参数管理
# 模块：   机构码表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 14:01

from . import loadcheck, insert, ROOT, execute, fetch, fetchvalue, transaction, load_file
from orange import Path, R, extract, arg, tprint
from orange.utils.sqlite import connect
from functools import partial
from contextlib import closing


def loadfile():
    path = ROOT.find('ggjgm.del')
    return load_file(path,
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
    convert = lambda obj: (obj[0], extract(obj[1], BranchPattern, 1))
    with connect('params') as conn:
        return dict(map(convert, conn.fetch(sql)))


@arg('query', help='查询条件')
def main(query):
    if R / r'\d{2}' == query:
        data = fetch('select * from ggjgm where jglx=?', [query])
    elif R / r'316\d{1,9}' == query:
        data = fetch(f'select * from ggjgm where zfhh like "{query}%"')
    elif R / r'\d{3,9}' == query:
        data = fetch(f'select * from ggjgm where jgm like "{query}%"')
    else:
        data = fetch(f'select * from ggjgm where mc like "%{query}%"')
    tprint(data, format_spec={1: '40', 2: '10'})
