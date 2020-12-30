from .init import init as _init
from orange import arg
from orange.utils.sqlite import db_config
from .load import load_reg, check_reg

db_config('~/.data/nkwg.db')


@arg('-i', '--init', action='store_true', help='初始化数据库')
@arg('-c', '--check', action='store_true', help='检查登记情况')
@arg('-r', '--report', action='store_true', help='报告登记情况')
@arg('-l', '--load', action='store_true', help='导入数据')
def main(init=False, check=False, report=False, load=False):
    if init:
        _init()
    if load:
        load_reg()
    if report:
        check_reg()
