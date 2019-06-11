# 项目：   工作平台
# 模块：   参数数据导入
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 16:46


def load_files():
    from gmongo import params
    params.branch.loadfile()
    params.ggnbzhmb.loadfile()
