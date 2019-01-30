# 项目：工作平台
# 模块：分行履职报告模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-01-23 10:16

from gmongo import executemany, procdata, HOME, R, execute, loadcheck,\
    fetch, transaction
from orange import extract
SAVEPATH = HOME/'OneDrive/工作/工作档案/分行履职报告'


@loadcheck
def loadbrorder(filename):
    r = executemany(
        'insert or replace into brorder(brname,brorder)values(?,?)',
        procdata(filename.sheets('分行顺序表'), mapper={
            '分行名称': None,
            '顺序': int,
        }))
    print(f'导入{r.rowcount}条数据')


@loadcheck
def _publish(filename, qc):
    hz = set(x[0] for x in fetch(
        'select name from brreport where type=0 and period=?', [qc]))
    data = filename.sheets('分行履职报告问题表')
    if data:
        execute('delete from lzwenti where period=? and type in (0,1)', [qc])
        data = tuple(
            procdata(data, header='分行,提出人,问题描述,答复部门,答复人,答复意见'.split(',')))
        for row in data:
            row.extend([0 if row[1] in hz else 1, qc])
        r = executemany('insert into lzwenti(rpt_branch,rpt_name,content,reply_depart,reply_name,reply,type,period)'
                        'values(?,?,?,?,?,?,?,?)', data)
        print(f'共导入 {r.rowcount} 条数据')


def publish_reply():
    path = (SAVEPATH/'答复意见').find('分行运营主管履职报告问题????-?.xls?')
    if path:
        qc = extract(path.pname, r'\d{4}\-\d')
        print(f'当前期次： {qc}')
        _publish(path, qc)
        _export(qc)
    else:
        print('未找到相应的文件')


export_sql = ('select a.rpt_branch,a.content,a.rpt_name,a.reply_depart,a.reply from lzwenti a '
              'left join brorder b on a.rpt_branch = b.brname '
              'where a.type in (0,1) and a.period=? '
              'order by b.brorder,a.type')

WIDTHS2 = {
    'A:A': 9.13,
    'B:B': 75.4,
    'C:C': 9.13,
    'D:D': 13,
    'E:E': 53.53
}
FORMATS2 = {
    'title': {'font_name': '黑体', 'font_size': 16, 'align': 'center', 'bold': True},
    'h2': {'font_name': '仿宋_GB2312', 'font_size': 12, 'align': 'center', 'bold': True,
           'bg_color': 'black', 'font_color': 'white'},
    'cnormal': {'font_name': '仿宋_GB2312', 'font_size': 12, 'align': 'center',
                'valign': 'vcenter', 'text_wrap': True, },
    'normal': {'font_name': '仿宋_GB2312', 'font_size': 12,  'valign': 'vcenter', 'text_wrap': True, },
}


def _export(qc):
    data = fetch(export_sql, [qc])
    title = "%s年%s季度分管行领导及部门负责人履职报告问题的答复意见" % tuple(qc.split('-'))
    filename = SAVEPATH / '正式答复意见' / ('关于%s.xlsx' % (title))
    print(filename)
    with filename.write_xlsx()as book:
        book.worksheet = '分行履职报告问题表'
        book.set_widths(WIDTHS2)
        book.add_formats(FORMATS2)
        book.A1_E1 = title, 'title'
        book.A2 = ['分行名称', '问题描述', '提出人', '答复部门', '答复意见'], "h2"
        fh_start, tcr_start = 3, 3
        tcr, fh = None, None
        for line, row in enumerate(data, 3):
            book.row = line
            book.B = row[1], 'normal'
            book.D = row[3] or "运营管理部", 'cnormal'
            book.E = row[4], 'normal'
            if fh != row[0]:
                if fh:
                    book['A%d:A%d' %
                         (fh_start, line-1)] = fh, 'cnormal'
                fh_start = line
                fh = row[0]
            if tcr != row[2]:
                if tcr:
                    book['C%d:C%d' %
                         (tcr_start, line-1)] = tcr, 'cnormal'
                tcr_start = line
                tcr = row[2]
        if fh:
            book['A%d:A%d' % (fh_start, line)] = fh, 'cnormal'
        if tcr:
            book['C%d:C%d' % (tcr_start, line)] = tcr, 'cnormal'
        book.set_border('A2:E%d' % (line))
