# 项目：工作管理平台
# 模块：履职报告
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-03-22 16:36

from orange import Path, HOME, R, extract
from gmongo import db_config, fetch, fetchone, fetchvalue, executescript, transaction, execute,\
    loadcheck
from orange.utils.sqlite import insert

PeriodPattern = R/r'.*?(?P<year>\d{4}).*?(?P<month>\d{1,2})'


class Period(object):
    def __init__(self, time):
        r = PeriodPattern.match(time)
        if r:
            d = r.groupdict()
            self.year, self.month = d['year'], d['month']

    def __str__(self):
        return f'{self.year}年{self.month}月份'

    @property
    def value(self):
        return f'{self.year}-{int(self.month):02d}'


FORMATS = {
    'Title': {'font_name': '仿宋_GB2312', 'bold': True,
              'font_size': 18, 'align': 'center'},
    'Header': {'font_name': '黑体', 'font_size': 14, 'align': 'center'},
    'Text': {'font_name': '微软雅黑', 'font_size': 11,
             'align': 'left', 'valign': 'vcenter', 'text_wrap': True},
    'VText': {'font_name': '微软雅黑', 'font_size': 11,
              'align': 'center', 'valign': 'vcenter', 'text_wrap': True},
}

Widthes2 = {
    'A:A': 15.25,
    'B:B': 8.63,
    'C:C': 12.63,
    'D:D': 20.38,
    'E:E': 47.5,
    'F:G': 16,
    'H:H': 38.63,
    'I:I': 18.38
}
Widthes1 = {
    'A:A': 15.25,
    'B:B': 12.63,
    'C:C': 20.38,
    'D:D': 47.5,
    'E:F': 16,
    'G:G': 38.63,
    'H:H': 18.38
}

ROOT = HOME/'OneDrive/工作/工作档案/履职报告/营业主管履职报告重点问题与答复意见'


def publish_wt():
    path = ROOT.find('营业主管履职报告重点问题与答复意见*.xlsx')
    if path:
        loaddfyj(path)
    path = (HOME/'OneDrive/工作/工作档案/履职报告/处理问题').find('营业主管履职报告*完成.xlsx')
    if path:
        loadwt(path)
    export_file(path)


@loadcheck
def loaddfyj(filename):
    print(f'导入基准文件：{filename.name}')
    excludes = set()
    for sheet in filename.worksheets:
        if sheet.name in ('重点问题', '一般问题'):
            def procline(x):
                x = [l.strip() for l in x]
                x.insert(1, sheet.name)
                x[0] = Period(x[0]).value
                excludes.add(x[0])
                return x
            data = sheet._cell_values
            if len(data) > 3 and len(data[2]) == 8:
                data = tuple(map(procline, filter(None, data[2:])))
            insert('lzwt', data)
        else:
            def procline(x):
                x = [l.strip()for l in x]
                x[0] = Period(x[0]).value
                return x if x[0] not in excludes else None
            data = sheet._cell_values
            if len(data) > 3 and len(data[2]) == 9:
                data = tuple(filter(None, map(procline, data[2:])))
                insert('lzwt', data)
    count = fetchvalue('select count(reporter) from lzwt')
    print(f'共导入数据：{count:,d}')


@loadcheck
def loadwt(filename):
    print(f'导入最新处理文件：{filename.name}')
    data = filename.sheets(0)
    if len(data) > 3 and len(data[2]) >= 7:
        rq = Period(data[0][0]).value
        print(f'当前导入文件日期：{rq}')
        count = fetchvalue(
            'select count(reporter) from lzwt where period=?', [rq])
        if count > 0:
            confirm = input('基准文件中已有数据，是否重新导入？ Y or N')
            if confirm.lower() == "n":
                return
            r = execute('delete from lzwt weher period=?', [rq])
            print(r)
            print('存量数据已删除')

        def procline(line):
            line = [x.strip() for x in line]
            importance = '重要问题' if '重要问题' in line[6] else '一般问题'
            nline = [rq, importance]
            nline.extend(line[:7])
            return nline
        data = filter(None, map(procline, data[2:]))
        insert('lzwt', data)
        s = 0
        for r in fetch('select importance,count(period) from lzwt '
                       'where period=? group by importance ', [rq]):
            print(*r)
            s += int(r[1])
        print(f'共导入数据：{s:,d}')


def write_curpriod(book, period, importance):
    data = fetch('select * from lzwt '
                 'where period=? and importance =? '
                 'order by rowid ', [period, importance])
    if not data:
        return
    book.worksheet = importance
    book.set_widths(Widthes1)
    period = str(Period(period))
    book.A1_H1 = f'营业主管履职报告重点问题与答复意见（{period}）', 'Title'
    book.A2 = '提出时间 问题分类 机构 具体内容 报告人 反馈部门 答复意见 状态'.split(' '), 'Header'
    for row, d in enumerate(data, 3):
        book.row = row
        book.A = [period, d[2], d[3]], 'VText'
        book.D = d[4], 'Text'
        book.E = d[5:7], 'VText'
        book.G = d[7], 'Text'
        book.H = d[8], 'VText'
    book.set_border(f'A2:H{row}')


def write_year(book, year):
    data = fetch('select * from lzwt '
                 'where  period like ? '
                 'order by period,importance desc,rowid ', [f'{year}%'])
    if not data:
        return
    book.worksheet = f'{year}年汇总'
    book.set_widths(Widthes2)
    book.A1_H1 = f'营业主管履职报告重点问题与答复意见（{year}年）', 'Title'
    book.A2 = '提出时间 重要性 问题分类 机构 具体内容 报告人 反馈部门 答复意见 状态'.split(' '), 'Header'
    for row, d in enumerate(data, 3):
        book.row = row
        book.A = [str(Period(d[0])), d[1], d[2], d[3]], 'VText'
        book.E = d[4], 'Text'
        book.F = d[5:7], 'VText'
        book.H = d[7], 'Text'
        book.I = d[8], 'VText'
    book.set_border(f'A2:I{row}')


def export_file(path):
    path = Path(path)
    period = fetchvalue('select max(period) from lzwt')
    with path.write_xlsx()as book:
        book.add_formats(FORMATS)
        write_curpriod(book, period, '一般问题')
        write_curpriod(book, period, '重点问题')
        for r in fetch('select distinct substr(period,1,4)as year from lzwt '
                       'order by year desc'):
            write_year(book, r[0])
        print(f'导出文件 {path.name} 成功')
