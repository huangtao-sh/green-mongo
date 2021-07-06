# 项目：   履职报告问题处理
# 模块：   主程序
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-06-21 20:14

import gmongo.lzwt.db  # 初始化数据库
from orange import arg


@arg('-l', '--load', action='store_true', help='导入问题')
@arg('-u', '--update', action='store_true', help='更新问题')
@arg('-p', '--publish', action='store_true', help='发布履职报告')
def main(**options):
    if options['load']:
        from .load import load_wt
        load_wt()
