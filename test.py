import gmongo.jqb
from gmongo.jqb.jqb import show, export
from gmongo.jqb.mail import conf
# export('2020-11-20')
from orange.utils.sqlite import db_config, tran, execute, fetch, connect

db_config('~/.data/jqb.db')

conf()
