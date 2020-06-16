# 项目：   工作平台
# 模块：   参数数据导入
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 16:46

from gmongo.params import branch, ggnbzhmb
from gmongo.nbzh.load import loadnbzh, create_hz
from gmongo.params import load_jym as jym
from gmongo.params.txl import loadfile as load_txl
from gmongo.params.teller import load_teller


def load_files():
    ggnbzhmb.loadfile()  # 导入内部账户模板
    loadnbzh()  # 导入内部账户表
    create_hz()  # 创建内部账户汇总表
    jym.loadfile()  # 导入交易码参数
    jym.loadmenu()  # 导入交易码菜单
    jym.loadjyz()  # 导入交易组
    load_txl()  # 导入通讯录
    load_teller() # 导入柜员表