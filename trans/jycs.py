# 项目：工作平台
# 模块：交易码参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-29 15:18
# 修订：2019-01-02 20:42 新增命令行处理模块
# 修订：2019-12-01 11:58 新增相关功能

from orange import Path, R, now, arg, HOME, Data, datetime, R
from glemon import Document, P, Shadow
from trans.jy import JyJiaoyi, FORMAT
from orange.xlsx import Header

profile = Shadow.read('jycs') or {}


def save_profile():
    Shadow.write('jycs', profile)


ROOT = HOME / 'OneDrive/工作/参数备份/生产参数'

path = ROOT / '交易码参数.xlsx'


def itos(length=4):
    def _(s):
        return f'%0{length}d' % (int(s))

    return _


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


@arg('-u', '--update', action='store_true', help='更新参数表')
@arg('-t', '--touchan', nargs='?', help='投产管理')
@arg('-n', '--new', action='store_true', help='新增交易码')
@arg('-d', '--delete', action='store_true', help='删除交易码')
@arg('-m', '--modify', action='store_true', help='修改交易码')
@arg('-e', '--export', action='store_true', help='导出交易参数')
@arg('-v', '--valid', action='store_true', help='生效')
def main(**option):
    if option['update']:
        PmJiaoyi.update_()
    if option['touchan']:
        PmJiaoyi.touchan(option['touchan'])


def confirm(prompt):
    s = input(prompt, ',请确认? Yes or No')
    return s in ('Y', 'y', 'yes', 'Yes')


class PmJiaoyi(Document):
    # 类别：0-新增，1-修改，2-删除
    # 交易码，交易名称，交易组，优先级，网点授权级别，中心授权级别，网点授权标志，中心授权机构，中心授权标志，
    # 技能级别，现转标志，外包，大额提示，电子底卡，手续费，后台监测，事中扫描，补扫时限，审查，抹账，
    # 辅助交易组，事后补扫，磁道校验，一级菜单，二级菜单，建立时间，投产时间
    _projects = 'lb', 'jymc', 'jym', 'jyz','jyzm', 'yxj', 'wdsqjb', 'zxsqjb',\
        'bxwdsq', 'zxsqjg', 'bxzxsq', 'jnjb', 'xzbz', 'wb',\
        'dets', 'dzdk', 'sxf', 'htjc', 'jdfs', 'bssx', 'sc', 'mz', 'cesq', 'fjjyz',\
        'shbs', 'cdjy', 'yjcd', 'ejcd', 'tcrq','cjsj', 'tcsj', 'bz'

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
        if (not profile.get('header') and len(header) == 29) or True:  # 保存文件头
            profile['header'] = header
            save_profile()
            print('保存表头成功！')
        for row in Data(data[1:],
                        filter=lambda row: bool(row[2]),
                        converter={
                            2: itos(4),
                            5: itos(2),
                            6: itos(1),
                            7: itos(1),
                            8: bool_,
                            9: itos(1),
                            10: bool_,
                            11: itos(2),
                            13: itos(1),
                            14: itos(1),
                            15: itos(1),
                            16: itos(1),
                            17: itos(1),
                            18: itos(1),
                            19: itos(1),
                            20: itos(1),
                            21: itos(1),
                            22: bool_,
                            24: bool_,
                            25: bool_,
                        }):
            _id = row[0]
            row[0] = 0
            obj = dict(zip(cls._projects, row))
            if JyJiaoyi.objects.get(row[2]):
                cls.objects.filter((P.jym == row[2])
                                   & (P.lb == 0)).update_one(ytc=True)
                print(f'交易码： {row[2]} 已投产，忽略')
            elif _id:
                cls.objects.filter(P._id == _id).upsert_one(**obj)
            else:
                cls(obj).save()
        print('导入文件成功！')

    @classmethod
    def dump(cls):
        data=cls.objects.filter((P.lb==0) ).scalar('_id','jymc', 'jym', 'jyz','jyzm', 'yxj', 'wdsqjb', 'zxsqjb',\
        'bxwdsq', 'zxsqjg', 'bxzxsq', 'jnjb', 'xzbz', 'wb',\
        'dets', 'dzdk', 'sxf', 'htjc', 'jdfs', 'bssx', 'sc', 'mz', 'cesq', 'fjjyz',\
        'shbs', 'cdjy', 'yjcd', 'ejcd','cjrq','bz','bz','cjrq','tcrq')
        header = profile['header']
        widths = [
            0.01, 40, 9, 9, 27, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
            9, 9, 9, 9, 9, 17, 21, 17, 20, 15, 15
        ]
        Headers = [Header(h, w) for h, w in zip(header, widths)]
        data = map(lambda x: [str(x[0]), *x[1:]], data)
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
    def export(cls):
        # for obj in cls.objects((P.tcsj==None)or(P.tcsj>)
        pass

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
