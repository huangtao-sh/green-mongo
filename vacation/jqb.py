# 项目：假期表参数
# 模块：假期表参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-08-17 10:51
# 修改：2018-05-29

import re
import datetime as dt
import ONEDAY
from orange import arg, now, ensure, Path
from imongo import Document, EmbeddedDocument, StringField, IntField, ListField, \
    EmbeddedDocumentField, P
from collections import OrderedDict
from orange.xlsx import Book
from glemon import Document


WEEKDAY = {5: '星期六', 6: '星期日'}
Year = re.compile(r'(\d{4})年')
Holiday = re.compile(r'[一二三四五六七八九]、(.*?)：')
Num = re.compile(r'\d{1,2}')
Arrange = re.compile(r'(\d{1,2}月\d{1,2}日(?:至(?:\d{1,2}月)?(?:\d{1,2}日))?'
                     r'.*?(放假调休|补休|放假|上班))')

TYPES = {'放假调休': 'fjtx',
         '补休': 'bx',
         '放假': 'fj',
         '上班': 'sb'}

HOLIDAY_DAYS = {
    '元旦': 1,
    '春节': 3,
    '清明节': 1,
    '劳动节': 1,
    '端午节': 1,
    '中秋节': 1,
    '国庆节': 3, }

HEADERS = [{'header': '日期', },
           {'header': '假期标志', },
           {'header': '假期属性', },
           {'header': '备注', },
           {'header': 'AB户标志', },
           {'header': '一户通标志', }]


class ArrangeData(EmbeddedDocument):
    name = StringField()
    fj = StringField()
    bx = StringField()
    fjtx = StringField()
    sb = StringField()

    def _iter_item(self):
        for t in ('fj', 'bx', 'fjtx'):
            s = getattr(self, t)
            if s:
                yield s

    def iter(self, year):
        for t in self._iter_item():
            for d in self.trans(*t.split('、'), year=year):
                yield d.strftime('%Y%m%d'), '1', '2', self.name
        if self.sb:
            for d in self.trans(*self.sb.split('、'), year=year):
                yield d.strftime('%Y%m%d'), '0', '0', '调休上班'

    def days(self, year):
        days = 0
        for t in self._iter_item():
            days += len([x for x in self.trans(*t.split('、'),
                                               year=year) if x.weekday() < 5])
        if self.sb:
            days -= len([x for x in self.trans(*self.sb.split('、'), year=year)
                         if x.weekday() > 4])
        return days

    def describe(self, no=None):
        fmt = '%d、' % (no) if no else ''
        d = list(self._iter_item())
        fmt = fmt+self.name+'：'+'，'.join(d)+'。'
        if self.sb:
            fmt += self.sb+'。'
        return fmt

    def check(self, year, days):
        return self.days(year) == days

    @staticmethod
    def trans(*s, year=None):
        this_year = now().year
        if year:
            ensure(this_year-10 < year < year+10, '年份不能超过10年')
        else:
            year = this_year
        dates = []
        for d in s:
            numbers = [int(x) for x in Num.findall(d)]
            ensure(len(numbers) >= 2, '日期"%s"格式错误' % (d), 'error')
            ensure(len(numbers) <= 4, '日期"%s"格式错误' % (d), 'error')
            if len(numbers) == 2:
                dates.append(dt.date(year, *numbers))
            else:
                b = dt.date(year, *numbers[:2])
                if len(numbers) == 3:
                    numbers.pop(1)
                elif len(numbers) == 4:
                    numbers = numbers[-2:]
                e = dt.date(year, *numbers)
                while b <= e:
                    dates.append(b)
                    b += ONEDAY
        return dates


class Vacation(Document):
    year = IntField()
    base = ListField(StringField())
    arrangement = ListField(EmbeddedDocumentField(ArrangeData))

    @classmethod
    def fetch(cls):
        from .fetchjq import fetch
        fetch()

    def iter(self):
        if self.arrangement:
            for k in self.arrangement:
                for d in k.iter(self.year):
                    yield d

    @classmethod
    def show(cls, year):
        year = year or now().year
        vacation = cls.objects(year=int(year)).first()
        if vacation:
            print('%s年假期安排' % (year))
            for i, x in enumerate(vacation.arrangement):
                print(x.describe(i+1))
        else:
            print('没有找到该年度的年期安排')

    @classmethod
    def init_date(cls, begin, years=8):
        d = dt.date(begin, 1, 1)
        data = OrderedDict()
        while d < dt.date(begin+years, 1, 1):
            beiz = WEEKDAY.get(d.weekday(), None)
            if beiz:
                bz, sx = '1', '2'
            else:
                bz, sx = '0', '0'
            data[d.strftime('%Y%m%d')] = [bz, sx, beiz]
            d += ONEDAY
        return data

    @classmethod
    def update(cls, year, dates):
        for a in cls.objects(P.year >= year):
            for d, bz, sx, beiz in a.iter():
                if d in dates:
                    dates[d] = [bz, sx, beiz]
        a = cls.objects(year=year).first()
        ensure(a, '假期表参数未设置！')
        if a.base:
            bz, abh, yht = a.base
        else:
            s = input('基准日期%s的AB户状态未设置,请依次输入该日期的工作日标志、AB'
                      '户、一户通，格式如：0,A,B\n'
                      '请输入：' % (dt.date(year-1, 12, 31)))
            sr = s.split(',')
            ensure(len(sr) == 3, '输入参数个数不正确')
            bz, abh, yht = sr
            ensure(((abh in 'AB')and(yht in 'AB')and(bz in '01')),
                   '输入参数格式不正确')
            a.base = sr
            a.save()
        for d, v in dates.items():
            if bz == '0':
                abh = 'A' if abh == 'B' else 'B'
            bz = v[0]
            if bz == '0':
                yht = 'A' if yht == 'B' else 'B'
            v.extend([abh, yht])
        for a in cls.objects(P.year >= year):
            if a.arrangement:
                v = dates[dt.date(a.year, 12, 31).strftime('%Y%m%d')]
                cls.objects(
                    year=a.year+1).upsert_one(base=[v[0], v[-2], v[-1]])
        return dates

    @classmethod
    def export(cls, basedate=None, years=8, fn=None):
        basedate = basedate or (dt.datetime.today() +
                                dt.timedelta(days=5)).strftime('%Y%m%d')
        year = int(basedate[:4])
        dates = cls.init_date(year, years)
        dates = cls.update(year, dates)
        data = []
        for d, v in dates.items():
            if d >= basedate:
                data.append([d, *v])
        fn = fn or '假期参数表%s.xlsx' % (basedate)
        with Book(fn) as rpt:
            rpt.add_table('A1', sheet='假期参数表', columns=HEADERS,
                          autofilter=False, data=data)
        if not fn:
            print('导出参数表成功!')

    @classmethod
    def parse(cls, filename=None, content=None):
        lines = []
        if filename:
            lines = Path(filename).lines
        elif content:
            lines = content.splitlines()
        year = None
        for row, line in enumerate(lines):
            m = Year.search(line)
            if m:
                year = int(m.groups()[0])
                break
        ensure(year, '未能正确解析出年份，请核实！')
        vacation = cls.objects(year=year).first() or cls(year=year)
        vacation.arrangement.clear()
        for line in lines[row:]:
            m = Holiday.search(line)
            if m:
                name = m.groups()[0]
                a = ArrangeData(name=name)
                for ar, tp in Arrange.findall(line):
                    setattr(a, TYPES[tp], ar)
                # ensure(a.check(year,HOLIDAY_DAYS.get(name,1)),'假期%s天数不正确！'%(name))
                vacation.arrangement.append(a)
        vacation.save()
        return True

    @classmethod
    @arg('-p', '--parse', nargs='?', metavar='filename',
         dest='filename', help='分析假期通知文件')
    @arg('-e', '--export', default='NOSET', dest='basedate',
         metavar='basedate', nargs='?', help='导出参数文件')
    @arg('-s', '--show', nargs='?', default='NOSET', dest='syear',
         metavar='yaer', help='展示假期安排')
    @arg('-f', '--fetch', action='store_true',
         help='从官方网站上获取数据')
    def main(cls, filename=None, basedate="NOSET", syear="NOSET", fetch=False):
        if filename:
            cls.parse(filename=filename)
        if basedate != 'NOSET':
            cls.export(basedate)
        if syear != 'NOSET':
            cls.show(syear)
        if fetch:
            cls.fetch()
