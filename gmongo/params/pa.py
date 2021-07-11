# 项目：   参数程序
# 模块：   主程序
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-07-09 22:24

from orange import arg, info, command
from orange.utils.sqlite import db_config, fprintf, fprint, execute, connect, executefile


@command(description='参数管理程序')
@arg('-s', '--show', metavar='name', nargs='?', help='显示数据库表的创建语句')
@arg('-L', '--list', action='store_true', help='显示数据库表')
@arg('-q', '--query', metavar='sql', dest='qsql', nargs='*', help='执行查询语句并显示结果')
@arg('-e', '--execute', metavar='sql', dest='esql', nargs='*', help='执行命令语句并显示执行结果')
@arg('-l', '--load', action='store_true', help='导入参数数据')
@arg('-r', '--reset', metavar='name', dest='reset_name', nargs='?', help='重置某表，重置后可以重新导入数据')
@arg('-i', '--init', action='store_true', help='初始化数据库')
def main(**options):
    db_config('params')
    info(f'set db param')
    if options['list']:
        fprintf('{0:10s}{1:20s}',
                'select type,name from sqlite_master where type in ("table","view")order by name')
    if name := options['show']:
        fprint('select sql from sqlite_master where name=?', [name])
    if sql := options['qsql']:
        fprint(' '.join(sql))
    if sql := options['esql']:
        with connect():
            sql = ' '.join(sql)
            info(f'execute:{sql}')
            r = execute(sql)
            print(f'{r.rowcount:,d} 行数据受到影响')
    if options['load']:
        from .load import loadall
        info('开始导入参数')
        loadall()
        info('导入参数完成')
    if name := options['reset_name']:
        with connect():
            r = execute('delete from LoadFile where name=?', [name])
            print(f"重置 {name}", '成功' if r.rowcount else '失败')
    if options['init']:
        for name in ('jqb', 'jym', 'nbzh', 'nk', 'params', 'teller', 'yyzg'):
            print(f'执行 sql/{name}.sql')
            executefile('gmongo', f'sql/{name}.sql')
