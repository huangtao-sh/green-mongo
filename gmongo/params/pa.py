# 项目：   参数程序
# 模块：   主程序
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-07-09 22:24

from orange import arg
from orange.utils.sqlite import db_config, fprintf, fprint, execute, connect


@arg('-s', '--show', metavar='name', nargs='?', help='显示数据库表的创建语句')
@arg('-L', '--list', action='store_true', help='显示数据库表')
@arg('-q', '--query', metavar='sql', dest='querysql', nargs='*', help='执行查询语句并显示结果')
@arg('-e', '--execute', metavar='sql', dest='esql', nargs='*', help='执行命令语句并显示执行结果')
@arg('-l', '--load', action='store_true', help='导入参数数据')
@arg('-r', '--reset', metavar='name', dest='reset_name', nargs='?', help='重置某表，重置后可以重新导入数据')
def main(**options):
    db_config('params')
    if options['list']:
        fprintf('{0:10s}{1:20s}',
                'select type,name from sqlite_master where type in ("table","view")order by name')
    if options['show']:
        fprint('select sql from sqlite_master where name=?', [options['show']])
    if options['querysql']:
        fprint(' '.join(options['querysql']))
    if options['esql']:
        with connect():
            r = execute(' '.join(options['querysql']))
            print(f'{r.rowcount} 行数据受到影响')
    if options['load']:
        print('导入数据')
    if options['reset_name']:
        with connect():
            r = execute('delete from LoadFile where name=?',
                        [options['reset_name']])
            if r.rowcount == 1:
                print(f"重置 {options['reset_name']} 成功")
            else:
                print(f"重置 {options['reset_name']} 失败")
