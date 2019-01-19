# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20

from orange import Path, arg
from orange.utils.sqlite import db_config, execute, findone, find, executefile

db_config('lzbg')


@arg('-i', '--init', dest='init_', action='store_true', help='初始化')
@arg('-l', '--loadfile', action='store_true', help='导入文件')
@arg('-d', '--delete', metavar='branch', dest='branchs', nargs='*', help='删除机构')
@arg('-r', '--report', action='store_true', help='报告上报情况')
@arg('-f', '--force', action='store_true', help='强制初始化')
@arg('-w', '--wenti', action='store_true', help='收集问题')
@arg('-e', '--export', nargs="?", metavar='period', default='NOSET', dest='export_qc', help='导出一览表')
def main(init_=False, loadfile=False, branchs=None, report=False, force=False,
         export_qc=None, wenti=False, show=False):
    if init_:
        executefile('gmongo', 'sql/lzbg.sql')
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
