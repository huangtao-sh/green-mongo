# 项目：工作平台
# 模块：数据库模型
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-25 20:44

from orange import datetime
from glemon import Document, P


class GgJqb(Document):
    _projects = '_id', 'bz'
    _load_mapper = [0, 1]

    @classmethod
    def next_day(cls, begin, days):
        begin = int(datetime(begin) % ('%Y%m%d'))
        result = cls.objects(
            P._id >= begin, P.bz == '0').order_by(P._id).limit(days+1).skip(days).limit(1).first()
        return result and result._id


next_workday = GgJqb.next_day
