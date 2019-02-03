# 项目：支付报表
# 模块：生成报表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-01-18 09:15
from orange import R, ensure
from gmongo import find
from collections import defaultdict
QuaterPattern = R/r'20\d{2}-[1234]'
MonthPattern = R/r'20\d{2}-\d{2}'


def percent(b, t):
    return f'{(t-b)*100/b:7.2f}%' if b else ' '*3+'*'*5


QUATER_SQL = ('select a."id",sum(b.vv),sum(b.vv2) from parameter a '
              'join PaymentData b on a."in"=b."in" and a.dn=b.dn '
              'where b.at="CITY" and '
              '((a.rule=0 and b.subno=:end) or (a.rule=1 and b.subno between :begin and :end)) '
              'group by a."in",a.dn '
              )
MONTH_SQL = ('select a."id",b.vv,b.vv2 from parameter a '
             'join PaymentData b on a."in"=b."in" and a.dn=b.dn '
             'where b.at="CITY" and '
             'b.subno=? '
             'group by a."in",a.dn '
             )


def export(qc):
    print(f'当前期次： {qc}')
    if QuaterPattern == qc:
        year, q = qc.split('-')
        d = int(year)*12+(int(q)-1)*3-12
        # 生成 15 个连续的月份
        months = [f'{m//12}{m%12+1:02d}' for m in range(d, d+15)]
        data = defaultdict(lambda: [])                             # 初始化数据
        for i in (14, 2, 11):                                      # 分别获取当期、同比、环节数据
            for r in find(QUATER_SQL, {'begin': months[i-2], 'end': months[i]}):
                data[r[0]].extend(r[1:])
    elif MonthPattern == qc:
        year, m = qc.split('-')
        d = (int(year)-1)*12 + int(m)-1
        # 生成 12 个连续的月份
        months = [f'{d//12}{d%12+1:02d}' for d in range(d, d+13)]
        data = defaultdict(lambda: [])                             # 初始化数据
        for i in (12, 0, 11):                                      # 分别获取当期、同比、环节数据
            for r in find(MONTH_SQL, [months[i]]):
                data[r[0]].extend(r[1:])
    else:
        raise Exception('期次的格式应为：YYYY-Q 或 YYYY-MM')
    for k, v in sorted(data.items()):
        print(f'{k:02d}', *(f'{x:19,.2f}'for x in v[:2]), end='    ')
        print(percent(v[2], v[0]), percent(v[3], v[1]), sep='    ', end='    ')
        print(percent(v[4], v[0]), percent(v[5], v[1]), sep='    ')
