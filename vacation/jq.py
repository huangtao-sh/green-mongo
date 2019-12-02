# 项目：   工作平台
# 模块：   假期表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2018-11-01 20:47

from orange import R, datetime, arg, now
from itertools import cycle
from glemon import Document, P, enlist

YEAR = R / r'.*?(\d{4})年'
Pattern = R / r'\s*(?P<xh>.*?)、(?P<name>.*?)：(?P<fj>.*?)。((?P<sb>.*?)。)?\s*'
Rq = R / (r'((?P<y1>\d{4})年)?(?P<m1>\d{1,2})月(?P<d1>\d{1,2})日'
          r'(?P<flag>至)?'
          r'((((?P<y2>\d{4})年)?(?P<m2>\d{1,2})月)?(?P<d2>\d{1,2})日)?')
WEEKDAY = {7: "星期日", 6: '星期六'}

HEADERS = [{
    'header': '日期',
}, {
    'header': '假期标志',
}, {
    'header': '假期属性',
}, {
    'header': '备注',
}, {
    'header': 'AB户标志',
}, {
    'header': '一户通标志',
}]


def parsedate(s, year):
    for r in Rq.finditer(s):
        r = r.groupdict()
        flag, y1, m1, d1, y2, m2, d2 = tuple(
            map(r.__getitem__, enlist('flag,y1,m1,d1,y2,m2,d2')))
        y1 = y1 or year
        y2 = y2 or y1 or year
        d1 = datetime("-".join([y1, m1, d1]))
        if flag:
            d2 = datetime("-".join([y2, m2 or m1, d2]))
            yield from d1.iter(d2 + 1)
        else:
            yield d1


class Holiday(Document):
    _projects = enlist('_id,anpai,ab')

    @classmethod
    @arg('-f', '--fetch', action='store_true', help='从网站获取假期表')
    @arg('-e',
         '--export',
         dest='begindate',
         default='noset',
         nargs='?',
         help='显示假期表')
    @arg('-s',
         '--show',
         dest='year',
         default='noset',
         nargs='?',
         help='显示假期安排')
    @arg('-m', '--mailto', action='store_true', help='邮件发送交易码参数')
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
        if options.get('mailto'):
            cls.mailto()

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

    @classmethod
    def iter(cls, begin, years=9):
        workdays = set()
        holidays = {}
        for obj in cls.find(P._id >= begin[:4]):
            year = obj._id
            for a in obj.anpai:
                s = Pattern == a
                d = s.groupdict()
                holidays.update(
                    zip(parsedate(d.get('fj'), year), cycle([d['name']])))
                sb = d.get('sb')
                if sb:
                    workdays.update(parsedate(sb, year))
        year = begin[:4]
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
        ab = obj.ab
        data = []
        begin = datetime(f'{year}-1-1')
        for d in begin.iter(begin.add(years=years)):
            memo = holidays.get(d) or WEEKDAY.get(d.isoweekday())
            if not memo:
                flag, sx, memo = '0', '0', ''
            elif memo.startswith('星期') and d in workdays:
                flag, sx, memo = '0', '0', '调休上班'
            else:
                flag, sx = '1', '2'
            ab_ = ab if flag == '1' else "A" if ab == 'B' else "B"
            if d.month == 1 and d.day == 1:
                obj = cls.objects.get(str(d.year))
                if obj:
                    obj.ab = ab
                    obj.save()
            data.append((d % '%Y%m%d', flag, sx, memo, ab, ab_))
            ab = ab_
        return data

    @classmethod
    def export(cls, begindate):
        from orange.xlsx import Book
        begindate = datetime(begindate or now() + 5) % '%Y%m%d'
        data = cls.iter(begindate)
        data = [x for x in data if x[0] >= begindate]
        if data:
            fn = '假期参数表%s.xlsx' % (begindate)
            with Book(fn) as rpt:
                rpt.add_table('A1',
                              sheet='假期参数表',
                              columns=HEADERS,
                              autofilter=False,
                              data=data)

    @classmethod
    def mailto(cls):
        from orange.xlsx import Book
        from params.mail import Mail, MailClient
        begindate = datetime(now() + 5) % '%Y%m%d'
        data = cls.iter(begindate)
        data = [x for x in data if x[0] >= begindate]
        if data:
            filename = '假期参数表%s.xlsx' % (begindate)

            def writer(fn):
                with Book(fn) as rpt:
                    rpt.add_table('A1',
                                  sheet='假期参数表',
                                  columns=HEADERS,
                                  autofilter=False,
                                  data=data)

            mail = Mail(sender='hunto@163.com',
                        to='huangtao@czbank.com',
                        subject='假期表参数',
                        body='假期表参数，请审阅！')
            mail.attach(filename, writer=writer)
            with MailClient()as client:
                mail.post(client)
                print('发送邮件成功！')
