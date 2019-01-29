# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20

from orange import Path, arg, HOME
from orange.utils.sqlite import db_config, execute, findone, find, executefile, trans, fetch
from gmongo import checkload
from .db import init_db, drop_tables

db_config('lzbg')
brfile = HOME/'OneDrive/工作/参数备份/分行表/分行顺序表.xlsx'


@arg('-i', '--init', dest='init_', action='store_true', help='初始化')
@arg('-d', '--drop', nargs='*', dest='tables', metavar='table', help='删除数据库表')
@arg('-c', '--config', action='store_true', help='导入参数')
@arg('-l', '--load', action='store_true', help='导入报告文件')
@arg('-r', '--report', nargs='?', default='NOSET', metavar='period', dest='rptqc', help='报告上报情况')
@arg('-p', '--publish', action='store_true', help='发布报告')
@arg('-o', '--restore', action='store_true', help='发布报告')
def fhlz(init_=False, tables=None, config=False, load=False,
         rptqc=None, publish=False, restore=False):
    if tables:
        drop_tables(*tables)
    if init_:
        init_db()
    if config:
        from .fhlz import loadbrorder
        loadbrorder(brfile)
    if load:
        from .loadbrfile import loadfiles
        loadfiles()
    if restore:
        from .loadbrfile import restorefiles
        restorefiles()
    if rptqc != 'NOSET':
        from .reportbr import report
        report(rptqc)
    if publish:
        #from .fhlz import publish_reply
        # publish_reply()
        for r in fetch('select name,branch from brreport where period=?', ['2018-4']):
            print(*r)


@arg('-i', '--init', dest='init_', action='store_true', help='初始化')
@arg('-l', '--loadfile', action='store_true', help='导入文件')
@arg('-d', '--delete', metavar='branch', dest='branchs', nargs='*', help='删除机构')
@arg('-r', '--report', action='store_true', help='报告上报情况')
@arg('-w', '--wenti', action='store_true', help='收集问题')
@arg('-e', '--export', nargs="?", metavar='period', default='NOSET', dest='export_qc', help='导出一览表')
@arg('-p', '--publish', action='store_true', help='发布文档')
def lzbg(init_=False, loadfile=False, branchs=None, report=False,
         export_qc=None, wenti=False, show=False, publish=False):
    if init_:
        init_db()
    if loadfile:
        from .lzbg import load_file
        load_file()
    if branchs:
        from .tj import delete_branchs
        delete_branchs(branchs)
    if report:
        from .tj import do_report
        do_report()
    if export_qc != "NOSET":
        from .report import export_ylb
        export_ylb(export_qc)
    if wenti:
        from .report import export_wt
        export_wt()
    if publish:
        from .report import publish_wt
        publish_wt()
