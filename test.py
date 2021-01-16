import gmongo.jqb
from gmongo.jqb.jqb import show, export
# export('2020-11-20')
from orange.utils.sqlite import db_config, tran, execute, fetch,connect

db_config('~/.data/jqb.db')

with connect():
    execute('update jqb set ab="A" where year="2020" ')

for r in fetch('select year,ab from jqb order by year'):
    print(r)
