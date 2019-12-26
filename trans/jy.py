#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-16 12:16:49
# @Author  : 黄涛 (huang.t@live.cn)
# @Link    : http://www.jianshu.com/u/3bf5919e38a7
# @Version : $Id$
# 修订：2018-09-06 调整导出文件格式，增加菜单
# 修改：2018-10-19 19:53 使用 loadfile 导入文件
# 修订：2018-12-12 09:09 查询交易码时，按交易码排序
# 修改：2018-12-13 17:32 调整 jym 查询列表的显示格式

from orange import classproperty, arg, Path, now, R, wlen
from glemon import P
from glemon.load import LoadDocument as Document
from .gangwei import JyGangwei


class JyShbs(Document):
    '''不需要事后补扫交易清单'''
    _projects = ('_id', )
    load_options = {
        'file': {
            'filter': lambda row: row[2] == '8',
            'columns': (1, )
        },
        'dupcheck': True,
    }


class JyCdjy(JyShbs):
    '''需要校验磁道信息的交易'''
    load_options = {
        'dupcheck': True,
    }
    pass


class JyMenu(Document):
    _projects = 'menu', 'submenu', 'trans'

    @classproperty
    def menus(self):
        # 一级菜单列表
        return self.objects.distinct('menu')

    @classmethod
    def submenus(cls, menu):
        # 一级菜单项下的二级菜单
        return cls.find(menu=menu).distinct('submenu')

    @classmethod
    def trs(cls, menu, submenu=None):
        # 某一菜单下所有交易
        d = cls.find(menu=menu, sumenu=submenu).first()
        return d or d.trans

    @classmethod
    def get_path(cls, code):
        # 获取指定交易码的菜单路径
        d = cls.find(trans=code).first()
        if d:
            return d.menu, d.submenu

    @classmethod
    def procdata(cls, data, options):
        datas = []
        for child in data:
            menu = child.attrib['DisplayName']
            trans = []
            for node in child:
                if node.tag == 'SubMenu':
                    trs = [n.attrib['Code'] for n in node if n.tag == 'Trade']
                    datas.append((menu, node.attrib['DisplayName'], trs))
                elif node.tag == 'Trade':
                    trans.append(node.attrib['Code'])
            if trans:
                datas.append((menu, None, trans))
        return datas


SHAMA = (
    ('jymc', '交易名称'),
    ('_id', '交易码'),
    ('jyz', '交易组'),
    ('jyzm', '交易组名'),
    ('yxj', '优先级'),
    ('wdsqjb', '网点授权级别'),
    ('zxsqjb', '中心授权级别'),
    ('bxwdsq', '必须网点授权'),
    ('zxsqjg', '中心授权机构'),
    ('bxzxsq', '必须中心授权'),
    ('jnjb', '技能级别'),
    ('xzbz', '现转标志'),
    ('wb', '是否外包'),
    ('dets', '大额提示'),
    ('dzdk', '是否扫描电子底卡'),
    ('sxf', '是否收手续费'),
    ('htjc', '是否需要后台监测'),
    ('jdfs', '事中监督扫描方式'),
    ('bssx', '补扫的限时时间'),
    ('sc', '是否需要审查'),
    ('mz', '是否允许抹账'),
    ('cesq', '是否允许超额授权'),
    ('fjjyz', '附加交易组'),
    ('shbs', '事后补扫'),
    ('cdjy', '磁道校验'),
)

TRANSFER = {
    'wdsqjb': {
        '1': '1-主办授权',
        '2': '2-主管授权'
    },
    'zxsqjb': {
        '1': '1-主办授权',
        '2': '2-主管授权'
    },
    'zxsqjg': {
        '0': '0-总中心',
        '1': '1-分中心'
    },
    'dets': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'dzdk': {
        '0': '0-不扫描',
        '1': '1-扫描'
    },
    'sxf': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'htjc': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'sc': {
        '0': '0-不需要',
        '1': '1-需要'
    },
    'wb': {
        '2': '2-需要',
        '1': '1-不需要'
    },
    'mz': {
        '0': '0-不允许',
        '1': '1-允许'
    },
    'jdfs': {
        '0': '0-不扫描',
        '1': '1-实时扫描',
        '2': '2-补扫'
    },
    'xzbz': {
        "CashIn": "CashIn-现金收",
        "CashOut": "CashOut-现金付",
        "TransIn": "TransIn-转账收",
        "TransOut": "TransOut-转账付",
        "SelfCashIn": "SelfCashIn-自助现金收",
        "SelfCashOut": "SelfCashOut-自助现金付",
        "SelfTransIn": "SelfTransIn-自助转账收",
        "SelfTransOut": "SelfTransOut-自助转账付",
    }
}

FORMAT = [
    {
        'header': '交易名称',
        'width': 44
    },
    {
        'header': '交易码'
    },
    {
        'header': '交易组'
    },
    {
        'header': '交易组名称',
        'width': 18.4
    },
    {
        'header': '优先级'
    },
    {
        'header': '网点授权级别',
        'width': 18.4
    },
    {
        'header': '中心授权级别',
        'width': 18.4
    },
    {
        'header': '必须网点授权'
    },
    {
        'header': '中心授权机构'
    },
    {
        'header': '必须中心授权'
    },
    {
        'header': '技能级别'
    },
    {
        'header': '现转标志',
        'width': 22.8
    },
    {
        'header': '是否外包',
        'width': 13.8
    },
    {
        'header': '大额提示',
        'width': 13.8
    },
    {
        'header': '是否扫描电子底卡',
        'width': 13.8
    },
    {
        'header': '是否收手续费',
        'width': 13.8
    },
    {
        'header': '是否需要后台监测',
        'width': 13.8
    },
    {
        'header': '事中扫描方式',
        'width': 13.8
    },
    {
        'header': '补扫的限时时间'
    },
    {
        'header': '是否需要审查',
        'width': 13.8
    },
    {
        'header': '是否允许抹账',
        'width': 13.8
    },
    {
        'header': '是否允许超额授权'
    },
    {
        'header': '附加交易组'
    },
    {
        'header': '事后补扫'
    },
    {
        'header': '磁道校验'
    },
    {
        'header': '一级菜单',
        'width': 16.33
    },
    {
        'header': '二级菜单',
        'width': 30.67
    },
]


def conv(row):
    row = [x.strip() for x in row]
    if len(row) < 22:
        row.append(None)
    return row


class JyJiaoyi(Document):
    _projects = '_id', 'jymc', 'jyz', 'yxj', 'wdsqjb', 'zxsqjb',\
        'bxwdsq', 'zxsqjg', 'bxzxsq', 'jnjb', 'xzbz', 'wb',\
        'dets', 'dzdk', 'sxf', 'htjc', 'jdfs', 'bssx', 'sc', 'mz', 'cesq', 'fjjyz'
    _textfmt = '{self._id}\t{self.jyz}\t{self.jyzm}\t{self.jymc}'
    load_options = {
        'file': {
            'converter': conv,
        },
        'dupcheck': True,
        'drop': True
    }
    _profile = {
        '交易码': '_id',
        '交易名称': 'jymc',
        '交易组': 'jyz',
        '交易组名': 'jyzm',
    }

    @classmethod
    def procrow(cls, row, converter):
        if len(row) < 22:
            row.append(None)
        return super().procrow(row, converter)

    @classmethod
    def get_item(cls, jym):
        obj = cls.find(_id=jym).first()

        def trans(a):
            v = getattr(obj, a)
            if a in TRANSFER:
                return TRANSFER[a].get(str(v))
            else:
                return v

        if obj:
            k = [(b, trans(a)) for a, b in SHAMA]
            return k

    @classmethod
    def export(cls, fn=None):
        def trans(obj, a):
            v = getattr(obj, a)
            if a in TRANSFER:
                return TRANSFER[a].get(str(v))
            else:
                return v

        data = []
        data2 = []
        for obj in cls.objects.order_by(P._id):
            d1 = [trans(obj, a[0]) for a in SHAMA]
            d2 = [getattr(obj, a[0]) for a in SHAMA]
            menus = JyMenu.get_path(obj._id) or [None, None]
            d2.extend(menus)
            d1.extend(menus)
            data.append(d1)
            data2.append(d2)
        d = now().add(months=-1) % ('%Y-%m')
        fn = fn or str(Path('~/Documents/交易码表（%s）.xlsx' % (d)))
        from orange.xlsx import Book
        with Book(fn) as book:
            book.add_table('A1', columns=FORMAT, data=data, sheet='交易码表')
            book.add_table("A1", columns=FORMAT, data=data2, sheet='交易码参数')

    @property
    def jyzm(self):
        obj = JyGangwei.objects.get(self.jyz)
        return obj and obj.name

    @property
    def shbs(self):  # 事后补扫
        return 'FALSE' if JyShbs.objects.get(self._id) else "TRUE"

    @property
    def cdjy(self):  # 磁道校验
        return 'TRUE' if JyCdjy.objects.get(self._id) else 'FALSE'

    @classmethod
    @arg('-e', '--export', action='store_true', help='导出交易码文件')
    @arg('query', nargs='?', help='查询交易信息')
    def main(cls, export=False, query=None):
        if export:
            cls.export()
            print('导出交易码表成功！')
        if query:
            if R / r'\d{4}' == query:
                obj = cls.get_item(query)
                if obj:
                    for n, v in obj:
                        print(n, v, sep=' ' * (20 - wlen(n)))
            else:
                cls.find(P.jymc.contains(query)).order_by(P._id).show(
                    '_id', 'jyz', 'jyzm', 'jymc', format_spec={
                        2: '20',
                    })
