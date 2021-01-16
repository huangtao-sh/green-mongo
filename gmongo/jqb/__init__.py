'''
项目：假期表参数程序
作者：黄涛
日期：2021-01-16  数据库从 MongoDB 迁移至 SQLite
'''

from .fetch import FetchVacation
from gmongo import executefile
from orange.utils.sqlite import db_config, fetch, fetchvalue

from orange import arg

db_config('~/.data/jqb.db')


@arg('-f', '--fetch', action='store_true', help='从网站获取假期表')
@arg('-e', '--export', dest='begindate', default='noset', nargs='?', help='显示假期表')
@arg('-s', '--show', dest='year', default='noset', nargs='?', help='显示假期安排')
@arg('-m', '--mailto', action='store_true', help='邮件发送交易码参数')
def main(**options):
    executefile('gmongo', 'sql/jqb.sql')
    if options.get('fetch'):
        from .fetch import FetchVacation
        FetchVacation.start()
    begindate = options.get('begindate')
    if begindate != 'noset':
        from .jqb import export
        export(begindate)
    year = options.get('year')
    if year != 'noset':
        from .jqb import show
        show(year)
    if options.get('mailto'):
        from .jqb import mailto
        mailto()
