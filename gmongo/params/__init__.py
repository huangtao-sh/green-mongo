# 项目：   工作平台
# 模块：   参数管理模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 11:36

from orange.utils.sqlite import executefile, fetch, db_config, loadcheck, insert, execute,\
    fetch,fetchone,fetchvalue,transaction
from orange import HOME
from functools import wraps

db_config('params')
executefile('gmongo', 'sql/params.sql')
ROOT = HOME / 'OneDrive/工作/参数备份'
