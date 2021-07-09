# 项目：   工作平台
# 模块：   参数管理模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 11:36
# 修订：2020-06-15 19:22 和 grape 共享数据库

from orange.utils.sqlite import executefile, fetch, db_config, loadcheck, execute,\
    fetch, fetchone, fetchvalue, executescript
from orange import HOME, Path, now
from functools import wraps
from gmongo.util.branch import get_branches

db_config('~/.data/params.db')

ROOT = HOME / 'OneDrive/工作/参数备份'
ParamRoot = ROOT.find('运营管理*')
DefaultPeriod = str(ParamRoot)[-7:]


def show_version(category=None):
    from gmongo.__version__ import version
    print('gmongo', version)
    if category:
        print('数据版本', get_param_ver(category)[0])


def load_file(path: Path,
              table: str,
              fields: list = None,
              drop: bool = True,
              proc: callable = None,
              exec: callable = None,
              period: str = DefaultPeriod,
              method: str = 'insert',
              **kw):
    @loadcheck
    def _(path: Path):
        if drop:
            execute(f'delete from {table}')
        if callable(proc):
            data = proc(path, **kw)
        else:
            data = path.iter_csv(**kw)
        if period:
            execute('insert or replace into param_period values(?,?,?)',
                    [table, period, now() % '%F %T'])
        insert(table, fields=fields, data=data, method=method)
        if callable(exec):
            exec()
        print(f'{path.name} 导入成功')

    return _(path)


def get_param_ver(name):
    return fetchone('select period,time from param_period where name =?',
                    [name])


def get_ver(name):
    return fetchvalue("select ver from loadfile where name=?", [name])
