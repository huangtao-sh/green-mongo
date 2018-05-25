# 项目：会计主管履职报告
# 模块：包模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-04-19 09:33
# 修改：2018-05-25 20:49 使用新版命令行


from .docs import LzBaogao, LzBranchs, LzWenTi
from .rpt import export_wt, export_ylb
from orange import arg


@arg('-r', '--report', action='store_true', help='报告当期上报情况')
@arg('-i', '--import', dest='import_', action='store_true', help='导入报告数据')
@arg('-d', '--delete', dest='branchs', metavar='branch', nargs='*', help='删除无用的机构')
@arg('-e', '--export', action='store_true', help='导出报告')
@arg('-c', '--collection', action='store_true', help='收集问题')
@arg('-w', '--wenti', action='store_true', help='导出问题')
def main(report=False, import_=False, branchs=None, export=False,
         collection=False, wenti=False):
    if import_:
        LzBaogao.import_file()
    if report:
        LzBaogao.report()
    if branchs:
        LzBranchs.remove(branchs)
    if export:
        export_ylb()
    if collection:
        LzWenTi.load_files()
    if wenti:
        export_wt()



'''
from .model import LvZhi
from .xlsx import export_ylb, export_wt
from orange import arg


@arg('-i', '--import', dest='_import', action='store_true', help='数据导入')
@arg('-e', '--export', action='store_true', help='导出一览表')
@arg('-r', '--report', action='store_true', help='报告报送情况')
def lvzhi(fetch=False, export=False, report=False, user=None, passwd=None,
          transfer=False, _import=False):
    if _import:
        LvZhi.load_files()
    if export:
        export_ylb()
    if report:
        LvZhi.report()


@arg('-i', '--import', dest='_import', action='store_true', help='导入问题数据')
@arg('-c', '--collect', action='store_true', help='收集问题')
@arg('-e', '--export', dest='rpt', action='store_true', help='导出问题,0-运营部，1-分部门，2-发布')
@arg('-a', '--assign', action='store_true', help='分派任务')
def lvzhiwenti(_import=False, collect=False, rpt=False, assign=False):
    if _import:
        from .sjdr import import_wenti
        import_wenti()
    if collect:
        from .lzwt import LzWenTi
        LzWenTi.load_files()
    if rpt:
        export_wt()
    if assign:
        from .assign import assign_task
        assign_task()
'''