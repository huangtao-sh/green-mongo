# 项目：工作平台
# 模块：主管履职报告报表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-25 20:48
# 修改：2018-07-29 增加问题转换功能
# 修订：2020-04-24 15:05 设备问题导出独立的 Excel 文件

from .lzbg import ROOT
from orange import Path, extract
import json
from gmongo import fetch, fetchone, procdata, R

FORMATS = {       # 预定义格式
    'h1': {'font_name': '黑体', 'text_wrap': True, 'font_size': 18,
           'align': 'center'},  # 一级标题
    'wrap': {'font_name': '微软雅黑', 'text_wrap': True, 'valign': 'vcenter'},  # 折行
    'cwrap': {'font_name': '微软雅黑', 'text_wrap': True, 'align': 'center',
              'valign': 'vcenter'},  # 换行并居中
    'normal': {'font_name': '微软雅黑'}}  # 正常


YLBFORMAT = [
    {'header': '机构', "width": 20, 'format': 'cwrap'},
    {'header': '报告人', 'width': 9, 'format': 'cwrap'},
    {'header': '内容', 'width': 50, 'format': 'wrap'},
    {'header': '收集问题', 'width': 50, 'format': 'wrap'},
]

SBFORMAT = [
    {'header': '机构', "width": 20, 'format': 'cwrap'},
    {'header': '报告人', 'width': 9, 'format': 'cwrap'},
    {'header': '异常机具', 'width': 35, 'format': 'wrap'},
    {'header': '异常内容', 'width': 50, 'format': 'wrap'},
]


def export_ylb(qc=None, fn=None):
    from .tj import fetch_period
    qc = qc or fetch_period()
    print(f'期次    ：{qc}')
    ylb_path = ROOT / '一览表'
    ylb_path.ensure()
    fn = ylb_path / ('营业主管履职报告一览表（%s）.xlsx' % (qc))

    if fn.exists():
        s = input('%s 已存在，是否覆盖，Y or N?\n' % (fn.name))
        if s.upper() != 'Y':
            return
    print(f'生成文件：{fn}')
    wt_data, zh_data, sb_data = [], [], []
    db = fetch(
        'select br,name,zhjj,sbmc,ycnr,content from report where period=?', [qc])
    for br, name, zhjj, sbmc, ycnr, content in db:
        for zl, zyx, content in json.loads(content):
            if any(x in zl for x in ('建议', '问题')) and len(content) >= 10:
                wt_data.append((br, name, content, None))
        if len(zhjj) > 5:
            zh_data.append((br, name, zhjj, None))
        if sbmc or ycnr:
            sb_data.append((br, name, sbmc, ycnr))

    fn.write_tables(
        {'sheet': '问题及建议', 'columns': YLBFORMAT, 'data': wt_data},
        {'sheet': '需总行解决问题', 'columns': YLBFORMAT, 'data': zh_data},
        formats=FORMATS, force=True
    )
    print('导出问题：%d条' % (len(wt_data)))
    print('需总行解决问题：%d条' % (len(zh_data)))
    sbwt = ROOT/'设备问题'
    sbwt.ensure()
    if len(sb_data):
        (sbwt/f'设备问题（{qc}）.xlsx').write_tables(
            {'sheet': '机具问题', 'columns': SBFORMAT, 'data': sb_data},
            formats=FORMATS, force=True
        )
    print('设备问题：%d条' % (len(sb_data)))


WTFORMAT = [
    {'header': '问题分类', 'width': 13.5, 'format': 'cwrap'},
    {'header': '机构', 'width': 24.63, 'format': 'cwrap'},
    {'header': '具体内容', 'width': 57.63, 'format': 'wrap'},
    {'header': '报告人', 'width': 10.88, 'format': 'cwrap'},
    {'header': '答复人', 'width': 10.88, 'format': 'cwrap'},
    {'header': '答复意见', 'width': 47.38, 'format': 'wrap'}]


def export_wt(fn=None):
    ylb_path = ROOT / '一览表'
    filename = max(ylb_path.glob('营业主管履职报告一览表*.xlsx'))
    print(f'正在处理文件：{filename}')
    wt_path = ROOT / '处理问题'
    wt_path.ensure()
    qici = extract(filename.pname, r'\d{4}-\d{2}')
    print(qici)
    fn = wt_path / ('营业主管履职报告（%s）.xlsx' % (qici))
    datas = []
    for idx, name, data in filename.iter_sheets():
        if name in ('问题及建议', '需总行解决问题'):
            for br, name, nr, wts in data[1:]:
                if wts:
                    for wt in wts.split('\n\n'):
                        datas.append((None, br, wt, name, None, None))

    with fn.write_xlsx(formats=FORMATS) as book:
        book.worksheet = '运营管理部'
        book.A1_F1 = '营业主管履职报告重点问题（%s）' % (qici), "h1"
        book.add_table("A2", columns=WTFORMAT, data=datas)
        print('共导出%d条数据' % (len(datas)))
