# 项目：   工作平台
# 模块：   机构码表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-10-16 20:48

from .branch import get_branches

branches = get_branches()
branches['331000000'] = '总行业务处理中心'
branches['331000808'] = '总行营业中心'


def branch(jgm: str) -> str:
    '''根据机构码获取所在分行'''
    br = branches.get(jgm)
    if not br or br == '总行':
        br = '总行清算中心'
    return br
