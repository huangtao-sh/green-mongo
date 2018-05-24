from glemon import Document,P
from orange import datetime

class GgJqb(Document):
    # 日期、标标，属性，备注
    _projects='_id','bz','sx','memo'

    @classmethod
    def next_day(cls,begin,days):
        begin=datetime(begin)%'%Y'


