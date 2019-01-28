# 项目：   工作平台
# 模块：   分行履职报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-28 20:31

from gmongo import fetch, fetchvalue

rpt_sql = ('select a.brname,b.name,c.name from brorder a '
           'left join brreport b on b.period=? and a.brname=b.branch and b.type=0 '
           'left join brreport c on c.period=? and a.brname=c.branch and c.type=1 '
           'order by a.brorder'
           )

get_qc_sql = 'select period from brreport order by period desc limit 1 '


def get_qc():
    return fetchvalue(get_qc_sql)


def report():
    qc = get_qc()
    print(f'当前期次 {qc}')
    print('序号     分行        分管行长    运营主管')
    for i, row in enumerate(fetch(rpt_sql, [qc, qc]), 1):
        print(i, *row, sep='\t')
