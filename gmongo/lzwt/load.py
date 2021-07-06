# 项目：   履职报告问题
# 模块：   导入数据模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-06-21 20:54

from orange.utils.sqlite import executemany, loadcheck
from orange import Path, extract, get_md5

yyzgwt_sql = '''
insert or replace into lzwt(bh,rq,lx,jg,bgr,wtfl,wtms,dfbm,dfr)
values(?,?,"2",?,?,?,?,?,?)
'''

# @loadcheck


def load_yyzgwt(path):
    rq = extract(path.pname, r'\d{4}-\d{2}')
    print('报告日期：', rq)

    def read():
        for sheet in path.worksheets:
            print(sheet.name)
            for row in sheet._cell_values[1:]:
                if row[3]:
                    for lznr in row[3].split('\n\n'):
                        yield [*row[:2], lznr]

    for r in read():
        print(len(r), r)


def load_wt():
    path = Path('~/OneDrive/工作/工作档案/履职报告/一览表').find('营业主管履职报告一览表（????-??）.xlsx')
    print('处理文件：', path.name)
    load_yyzgwt(path)
