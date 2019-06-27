# 项目：   工作平台
# 模块：   参数数据导入
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 16:46

from gmongo.params import branch, ggnbzhmb
from gmongo.nbzh.load import loadnbzh


def load_files():
    branch.loadfile()  # 导入机构码
    ggnbzhmb.loadfile()  # 导入内部账户模板
    loadnbzh()  # 导入内部账户表
