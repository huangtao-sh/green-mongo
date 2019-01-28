# 项目：工作平台
# 模块：分行履职报告模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-01-23 10:16

from gmongo import checkload, executemany, procdata, HOME, trans, R, executetrans
from orange import extract

brfile = HOME/'OneDrive/工作/参数备份/分行表/分行顺序表.xlsx'
SAVEPATH = HOME/'OneDrive/工作/工作档案/分行履职报告'


@executetrans
def loadbrorder():
    def _():
        r = executemany(
            'insert or replace into brorder(brname,brorder)values(?,?)',
            procdata(brfile.sheets('分行顺序表'), mapper={
                '分行名称': None,
                '顺序': int,
            })
        )
        print(f'导入{r.rowcount}条数据')
    if checkload(brfile, _):
        print(f'{brfile.name}已导入，忽略')


def loadwenti(filename):
    qc = extract(filename.pname, r'\d{4}\-\d')
    hz = set(FhLvzhi.find((P.qc == qc) &
                          (P.lb == '分管行长')).distinct('bgr'))
    data = filename.sheets('分行履职报告问题表')
    if data:
        cls.find(P.qc == qc).delete()
        for d in data[1:]:
            d = d[:6]
            if not d[3].strip():
                d[3] = '运营管理部'
            order = BRANCHS.get(d[0], 150)*10
            if d[1] not in hz:
                order += 1
            d.append(order)
            d.insert(0, qc)
            obj = cls(zip(cls._projects, d))
            obj.save()
        data = [x for x in cls.find(P.qc == qc).order_by(P.order).scalar(
            'fh', 'wtms', 'tcr', 'dfbm', 'dfyj'
        )]
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
                book.D = row[3], 'cnormal'
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
