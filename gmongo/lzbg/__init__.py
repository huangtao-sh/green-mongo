# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20

from orange import Path, arg, HOME
from orange.utils.sqlite import db_config, fprint
from gmongo import checkload
from .db import init_db, drop_tables

db_config('~/OneDrive/db/lzbg.db')
brfile = HOME/'OneDrive/工作/参数备份/分行表/分行顺序表.xlsx'


@arg('-i', '--init', dest='init_', action='store_true', help='初始化')
@arg('-d', '--drop', nargs='*', dest='tables', metavar='table', help='删除数据库表')
@arg('-c', '--config', action='store_true', help='导入参数')
@arg('-l', '--load', action='store_true', help='导入报告文件')
@arg('-r', '--report', nargs='?', default='NOSET', metavar='period', dest='rptqc', help='报告上报情况')
@arg('-p', '--publish', action='store_true', help='发布报告')
@arg('-e', '--export', nargs="?", metavar='period', default='NOSET', dest='export_qc', help='导出一览表')
@arg('-g', '--genban', action='store_true', help='导出跟班情况')
def fhlz(init_=False, tables=None, config=False, load=False,
         rptqc=None, publish=False, restore=False, genban=False,
         export_qc=None):
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
    if rptqc != 'NOSET':
        from .reportbr import report
        report(rptqc)
    if export_qc != 'NOSET':
        from .fhlz import export_ylb
        export_ylb(export_qc)
    if publish:
        from .fhlz import publish_reply
        publish_reply()
    if genban:
        from .fhlz import GenBan
        GenBan()


@arg('-i', '--init', dest='init_', action='store_true', help='初始化')
@arg('-l', '--loadfile', action='store_true', help='导入文件')
@arg('-r', '--report', action='store_true', help='报告上报情况')
@arg('-w', '--wenti', action='store_true', help='收集问题')
@arg('-e', '--export', nargs="?", metavar='period', default='NOSET', dest='export_qc', help='导出一览表')
@arg('-p', '--publish', action='store_true', help='发布文档')
@arg('-q', '--query', nargs='?', dest='sql', metavar='sql', default='NOSET', help='执行查询语句')
@arg('-R', '--Restore', action='store_true', help='恢复数据')
@arg('-U', '--update', action='store_true', help='更新进度')
def lzbg(init_=False, loadfile=False, branchs=None, report=False, Restore=False, update=False,
         export_qc=None, wenti=False, show=False, publish=False, sql=''):
    if init_:
        init_db()
    if loadfile:
        from .lzbg import load_file
        load_file()
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
        from .publish import publish_wt
        publish_wt()
    if sql != 'NOSET':
        fprint(sql)
    if Restore:
        from .publish import restore
        restore()
    if update:
        from .publish import update_wenti
        update_wenti()
