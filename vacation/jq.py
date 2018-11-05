# 项目：   工作平台
# 模块：   假期表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2018-11-01 20:47

from orange import R, datetime, arg, now
from itertools import cycle
from glemon import Document, P, enlist

YEAR = R/r'.*?(\d{4})年'
Pattern = R/r'\s*(?P<xh>.*?)、(?P<name>.*?)：(?P<fj>.*?)。((?P<sb>.*?)。)?\s*'
Rq = R / (r'(?P<m1>\d{1,2})月(?P<d1>\d{1,2})日'
          r'(?P<flag>至)?'
          r'(((?P<m2>\d{1,2})月)?(?P<d2>\d{1,2})日)?')
WEEKDAY = {7: "星期日", 6: '星期六'}

HEADERS = [{'header': '日期', },
           {'header': '假期标志', },
           {'header': '假期属性', },
           {'header': '备注', },
           {'header': 'AB户标志', },
           {'header': '一户通标志', }]


def parsedate(s, year):
    for r in Rq.finditer(s):
        r = r.groupdict()
        flag, m1, d1, m2, d2 = tuple(
            map(r.__getitem__, enlist('flag,m1,d1,m2,d2')))
        d1 = datetime("-".join([year, m1, d1]))
        if flag:
            d2 = datetime("-".join([year, m2 or m1, d2]))
            yield from d1.iter(d2+1)
        else:
            yield d1


class Holiday(Document):
    _projects = enlist('_id,anpai,ab')

    @classmethod
    @arg('-f', '--fetch', action='store_true', help='从网站获取假期表')
    @arg('-e', '--export', dest='begindate', default='noset', nargs='?', help='显示假期表')
    @arg('-s', '--show', dest='year', default='noset', nargs='?', help='显示假期安排')
    def main(cls, **options):
        if options.get('fetch'):
            from .fetch import FetchVacation
            FetchVacation.start()
        begindate = options.get('begindate')
        if begindate != 'noset':
            cls.export(begindate)
        year = options.get('year')
        if year != 'noset':
            cls.show(year)

    @classmethod
    def show(cls, year):
        year = year or str(now().year)
        obj = cls.objects.get(year)
        if obj:
            print(f'年份： {year}')
            if obj.ab:
                print(f'初始AB户标志：{obj.ab}')
            print(*obj.anpai, sep='\n')

    @classmethod
    def parse(cls, txt):
        year = None
        anpai = []
        for r in txt.splitlines():
            if not year:
                k = YEAR.match(r)
                if k:
                    year = k.groups()[0]
            else:
                if Pattern == r:
                    anpai.append(r)
        cls.find(_id=year).upsert_one(anpai=anpai)
        print(f'{year}年假期安排获取成功')

    def __iter__(self):
        workdays = set()
        holidays = {}
        anpai = self.anpai or ""
        year = self._id
        ab = self.ab
        for a in anpai:
            s = Pattern == a
            d = s.groupdict()
            holidays.update(
                zip(parsedate(d.get('fj'), year), cycle([d['name']])))
            sb = d.get('sb')
            if sb:
                workdays.update(parsedate(sb, year))
        begin = datetime(f'{self._id}-1-1')
        for d in begin.iter(begin.add(years=1)):
            memo = holidays.get(d)or WEEKDAY.get(d.isoweekday())
            if not memo:
                flag, sx, memo = '0', '0', ''
            elif memo.startswith('星期') and d in workdays:
                flag, sx, memo = '0', '0', '调休上班'
            else:
                flag, sx = '1', '2'
            ab_ = ab if flag == '1' else "A" if ab == 'B' else "B"
            yield d % '%Y%m%d', flag, sx, memo, ab, ab_
            ab = ab_
        self.ab_ = ab   # 返回次年 1 月 1 日的 AB 户标志

    @classmethod
    def export(cls, begindate):
        from orange.xlsx import Book
        begindate = datetime(begindate or now()+5) % '%Y%m%d'
        year = begindate[:4]
        obj = cls.objects.get(year)
        if not obj:
            print('起始年份无对应的假期表，请先下载')
            exit(1)
        if not obj.ab:
            ab = input(f'请输入 {year} 年 1 月 1 日的 AB 户标志：')
            ab = ab.upper()
            if ab not in 'AB':
                print('AB户标志输入不正确!')
                exit(2)
            obj.ab = ab
            obj.save()
        data = []
        for d in obj:
            if d[0] >= begindate:
                data.append(d)
        for y in range(int(year)+1, int(year)+9):
            y = str(y)
            if obj.anpai:
                obj_ = cls.objects.get(y)
                if obj_:
                    obj_.ab = obj.ab_
                else:
                    obj_ = cls(_id=y, ab=obj.ab_)
                obj_.save()
            else:
                obj_ = cls(_id=y, ab=obj.ab_)
            obj = obj_
            for d in obj:
                data.append(d)
            fn = '假期参数表%s.xlsx' % (begindate)
            with Book(fn) as rpt:
                rpt.add_table('A1', sheet='假期参数表', columns=HEADERS,
                              autofilter=False, data=data)
