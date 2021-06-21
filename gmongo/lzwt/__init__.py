# 项目：   履职报告
# 模块：   履职报告问题更新模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-06-21 20:14

import lzwt.db  # 初始化数据库
from orange import arg


@arg('-l', '--load', action='store_true', help='导入问题')
@arg('-u', '--update', action='store_true', help='更新问题')
def main(**options):
    print(options)
