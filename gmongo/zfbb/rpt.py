# 项目：支付报表
# 模块：生成报表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-01-18 09:15
from orange import R,ensure
QcPattern=R/r'20\d{2}-[1234]'
def export(qc):
    ensure(QcPattern==qc,'期次的格式应为：YYYY-Q')
    year,q=qc.split('-')
    d=int(year)*12+(int(q)-1)*3-12
    months=[f'{m//12}{m%12+1:02d}' for m in range(d,d+15)]
    print(months)

