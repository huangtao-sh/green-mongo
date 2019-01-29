# 项目：   工作平台
# 模块：   分管行长及运营主管履职报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-23 20:14
from orange import now
import yaml
from gmongo import execute, R, HOME, loadcheck

ROOT = HOME/'OneDrive/工作/工作档案/分行履职报告'


DatePattern = tuple(R / x for x in (r'(\d{4})(\d{2})', r'(\d{4}).?(\d{1,2})'))
TYPES = ('行领导', '分管行长', '部门负责人')
FenHang = R/r'[:：]\s*(.*?分行)'
BaogaoRen = R/r'报告人[:：]\s*(.*?)\s'


def getdate(s):
    for pattern in DatePattern:
        m = pattern.search(s)
        if m:
            year, month = (int(x)for x in m.groups())
            m = year*4+(month-2)//3
            return f'{year}-{month:02d}', f'{m//4}-{m%4+1}'


def get_type(s):
    for i, x in enumerate(TYPES):
        if x in s:
            return i//2


def get_bgr(s):
    m = BaogaoRen.search(s)
    return m and m.group(1)


def get_br(s):
    m = FenHang.search(s)
    return m and m.group(1)


@loadcheck
def loadfile(filename, curqc):
    data = []
    print(f'开始处理文件：{filename.name}')
    for sheet in filename.iter_sheets():
        rows = sheet[2]
        if len(rows) > 2:
            months = getdate(rows[2][0])
            if months:
                data.append([*months, rows])
    data = max(data)
    if data:
        date, period, rows = data
        if period != curqc:
            raise Exception('非当前期次')
        print(f'报告日期： {date}       期次：{period}')
        type_ = get_type(rows[0][0])
        bgr = get_bgr(rows[2][0])
        branch = get_br(rows[1][0])
        print(f'分行:      {branch}      报告类型：   {type_}     ')
        print(f'报告人：   {bgr}        报告时间：   {date}')
        if any([x is None for x in [type_, bgr, branch]]):
            raise Exception('报告格式不正确')
        header = [rows[i][0]for i in range(3)]
        contents = [(row[:2])for row in rows[3:]]
        content = yaml.dump({
            'header': header,
            'content': contents
        })
        execute('insert or replace into brreport values(?,?,?,?,?,?)',
                [period, type_, branch, bgr, date, content])


def loadfiles():
    curqc = (now().add(months=-1)) % "%Q"
    for file in (ROOT/'分行上报').glob('*.xls?'):
        try:
            loadfile(file, curqc=curqc)
        except Exception as e:
            print(e)


def restorefiles():
    for file in (ROOT/'报告').glob('*.xlsx'):
        print(file.name)
