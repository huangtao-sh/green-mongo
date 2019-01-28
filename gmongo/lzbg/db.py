# 项目：   工作平台
# 模块：   履职报告，数据库操作模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-28 21:19

from gmongo import execute, executefile, fetch, executetrans


def init_db():
    executefile('gmongo', 'sql/lzbg.sql')
    print('初始化数据库成功！')


def drop_tables(*tables):
    for table in tables:
        try:
            execute(f'drop table {table}')
            print(f'{table} 已被删除!')
        except:
            print(f'{table} 不存在!')
