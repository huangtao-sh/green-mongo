# 项目：   工作平台
# 模块：   履职报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-18 20:39

from orange.utils.sqlite import findone, findvalue, find, execute, executemany, trans, fetchvalue,\
    fprint, fprintf, fetch, Path
from orange import cstr, R
from orange.xlsx import Header


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

    zgwb_sql = (
        'select jgmc,xm from yyzg  a '
        'left join report b on a.ygh=b.ygh and period=? and lx="营业主管" '
        'where  a.js like "a%" and b.ygh is null '
        'and a.jg not like "331000%" and a.jg not in '
        '("191000000","342002000","361000000","421000000","551000000")'
    )
    fprintf('{0:20s} {1:25s}', zgwb_sql, [period])
    print(' - '*10)
    zgyc_sql = (
        'select br,name from report  b '
        'left join yyzg a on a.ygh=b.ygh and a.js like "a%"  '
        'where  a.ygh is null and lx="营业主管" and period=? '
    )
    fprintf('{0:20s} {1:25s}', zgyc_sql, [period])

    with Path("~/Downloads/当期履职报告报送情况统计表.xlsx").write_xlsx(force=True)as book:
        book.add_table(sheet="事后监督未报送", data=fetch(hd_sql, [period]),
                       columns=[
            Header("分行序号", 8),
            Header("分行名称", 45)
        ])
        book.add_table(sheet="营业主管履职报告未报送清单", data=fetch(zgwb_sql, [period]),
                       columns=[
            Header("机构", 40),
            Header("姓名", 20)
        ])
        print(f"当期履职报告报送情况统计表已生成")

        book.add_table(sheet="营业主管履职报告异常报送清单", data=fetch(zgyc_sql, [period]),
                       columns=[
            Header("机构", 40),
            Header("姓名", 20)
        ])
        print(f"当期履职报告报送情况统计表已生成")
