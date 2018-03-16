# 项目：数据库模型
# 模块：假期表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-11-19 17:51

from orange import *
from imongo import *
from .jqb import Vacation
from orange.hclient import *

URL='http://sousuo.gov.cn/list.htm'
values={'searchfield':'title', # 搜索标题
        'n':5,                 # 只取三条记录
        't':'paper',
        'sort':'pubtime',      # 按发布时间排序
        'timetype':'timeqb',
        'title':'部分节假日安排'}

class FetchVacation(Crawler):
    async def run(self):
        soup=await self.get_soup(URL,params=values) # 获取文件列表
        table=soup.find('table',class_='dataList')  # 查找表格
        urls=[]  # 收集文件的地址
        for a in table.find_all('a',target='_blank'):
            if R/r'国务院办公厅关于\d{4}年部分节假日安排的通知'==a.text:
                urls.append(self.get_page(a['href']))
        await wait(urls) # 并发分析假期文件
        
    async def get_page(self,url): # 假期文件分析
        soup=await self.get_soup(url) # 获取文件
        s=[]
        for p in soup.find_all('p'):  # 获取文件内容
            s.append(p.text.strip())
        s="\n".join(s)
        s=R/r'　+?'/s%'\n'
        Vacation.parse(content=s)     # 添加假期表
        
fetch = FetchVacation.start

if __name__=='__main__':
    fetch()
    
