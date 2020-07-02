# 项目：   工作平台
# 模块：   履职报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-18 20:39

from orange.utils.sqlite import findone, findvalue, find, execute, executemany, trans, fetchvalue,\
    fprint, fprintf, fetch
from orange import cstr, R


def fetch_period() -> str:
    d = findvalue('select period from report order by date desc limit 1')
    if not d:
        raise Exception('无数据记录')
    return d


def do_report():
    period = fetch_period()
    print('当前期次：%s' % (period))
    print(
        f'报告数量：{fetchvalue("select count(distinct title||br)from report where period=?",[period])}')
    hd_sql = ('select brorder,brname from brorder a '
              'left join report b '
              'on instr(b.br,a.brname)>0 and period =? and b.lx="事后监督" '
              'where b.br is null  '
              'order by brorder'
              )
    print('事后监督报告漏报清单')
    print('应报：', fetchvalue('select count(*) from brorder where brname not like "%总行%" and brname not in ("香港分行","义乌分行")'),
          "实报：", fetchvalue("select count(*)from report where lx='事后监督' and period=?", [period]))
    fprintf("{0:2d}            {1:20s}", hd_sql, [period])
    yyzgs = fetchvalue('select count(distinct jg)from yyzg  '
                       'where jg not like "331000%" and jg not in '
                       '("191000000","342002000","361000000","421000000","551000000")')
    bss = fetchvalue(
        'select count(*)from report where period=? and lx="营业主管"', [period])
    print(f'营业主管数：{yyzgs},实报：{bss}')
    for xm, count in fetch('select xm,count(xm)as sl from yyzg where js like "a%" '
                           'and jg not like "331000%" and jg not in '
                           '("191000000","342002000","361000000","421000000","551000000")'
                           'group by xm having sl>1'):
        x = fetchvalue(
            'select count(*)from report where name=? and period=? and lx="营业主管" ', [xm, period])
        if x < count:
            print(f'{xm} ,应报：{count} 实报：{x}')
            fprint("select * from report where name=? and period=?",
                   [xm, period])
    zg_sql = (
        'select jgmc,xm from yyzg  a '
        'left join report b on a.xm=b.name and period=? and lx="营业主管" '
        'where  a.js like "a%" and b.name is null '
        'and a.jg not like "331000%" and a.jg not in '
        '("191000000","342002000","361000000","421000000","551000000")'
    )
    fprintf('{0:20s} {1:25s}', zg_sql, [period])
    print(' - '*10)
    zg_sql = (
        'select br,name from report  b '
        'left join yyzg a on a.xm=b.name and a.js like "a%"  '
        'where  a.xm is null and lx="营业主管" and period=? '
    )
    fprintf('{0:20s} {1:25s}', zg_sql, [period])
