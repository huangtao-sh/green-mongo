# 项目：工作平台
# 模块：内部账户表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-10-14 11:28
# 修订：2017-12-18 修正导入文件的算法，以提高导入速度
# 修订：2018-09-06 修正内部账户导入问题
# 修订：2018-09007 由于性能问题，不再支持 aiofiles
# 修改：2018-09-12 15:13 调整打印格式
# 修改：2018-10-20 14:23 调整数据导入方式


from glemon import Document, P, Descriptor
from orange import R, arg, Path, tprint


class AcTemplate(Document):
    _projects = 'jglx', 'sxrq', 'km', 'bz', 'xh', 'hmgz', 'hm', 'tzed', 'cszt', 'jxbz'
    load_options = {
        'encoding': 'gbk',
        'errors': 'ignore',
        'converter': {
            'tzed': float,
            'jglx': str.strip,
        },
    }

    _profile = {
        '机构类型': 'jg',
        '生效日期': 'sxrq',
        '币种': 'bz',
        '科目': 'km',
        '序号': 'xh',
        '户名规则': 'hmgz_',
        '透支额度': 'tzed',
        '初始装态': 'cszt',
        '计息标志': 'jxbz'
    }
    jg = Descriptor('jglx', {
        '00': '总行清算中心',
        '01': '总行业务处理中心',
        '10': '分行业务处理中心',
        '11': '分行营业部',
        '12': '支行营业部'
    })
    hmgz_ = Descriptor('hmgz', {
        '1': '按科目名称',
        '2': '按账户名称'
    })

    @classmethod
    def search(cls, km):
        objs = cls.objects.filter(km=km).order_by(P.xh, P.jglx, P.bz)
        if objs:
            print('机构类型  生效日期  科目  币种     序号       户名  ')
            objs.show('jglx', 'sxrq', 'km', 'bz',
                      'xh', 'hm',
                      format_spec='^4,^10,^8,^6,>4,40'.split(','))


class GgKmzd(Document):
    _projects = 'kmh', 'hzkzz', 'kmkzz', 'kmmc', 'kmjb', 'jdbz', 'kmlx', 'bz'
    _textfmt = '''科目号：    {self.kmh}
汇总科目：  {self.hzkzz}
科目名称：  {self.kmmc}
科目级别：  {self.jb}
借贷标志：  {self.jd}
科目类型：  {self.lx}
标志：      {self.bz}'''
    jb = Descriptor('kmjb', {
        '0': '明细科目',
        '1': '一级科目',
        '2': '二级科目',
        '3': '三级科目'
    })
    jd = Descriptor('jdbz', {
        '0': '两性',
        '1': '借方',
        '2': '贷方',
        '3': '并列（借贷不轧差）'
    })
    lx = Descriptor('kmlx', {
        '0': '汇总科目（不开户）',
        '1': '单账户科目',
        '2': '多账户科目'
    })

    @classmethod
    def search(cls, item):
        obj = cls.objects.filter(kmh=item).first()
        if obj:
            print(obj)


class ZhangHu(Document):
    _projects = '_id', 'name'
    load_options = {
        'encoding':     'gbk',
        'errors':       'ignore',
    }

    @classmethod
    def procdata(cls, data, options):
        datas = set()

        def _(row):
            ac = row[0][12:20]
            if ac not in datas:
                datas.add(ac)
                return (ac, row[3].strip())
        return filter(None,map(_,data)))

    @classmethod
    def show(cls, ac):
        objects = cls.find(P._id.startswith(ac)).order_by(P._id)
        if objects.count() > 0:
            print('已开账户情况：')
            wy = None
            for i, obj in enumerate(objects, 1):
                xh = obj._id[6:]
                if not wy and i != int(xh):
                    wy = i
                print('%s-%s    %s' % (obj._id[:6], xh, obj.name))
            if not wy:
                wy = int(xh) + 1
            print('最小未用账户序号：%03d' % (wy))
        else:
            print('尚未开立账户')


@arg('ac', nargs='?', help='账户，格式应为：999999')
def main(ac=None):
    if ac:
        if R / r'\d{6}' == ac:
            from .accounting import Accounting
            q = Accounting.search(query=ac).first()
            if q:
                print('科目信息：%s\n' % (q))
            ZhangHu.show(ac)
            print('\n科目属性')
            print('-'*20)
            GgKmzd.search(ac)
            print('\n内部账户开立模板')
            print('-'*20)
            AcTemplate.search(ac)

        elif R/r'\d{6}\-\d{1,3}':
            km, xh = ac.split('-')
            objects = AcTemplate.objects.filter(
                km=km, xh=xh).order_by(P.jglx, P.bz)
            for obj in objects:
                obj.show()
                print('\n')
