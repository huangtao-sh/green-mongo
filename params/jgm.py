# 项目：数据库表结构
# 模块：公共机构表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-01-19 15:01

from orange import arg, R
from glemon import Document, P


class GgJgm(Document):
    _projects = '_id', 'jgmc', 'dz', 'dh', 'zfhh', 'lx', 'kbrq', 'hzjgm'
    load_options = {
        'mapper': {
            '_id': 0,
            'jgmc': 1,
            'dz': 4,
            'dh': 5,
            'zfhh': 7,
            'lx': 15,
            'kbrq': 16,
            'hzjgm': 17
        },
    }
    _textfmt = '''
机构号：    {self._id}
机构名称：  {self.jgmc}
地址：      {self.dz}
电话：      {self.dh}
支付行号：  {self.zfhh}
类型：      {self.lx}
开办日期：  {self.kbrq}
汇总机构：  {self.hzjgm}'''

    @classmethod
    @arg('query', help='查询条件')
    def main(cls, query=None):
        filter = None
        if R/'\d{9}' == query:
            filter = P._id == query
        elif R/'\d{12}' == query:
            filter = P.zfhh == query
        elif R/'\d{2}' == query:
            filter = P.lx == query
        else:
            filter = P.jgmc.contains(query)
        for obj in cls.objects(filter):
            print(obj)
