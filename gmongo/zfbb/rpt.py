# 项目：支付报表
# 模块：生成报表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-01-18 09:15
from orange import R, ensure
from orange.sqlite import find, connect
from collections import defaultdict
QcPattern = R/r'20\d{2}-[1234]'


def percent(b, t):
    return f'{(t-b)*100/b:7.2f}%' if b else ' '*3+'*'*5


SQL = ('select a."id",sum(b.vv),sum(vv2) from parameter a '
       'left join PaymentData b on a."in"=b."in" and a.dn=b.dn '
       'where b.at="CITY" and '
       '((a.rule=0 and b.subno=?) or (a.rule=1 and b.subno between ? and ?)) '
       'group by a."in",a.dn '
       )


def export(qc):
    ensure(QcPattern == qc, '期次的格式应为：YYYY-Q')
    year, q = qc.split('-')
    d = int(year)*12+(int(q)-1)*3-12
    months = [f'{m//12}{m%12+1:02d}' for m in range(d, d+15)]
    data = defaultdict(lambda: [])
    for i in (14, 2, 11):
        for r in find(SQL, [months[i], months[i-2], months[i]]):
            data[r[0]].extend(r[1:])
    for k, v in sorted(data.items()):
        print(f'{k:02d}', *(f'{x:19,.2f}'for x in v[:2]), end='    ')
        print(percent(v[2], v[0]), percent(v[3], v[1]), sep='    ', end='    ')
        print(percent(v[4], v[0]), percent(v[5], v[1]), sep='    ')
