# 项目：   参数管理
# 模块：   机构码表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 14:01

from gmongo.params import loadcheck, insert, ROOT, execute, fetch, fetchvalue,\
    cachedfunc
from orange import Path, R, extract
from orange.utils.sqlite import fix_db_name


def loadfile():
    path = ROOT.find('ggjgm.del')

    @loadcheck
    def _(path: Path):
        execute('delete from ggjgm')
        insert(
            'ggjgm',
            path.iter_csv(encoding='gbk',
                          errors='ignore',
                          columns=(0, 1, 3, 7, 15, 16, 17)))
        print(f'{path.name} 导入成功')

    return _(path)


BranchPattern = R / '(总行|.{2}分行)'


@cachedfunc
def brname(jgm):
    name = fetchvalue('select mc from ggjgm where jgm=?', [jgm])
    return name and extract(name, BranchPattern)


@cachedfunc
def br(jgm):
    return brname(fetchvalue('select hzjgm from ggjgm where jgm=?', [jgm]))


def branches():
    import sqlite3
    db = fix_db_name('params')
    with sqlite3.connect(db) as conn:
        return {
            br: extract(name, BranchPattern, 1)
            for br, name in conn.execute('select a.jgm,b.mc from ggjgm a '
                                         'left join ggjgm b on a.hzjgm=b.jgm ')
        }
