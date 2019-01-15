# 项目：   工作平台
# 模块：   版本说明
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-03 21:08

from glemon import Document, P, enlist
from orange import HOME, R, first, datetime, now
from xlrd import open_workbook

ROOT = HOME / 'OneDrive/工作/工作档案/投产版本说明'


def jym(s):
    return '%04d' % s if isinstance(s, (float, int)) else s


def endate(s):
    if not s:
        return datetime(3000, 12, 31)
    elif '实际' in s:
        return datetime('2100-12-31')
    else:
        s = s.replace('年', '-').replace('月', '-').replace('日',
                      '').replace('前', '').replace('：', ':')
        return datetime(s)


def dedate(s):
    if s.year == 3000:
        return None
    elif s.year == 2100:
        return "实际业务发生时"
    else:
        s=datetime(s)
        return f'{s.year}年{s.month}月{s.day}日 ' + s % "%H:%m" +'前'

def read_xls(filename, sheetindex):
    with open_workbook(str(filename)) as book:
        sheet = book.sheets()[sheetindex]
        data = sheet._cell_values
        for r1, r2, c1, c2 in sheet.merged_cells:
            v = data[r1][c1]
            for r in range(r1, r2):
                for c in range(c1, c2):
                    data[r][c] = v
    return data

class BanbenShouming(Document):
    _projects = enlist('rq,xh,xm,jym,jymc,nr,yhyy,yzjg,wcsj,yzyq,lxr')

    @classmethod
    def convert(cls):
        filename = str(ROOT.find('附件：版本说明*.xlsx'))
        print(f'处理版本说明文件：{filename}')
        data = read_xls(filename, 0)
        rq = first(R/'\d{8}'/filename)
        projects = cls._projects[1:]
        objs = []
        for r in data[1:]:
            d = dict(zip(projects, r[:10]))
            d['xh'] = int(d['xh'])
            d['rq'] = rq
            d['jym'] = jym(d['jym'])
            d['wcsj'] = endate(d['wcsj'])
            if d['nr']:
                objs.append(d)
        cls.find(P.rq == rq).delete()
        cls.insert_many(objs)
        for obj in cls.find(P.rq == rq).order_by(P.xh, P.lxr, P.jym):
            print(obj.xh, obj.lxr, obj.jym, dedate(obj.wcsj))


BanbenShouming.convert()
