# 项目：   工作平台
# 模块：   参数管理模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 11:36

from orange.utils.sqlite import executefile, fetch, db_config, loadcheck, insert, execute,\
    fetch, fetchone, fetchvalue, transaction
from orange import HOME, Path
from functools import wraps

db_config('params')
executefile('gmongo', 'sql/params.sql')
executefile('gmongo', 'sql/nbzh.sql')
ROOT = HOME / 'OneDrive/工作/参数备份'


def load_file(path: Path,
              table: str,
              drop: bool = True,
              proc: callable = None,
              **kw):
    @loadcheck
    def _(path: Path):
        if drop:
            execute(f'delete from {table}')
        if callable(proc):
            data = proc(path, **kw)
        else:
            data = path.iter_csv(**kw)
        insert(table, data)
        print(f'{path.name} 导入成功')

    return _(path)
