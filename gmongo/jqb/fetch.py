'''
项目：假期表参数程序
作者：黄涛
日期：2021-01-16  数据库从 MongoDB 迁移至 SQLite
'''
from orange.utils.hclient import Crawler, wait
from orange import R
from orange.utils.sqlite import tran, execute

URL = 'http://sousuo.gov.cn/list.htm'
values = {'searchfield': 'title',  # 搜索标题
          'n': 5,                 # 只取最近5年的记录
          't': 'paper',
          'sort': 'pubtime',      # 按发布时间排序
          'timetype': 'timeqb',
          'title': '部分节假日安排'}


class FetchVacation(Crawler):
    async def run(self):
        soup = await self.get_soup(URL, params=values)  # 获取文件列表
        table = soup.find('table', class_='dataList')  # 查找表格
        urls = []  # 收集文件的地址
        for a in table.find_all('a', target='_blank'):
            if R/r'国务院办公厅关于\d{4}年部分节假日安排的通知' == a.text:
                urls.append(self.get_page(a['href']))
        await wait(urls)  # 并发分析假期文件

    async def get_page(self, url):  # 假期文件分析
        soup = await self.get_soup(url)  # 获取文件
        s = []
        for p in soup.find_all('p'):  # 获取文件内容
            s.append(p.text.strip())
        s = "\n".join(s)
        s = R/r'　+?'/s % '\n'
        parse(s)


YEAR = R / r'.*?(\d{4})年'
Pattern = R / r'\s*(?P<xh>.*?)、(?P<name>.*?)：(?P<fj>.*?)。((?P<sb>.*?)。)?\s*'
Rq = R / (r'((?P<y1>\d{4})年)?(?P<m1>\d{1,2})月(?P<d1>\d{1,2})日'
          r'(?P<flag>至)?'
          r'((((?P<y2>\d{4})年)?(?P<m2>\d{1,2})月)?(?P<d2>\d{1,2})日)?')
WEEKDAY = {7: "星期日", 6: '星期六'}


def parse(txt):
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

    with connect():
        execute('insert or ignore into jqb(year,anpai) values(?,?)',
                [year, "\n".join(anpai)])
    print(f'{year}年假期安排获取成功')
