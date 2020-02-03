# 项目：数据库表结构
# 模块：公共机构表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-01-19 15:01

from orange import arg, R
from glemon import Document, P, Descriptor

JGLX = {
    '00': '总行清算中心',
    '01': '总行营业部',
    '10': '分行业务处理中心',
    '11': '分行营业部',
    '12': '支行'
}


class GgJgm(Document):
    _projects = '_id', 'jgmc', 'dz', 'dh', 'zfhh', 'lx', 'kbrq', 'hzjgm'
    load_options = {
        'encoding': 'utf8',
        'sep': ',',
        'include': (0, 1, 4-43, 5-43, 7-43, 15-43, 16-43, 17-43),
        'drop': True,
        'dupcheck': True
    }
    _profile = {
        '机构号': '_id',
        '机构名称': 'jgmc',
        '地址': 'dz',
        '电话': 'dh',
        '支付系统行号': 'zfhh',
        '类型': 'jglx',
        '开办日期': 'kbrq',
        '汇总机构': 'hzjgm'
    }
    jglx = Descriptor('lx', JGLX)

    @classmethod
    @arg('query', help='查询条件')
    def main(cls, query=None):
        if R/r'\d{9}' == query:
            filter = P._id == query
        elif R/r'\d{12}' == query:
            filter = P.zfhh == query
        elif R/r'\d{2}' == query:
            filter = P.lx == query
        else:
            filter = P.jgmc.contains(query)
        for obj in cls.find(filter):
            obj.show()
            print('\n')
