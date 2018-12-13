# 项目：会计主管履职报告
# 模块：包模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-04-19 09:33
# 修改：2018-05-25 20:49 使用新版命令行


from .docs import LzBaogao, LzBranchs, LzWenTi, LzDafu
from .rpt import export_wt, export_ylb
from orange import arg


@arg('-r', '--report', action='store_true', help='报告当期上报情况')
@arg('-i', '--import', dest='import_', action='store_true', help='导入报告数据')
@arg('-d', '--delete', dest='branchs', metavar='branch', nargs='*', help='删除无用的机构')
@arg('-e', '--export', action='store_true', help='导出报告')
@arg('-c', '--collection', action='store_true', help='收集问题')
@arg('-w', '--wenti', action='store_true', help='导出问题')
@arg('-p', '--publish', action='store_true', help='正式发布履职报告')
def main(report=False, import_=False, branchs=None, export=False,
         collection=False, wenti=False, publish=False):
    if import_:
        LzBaogao.import_file()
    if report:
        LzBaogao.report()
    if branchs:
        LzBranchs.remove(branchs)
    if export:
        export_ylb()
    if collection:
        LzWenTi.load_file()
    if wenti:
        export_wt()
    if publish:
        LzDafu.publish()
