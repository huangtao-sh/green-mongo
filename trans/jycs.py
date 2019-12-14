# 项目：工作平台
# 模块：交易码参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-29 15:18
# 修订：2019-01-02 20:42 新增命令行处理模块
# 修订：2019-12-01 11:58 新增相关功能
# 修订：2019-12-13 17:53 修正导出数据不正确的问题

from orange import Path, R, now, arg, HOME, Data, datetime, R
from glemon import Document, P, Shadow, Nor, Or, And
from trans.jy import JyJiaoyi, FORMAT
from orange.xlsx import Header

today = datetime.now() % '%F'
profile = Shadow.read('jycs') or {}
Widths = [
    40, 9, 9, 27, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    9, 17, 21, 20, 10, 10, 0.01
]


def save_profile():
    Shadow.write('jycs', profile)


ROOT = HOME / 'OneDrive/工作/参数备份/生产参数'

path = ROOT / '交易码参数.xlsx'


def itos(length=4):
    def _(s):
        return f'%0{length}d' % (int(s))

    return _


def dt(s):
    try:
        return datetime(s) % '%F'
    except:
        return s


def bool_(s):
    return 'TRUE' if s in ('TRUE', '1', 1) else 'FALSE'


LEIBIE = {'新增': 0, '修订': 1, '删除': 2}
JYFORMAT = FORMAT.copy()
JYFORMAT.extend([{
    'header': '创建日期',
    'width': 8.43
}, {
    'header': '投产时间',
    'width': 8.43
}, {
    'header': '备注',
    'width': 60
}])

JYSX = {
    'jymc': '交易名称',
    'jym': '交易码',
    'jyz': '交易组',
    'yxj': '优先级',
    'wdsqjb': '网点授权级别',
    'zssqjb': '中心授权级别',
    'wdsq': '网点授权',
    'zssq': '中心授权',
    'zssqjg': '中心授权机构',
    'jnjb': '技能级别',
    'xzbz': '现转标志',
    'wb': '外包',
    'dets': '大额提示',
    'dzdk': '电子底卡',
    'szjd': '事中监督',
    'bssx': '补扫时限',
    'mz': '抹账',
    'cesq': '超额授权',
    'fzjyz': '辅助交易组',
    'shbs': '事后补扫',
    'cdjy': '磁道校验',
    'cd': '菜单',
}


def confirm(prompt):
    s = input(prompt, ',请确认? Yes or No')
    return s in ('Y', 'y', 'yes', 'Yes')


HD_Header = (Header('交易名称', 40), Header('交易码', 10), Header('总行审查', 10),
             Header('分行审查', 10), Header('流水勾对', 10))
JX_JYM_Headers = (Header('交易名称',
                         40), Header('交易码',
                                     10), Header('交易类型\n（内部/外部/其他）', 35))
JX_ZSXS_Headers = (Header('交易名称', 40), Header('交易码', 10), Header('折算系数', 8))

JX_Header = '交易名称	交易码	账户行打印	附加要素补录	附加要素补录复核	权限管理岗(打印)	后台权限管理授权	后台权限管理录入	后台权限管理审查	后台录入A	后台录入B	后台录入C	后台验印	前台异机授权	业务监测岗	核算中心退票通知	后台授权	同城退票确认	开户网点退票确认录入	客户信息补录	异常授权岗	异常处理岗	退回交易	前台录入A	前台录入B	通知开户网点	返回前台	二维码打印	回单打印	网点打印	核算中心打印	凭证管理	核算中心退票录入	交易发起岗	审查岗（比对）复核	审查岗(比对)	前台授权	数据变更发起岗	数据变更复核岗	放款受理岗	放款审核岗	放款核准岗	放款复核岗	验票与保管岗	辅助录入岗	审查岗	信用卡审核岗'.split(
    '\t')
JX_Widths = [10] * len(JX_Header)
JX_Widths[0] = 40
JX_HJ_Headers = [Header(h, w) for h, w in zip(JX_Header, JX_Widths)]


class PmJiaoyi(Document):
    # 类别：0-新增，1-修改，2-删除
    # 交易码，交易名称，交易组，优先级，网点授权级别，中心授权级别，网点授权标志，中心授权机构，中心授权标志，
    # 技能级别，现转标志，外包，大额提示，电子底卡，手续费，后台监测，事中扫描，补扫时限，审查，抹账，
    # 辅助交易组，事后补扫，磁道校验，一级菜单，二级菜单，建立时间，投产时间
    _projects = ('lb', 'jymc', 'jym', 'jyz', 'jyzm', 'yxj', 'wdsqjb', 'zxsqjb',
                 'bxwdsq', 'zxsqjg', 'bxzxsq', 'jnjb', 'xzbz', 'wb', 'dets',
                 'dzdk', 'sxf', 'htjc', 'jdfs', 'bssx', 'sc', 'mz', 'cesq',
                 'fjjyz', 'shbs', 'cdjy', 'yjcd', 'ejcd', 'bz', 'cjrq', 'tcrq')

    @classmethod
    def update_(cls):
        '更新数据库记录'
        if profile.get('mtime', 0) < path.mtime:
            cls.load()
        cls.dump()
        profile['mtime'] = path.mtime
        save_profile()

    @classmethod
    def load(cls):
        data = path.sheets('新增')
        header = data[0]
        if (not profile.get('header')
                and len(header) == len(cls._projects)) or True:  # 保存文件头
            profile['header'] = header
            save_profile()
            print('保存表头成功！')
        for row in Data(data[1:],
                        filter=lambda row: bool(row[1]),
                        converter={
                            1: itos(4),
                            4: itos(2),
                            5: itos(1),
                            6: itos(1),
                            7: bool_,
                            8: itos(1),
                            9: bool_,
                            10: itos(2),
                            12: itos(1),
                            13: itos(1),
                            14: itos(1),
                            15: itos(1),
                            16: itos(1),
                            17: itos(1),
                            18: itos(1),
                            19: itos(1),
                            20: itos(1),
                            21: bool_,
                            23: bool_,
                            24: bool_,
                            -3: dt,
                            -2: dt
                        }):
            _id = row[-1]
            fields = cls._projects[1:]
            obj = dict(zip(fields, row))
            obj['lb'] = 0
            if JyJiaoyi.objects.get(row[1]):
                cls.objects.filter(P.jym == row[1], P.lb == 0,
                                   Or(P.tcrq.exists(False),
                                      P.tcrq >= today)).update_one(ytc=True)
                print(f'交易码： {row[1]} 已投产，忽略')
            elif _id:
                if obj.get('tcrq') == '删除':
                    cls.objects.filter(P._id == _id).delete_one()
                else:
                    cls.objects.filter(P._id == _id).upsert_one(**obj)
            else:
                cls(obj).save()
        print('导入文件成功！')

    @classmethod
    def dump(cls):
        fields = [*cls._projects[1:], '_id']
        data = cls.objects.filter(
            Nor(P.lb != 0, P.ytc == True, And(P.tcrq != "",
                                              P.tcrq < today))).scalar(fields)
        header = profile['header']
        Headers = [Header(h, w) for h, w in zip(header, Widths)]
        data = map(lambda x: [*x[:-1], str(x[-1])], data)
        with path.write_xlsx(force=True) as book:
            book.add_table('A1', '新增', data=data, columns=Headers)
            print('导出文件成功！')

    @classmethod
    def touchan(cls, date):
        date = datetime(date) % '%F'
        prompt = (f'Please enter command date({date}):\n'
                  '(D)ate:yyyy-mm-dd,'
                  '(E)xport,'
                  '{jym},'
                  '(U)set:{jym},'
                  '(L)ist,'
                  '(Q)uit\n')
        s = ''
        while s.lower() != 'q':
            s = input(prompt)
            if R / r'[Ee](xport)?' == s:
                print('export')
            elif R / r'[Dd](ate)?:\d{4}-\d{2}-\d{2}' == s:
                _, date = s.split(':')
                print('调整日期为：', date)
            elif R / r'\d{4}' == s:
                print('设置交易码成功：', s)
            elif R / r'[Uu](set)?:\d{4}' == s:
                _, jym = s.split(':')
                print('取消投产交易成功:', jym)
            elif R / r'[Ll](ist)?' == s:
                print('列表显示待投产交易')

    @classmethod
    def export_jymcs(cls):
        tcrq = tuple(
            cls.objects.filter(P.tcrq >= datetime.now() % '%F').order_by(
                P.tcrq).limit(1).scalar('tcrq'))
        if tcrq:
            tcrq = tcrq[0]
            print('当前投产日期：', tcrq)
            data = tuple(
                cls.objects.filter((P.tcrq == tcrq) & (P.lb == 0)).scalar(
                    cls._projects[1:26]))
            header = profile['header'][:25]
            JY_Headers = [Header(h, w) for h, w in zip(header, Widths)]
            hd_data = [[*row[:2], None, None, None] for row in data]
            jx_data = hd_data = [[*row[:2], None] for row in data]
            zsxs_data = [[*row[:2], 1] for row in data]
            jx_hj = [[
                *row[:2], 0, 0.63, 0.63, 0.5, 0.8, 0.8, 0.8, 0.55, 0.55, 0.55,
                0.5, 0.8, 0.4, 0.5, 0.75, 0.5, 0.5, 0.75, 0.63, 0.63, 0, 0.8,
                0.8, 0.5, 0, 0, 0, 0.1, 0.1, 0.67, 0.5, 1, 0.63, 0.63, 0.8, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0
            ] for row in jx_data]
            with (ROOT / f'交易码参数表{tcrq}.xlsx').write_xlsx(force=True) as book:
                book.add_table('A1', '新增交易码', data=data, columns=JY_Headers)
                book.add_table('A1', '事后监督参数', data=hd_data, columns=HD_Header)
                book.add_table('A1',
                               '绩效-系统交易码',
                               data=jx_data,
                               columns=JX_JYM_Headers)
                book.add_table('A1',
                               '绩效-机构交易折算系数',
                               data=zsxs_data,
                               columns=JX_ZSXS_Headers)
                book.add_table('A1',
                               '绩效-柜员交易折算系数',
                               data=zsxs_data,
                               columns=JX_ZSXS_Headers)
                book.add_table('A1',
                               '绩效-交易环节折算系数',
                               data=jx_hj,
                               columns=JX_HJ_Headers)
                print('导出交易码参数成功')

        else:
            print('无待投产内容')

    @classmethod
    def del__(cls, objs):
        for obj in objs:
            obj['cjsj'] = obj.get('cjsj', None) or now() % ('%Y-%m-%d')
            cls.objects.filter(P.jym == obj['jym']).upsert_one(
                cjsj=obj['cjsj'])

    @classmethod
    def insert__(cls, objs):
        for obj in objs:
            if JyJiaoyi.objects.filter(P._id == obj['jym']).count() > 0:
                print('交易 %s-%s 已存在，忽略' % (obj['jym'], obj['jymc']))
            else:
                obj['cjsj'] = obj['cjsj'] or now() % ('%Y-%m-%d')
                jym = obj.pop('jym')
                cls.objects.filter(P.jym == jym).upsert_one(**obj)

    @classmethod
    def modify__(cls, objs):
        pjs = 'jymc',  'jyz', 'yxj', 'wdsqjb', 'zxsqjb',\
            'bxwdsq', 'zxsqjg', 'bxzxsq', 'jnjb', 'xzbz', 'wb',\
            'dets', 'dzdk', 'sxf', 'htjc', 'jdfs', 'bssx', 'sc', 'mz', 'cesq', \
            'shbs', 'cdjy'
        for obj in objs:
            obj_ = JyJiaoyi.objects.filter(P._id == obj['jym']).first()
            if not obj_:
                print('交易 %s-%s 不存在，忽略' % (obj['jym'], obj['jymc']))
            else:
                obj['cjsj'] = obj.get('cjsj', None) or now() % ('%Y-%m-%d')
                jym = obj.pop('jym')
                for key in pjs:
                    val = getattr(obj_, key)
                    if isinstance(val, str):
                        val = val.strip()
                    if obj[key] == val:
                        obj.pop(key)
                if (not obj['fjjyz']) and (not obj_.fjjyz):
                    obj.pop('fjjyz')
                obj.pop('yjcd')
                obj.pop('ejcd')
                cls.objects.filter(P.jym == jym).upsert_one(**obj)

    @classmethod
    @arg('-u', '--update', action='store_true', help='更新参数表')
    @arg('-t', '--touchan', nargs='?', help='投产管理')
    @arg('-n', '--new', action='store_true', help='新增交易码')
    @arg('-d', '--delete', action='store_true', help='删除交易码')
    @arg('-m', '--modify', action='store_true', help='修改交易码')
    @arg('-e', '--export', action='store_true', help='导出交易参数')
    @arg('-v', '--valid', action='store_true', help='生效')
    def main(cls, **option):
        from gmongo.__version__ import version
        print('gmongo version:', version)
        if option['update']:
            cls.update_()
        if option['touchan']:
            cls.touchan(option['touchan'])
        if option['export']:
            cls.export_jymcs()
