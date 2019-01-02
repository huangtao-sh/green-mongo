# 项目：工作平台
# 模块：交易码参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-29 15:18
# 修订：2019-01-02 20:42 新增命令行处理模块

from orange import Path, R, now, arg
from glemon import Document, P
from trans.jy import JyJiaoyi, FORMAT

path = Path('~/Documents/工作/工作档案/运营参数维护/交易码表/交易码参数表.xlsx')
LEIBIE = {'新增': 0, '修订': 1, '删除': 2}
JYFORMAT = FORMAT.copy()
JYFORMAT.extend([{'header': '创建日期', 'width': 8.43},
                 {'header': '投产时间', 'width': 8.43},
                 {'header': '备注', 'width': 60}
                 ])

JYSX = {
    'jymc':     '交易名称',
    'jym':      '交易码',
    'jyz':      '交易组',
    'yxj':      '优先级',
    'wdsqjb':   '网点授权级别',
    'zssqjb':   '中心授权级别',
    'wdsq':     '网点授权',
    'zssq':     '中心授权',
    'zssqjg':   '中心授权机构',
    'jnjb':     '技能级别',
    'xzbz':     '现转标志',
    'wb':       '外包',
    'dets':     '大额提示',
    'dzdk':     '电子底卡',
    'szjd':     '事中监督',
    'bssx':     '补扫时限',
    'mz':       '抹账',
    'cesq':     '超额授权',
    'fzjyz':    '辅助交易组',
    'shbs':     '事后补扫',
    'cdjy':     '磁道校验',
    'cd':       '菜单',
}


@arg('-u', '--update', action='store_true', help='更新参数表')
@arg('-n', '--new', action='store_true', help='新增交易码')
@arg('-d', '--delete', action='store_true', help='删除交易码')
@arg('-m', '--modify', action='store_true', help='修改交易码')
@arg('-e', '--export', action='store_true', help='导出交易参数')
@arg('-v', '--valid', action='store_true', help='生效')
def main(**kw):
    print(kw)


class PmJiaoyi(Document):
    # 类别：0-新增，1-修改，2-删除
    # 交易码，交易名称，交易组，优先级，网点授权级别，中心授权级别，网点授权标志，中心授权机构，中心授权标志，
    # 技能级别，现转标志，外包，大额提示，电子底卡，手续费，后台监测，事中扫描，补扫时限，审查，抹账，
    # 辅助交易组，事后补扫，磁道校验，一级菜单，二级菜单，建立时间，投产时间
    _projects = 'lb', 'jymc', 'jym', 'jyz', 'yxj', 'wdsqjb', 'zxsqjb',\
        'bxwdsq', 'zxsqjg', 'bxzxsq', 'jnjb', 'xzbz', 'wb',\
        'dets', 'dzdk', 'sxf', 'htjc', 'jdfs', 'bssx', 'sc', 'mz', 'cesq', 'fjjyz',\
        'shbs', 'cdjy', 'yjcd', 'ejcd', 'cjsj', 'tcsj', 'bz'

    @classmethod
    def import_file(cls):
        for idx, name, rows in path.iter_sheets():
            lb = LEIBIE.get(name, None)
            if lb is None:
                continue
            data = []
            for row in rows[1:]:
                if row[0]:
                    row.pop(3)
                    row.insert(0, lb)
                    obj = dict(zip(cls._projects, row))
                    data.append(obj)
                    if isinstance(obj['jym'], (int, float)):
                        obj['jym'] = '%04d' % (obj['jym'])
                    for name in ('yxj', 'jnjb'):
                        if isinstance(obj[name], (int, float)):
                            obj[name] = '%02d' % (obj[name])
                        else:
                            obj[name] = obj[name].strip()
                    for name in ('bxwdsq', 'bxzxsq', 'cesq', 'shbs', 'cdjy'):
                        val = obj[name]
                        if val == 1 or val == 'TRUE':
                            val = 'TRUE'
                        else:
                            val = 'FALSE'
                        obj[name] = val
            if lb == 0:
                cls.insert__(data)
            elif lb == 1:
                cls.modify__(data)
            elif lb == 2:
                cls.del__(data)

    @classmethod
    def export(cls):
        # for obj in cls.objects((P.tcsj==None)or(P.tcsj>)
        pass

    @classmethod
    def del__(cls, objs):
        for obj in objs:
            obj['cjsj'] = obj.get('cjsj', None) or now() % ('%Y-%m-%d')
            cls.objects(P.jym == obj['jym']).upsert_one(cjsj=obj['cjsj'])

    @classmethod
    def insert__(cls, objs):
        for obj in objs:
            if JyJiaoyi.objects(P._id == obj['jym']).count() > 0:
                print('交易 %s-%s 已存在，忽略' % (obj['jym'], obj['jymc']))
            else:
                obj['cjsj'] = obj['cjsj']or now() % ('%Y-%m-%d')
                jym = obj.pop('jym')
                cls.objects(P.jym == jym).upsert_one(**obj)

    @classmethod
    def modify__(cls, objs):
        pjs = 'jymc',  'jyz', 'yxj', 'wdsqjb', 'zxsqjb',\
            'bxwdsq', 'zxsqjg', 'bxzxsq', 'jnjb', 'xzbz', 'wb',\
            'dets', 'dzdk', 'sxf', 'htjc', 'jdfs', 'bssx', 'sc', 'mz', 'cesq', \
            'shbs', 'cdjy'
        for obj in objs:
            obj_ = JyJiaoyi.objects(P._id == obj['jym']).first()
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
                if (not obj['fjjyz'])and (not obj_.fjjyz):
                    obj.pop('fjjyz')
                obj.pop('yjcd')
                obj.pop('ejcd')
                cls.objects(P.jym == jym).upsert_one(**obj)


if __name__ == '__main__':
    # from params.sjdr import sjdr
    # sjdr()
    PmJiaoyi.import_file()
