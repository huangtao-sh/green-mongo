from orange.xlsx import Header
from orange.utils.sqlite import fetchone, fetch, tran, execute, connect
from orange import now

from orange import R, datetime, arg, now
from itertools import cycle
from glemon import Document, P, enlist

YEAR = R / r'.*?(\d{4})年'
Pattern = R / r'\s*(?P<xh>.*?)、(?P<name>.*?)：(?P<fj>.*?)。((?P<sb>.*?)。)?\s*'
Rq = R / (r'((?P<y1>\d{4})年)?(?P<m1>\d{1,2})月(?P<d1>\d{1,2})日'
          r'(?P<flag>至)?'
          r'((((?P<y2>\d{4})年)?(?P<m2>\d{1,2})月)?(?P<d2>\d{1,2})日)?')
WEEKDAY = {7: "星期日", 6: '星期六'}


def show(year):
    year = year or str(now().year)
    sql = 'select * from jqb where year=?'
    obj = fetchone(sql, [year])
    if obj:
        print(f'年份： {obj[0]}')
        if obj[2]:
            print(f'初始AB户标志：{obj[2]}')
        print(obj[1])


Headers = [
    Header('日期'),
    Header('假期标志'),
    Header("假期属性"),
    Header('备注'),
    Header('AB户标志'),
    Header('一户通标志')]


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


def iter_(begin, years=9):
    workdays = set()
    holidays = {}
    for year, anpai, ab in fetch('select * from jqb where year>=?', [begin[:4]]):
        for a in anpai.splitlines():
            s = Pattern == a
            d = s.groupdict()
            holidays.update(
                zip(parsedate(d.get('fj'), year), cycle([d['name']])))
            sb = d.get('sb')
            if sb:
                workdays.update(parsedate(sb, year))
    year = begin[:4]
    obj = fetchone('select * from jqb where year=?', [begin[:4]])
    if not obj:
        print('起始年份无对应的假期表，请先下载')
        exit(1)
    ab = obj[2]
    if not ab:
        ab = input(f'请输入 {year} 年 1 月 1 日的 AB 户标志：')
        ab = ab.upper()
        if ab not in 'AB':
            print('AB户标志输入不正确!')
            exit(2)

        with connect():
            execute('update jqb set ab=? where year=?', [ab, year])
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
            if fetchone('select ab from jqb where year =?', [d.year]):
                with connect():
                    execute('update jqb set ab=? where year=?', [ab, d.year])
        data.append((d % '%Y%m%d', flag, sx, memo, ab, ab_))
        ab = ab_
    return data


def export(begindate):
    from orange.xlsx import Book
    begindate = datetime(begindate or now() + 5) % '%Y%m%d'
    data = iter_(begindate)
    data = [x for x in data if x[0] >= begindate]
    if data:
        fn = f'假期参数表{begindate}.xlsx'
        with Book(fn) as rpt:
            rpt.add_table('A1',
                          sheet='假期参数表',
                          columns=Headers,
                          autofilter=False,
                          data=data)


def mailto():
    from orange.xlsx import Book
    from params.mail import Mail
    begindate = datetime(now() + 5) % '%Y%m%d'
    data = iter_(begindate)
    data = [x for x in data if x[0] >= begindate]
    if data:
        filename = f'假期参数表{begindate}.xlsx'

        def writer(fn):
            with Book(fn) as rpt:
                rpt.add_table('A1',
                              sheet='假期参数表',
                              columns=Headers,
                              autofilter=False,
                              data=data)

        mail = Mail(sender='hunto@163.com',
                    to='huangtao@czbank.com',
                    subject='假期表参数',
                    body='假期表参数，请审阅！')
        mail.attach(filename, writer=writer)
        mail.post()
        print('发送邮件成功！')
