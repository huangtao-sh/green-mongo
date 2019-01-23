# 项目：   工作平台
# 模块：   分管行长及运营主管履职报告
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-23 20:14

from gmongo import db_config, execute, executemany, find, findone, findvalue, R, HOME
ROOT = HOME/'OneDrive/工作/工作档案/分行履职报告'

DatePattern = tuple(R / x for x in (r'(\d{4})(\d{2})', r'(\d{4}).?(\d{1,2})'))
TYPES = ('行领导', '分管行长', '部门负责人')
FenHang = R/r'[:：]\s*(.*?分行)'
BaogaoRen=R/r'报告人[:：]\s*(.*?)\s'


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
    m=BaogaoRen.search(s)
    return m and m.group(1)


def get_br(s):
    m = FenHang.search(s)
    return m and m.group(1)

def loadfile(filename):
    pass