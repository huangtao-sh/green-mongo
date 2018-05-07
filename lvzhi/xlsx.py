# 项目：会计主管履职报告
# 模块：Excel导出模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-04-19 13:45
# 修订：2017-11-10

from orange.xlsx import Book
from .model import LvZhi, P, Path
from .lzwt import LzWenTi

FORMATS = {       # 预定义格式
    'h1': {'font_name': '黑体', 'text_wrap': True, 'font_size': 18,
           'align': 'center'},  # 一级标题
    'wrap': {'font_name': '微软雅黑', 'text_wrap': True, 'valign': 'vcenter'},  # 折行
    'cwrap': {'font_name': '微软雅黑', 'text_wrap': True, 'align': 'center',
              'valign': 'vcenter'},  # 换行并居中
    'normal': {'font_name': '微软雅黑'}}  # 正常

YLBFORMAT = [
    {'header': '机构', "width": 40, 'format': 'cwrap'},
    {'header': '报告人', 'width': 9, 'format': 'cwrap'},
    {'header': '序号', 'width': 8, 'format': 'cwrap'},
    {'header': '种类', 'width': 29.5, 'format': 'wrap'},
    {'header': '内容', 'width': 100, 'format': 'wrap'},
    {'header': '收集问题', 'width': 51, 'format': 'wrap'},
]


def export_ylb(fn=None):
    qc = LvZhi.cur_qc
    path = Path(r'~\OneDrive\工作\工作档案\会计履职报告') / qc
    path.ensure()
    fn = fn or str(path/('营业主管履职报告一览表（%s）.xlsx' % (qc)))
    data = []
    for obj in LvZhi.objects(P.qc == qc):
        for k in obj.detail:
            data.append(('%s%s' % (obj.jg, obj.bm), obj.bgr, k['xh'],
                         k['bgzl'], k['jtnr'], None))
    with Book(fn) as book:
        book.add_formats(FORMATS)
        book.worksheet = '明细表'
        book.add_table("A1", columns=YLBFORMAT, data=data)
    print('共导出%d条数据' % (len(data)))


WTFORMAT = [
    {'header': '问题分类', 'width': 13.5, 'format': 'cwrap'},
    {'header': '机构', 'width': 24.63, 'format': 'cwrap'},
    {'header': '具体内容', 'width': 57.63, 'format': 'wrap'},
    {'header': '报告人', 'width': 10.88, 'format': 'cwrap'},
    {'header': '答复人', 'width': 10.88, 'format': 'cwrap'},
    {'header': '答复意见', 'width': 47.38, 'format': 'wrap'}]


def export_wt(yyb=True, fn=None):
    yf = max(LvZhi.objects.distinct('qc'))
    print('当前月份：%s' % (yf))
    path = Path(r'~\OneDrive\工作\工作档案\会计履职报告') / yf
    fn = fn or str(path / ('营业主管履职报告（%s）.xlsx' % (yf)))
    data = list(LzWenTi.objects(yf=yf).order_by('bm', 'wtfl', 'dfr').scalar(
        'wtfl', 'jg', 'jtnr', 'bgr', 'dfr', 'dfyj'))
    with Book(fn) as book:
        book.add_formats(FORMATS)
        book.worksheet = '运营管理部'
        book.A1_F1 = '营业主管履职报告重点问题（%s）' % (yf), "h1"
        book.add_table("A2", columns=WTFORMAT, data=data)
        print('共导出%d条数据' % (len(data)))
