# 项目：   工作平台
# 模块：   机构表参数
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-12-04 21:45
# 修订：2020-06-15 19:21 和 go 语言的 grape 共享数据库

from orange.utils.sqlite import db
from orange import extract, R

BranchPattern = R / '浙商银行(.*?公司)?(.*?行).*?'


def get_branches():
    '获取机构对应分行的名称'
    sql = 'select a.jgm,b.mc from ggjgm a left join ggjgm b on a.hzjgm=b.jgm'

    def convert(obj):
        return (obj[0], extract(obj[1], BranchPattern, 2))

    with db('~/.data/params.db') as d:
        branches = dict(map(convert, d.fetch(sql)))
        branches['331000000'] = '总行业务中心'
        branches['331000808'] = '总行营业中心'
        return branches


branches = get_branches()


def branch(jg):
    br = branches.get(jg)
    if not br or br == '总行':
        br = '总行清算中心'
    elif br == '义乌分行':
        br = '金华分行'
    return br
