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


from glemon import Document, P
from orange import R, arg, Path, tprint


class AcTemplate(Document):
    _projects = 'jglx', 'sxrq', 'km', 'bz', 'xh', 'hmgz', 'hm', 'tzed', 'cszt', 'jxbz'
    load_options = {
        'encoding': 'gbk',
        'errors': 'ignore',
        'converter': {
            'tzed': float,
        },
    }
    _textfmt = '''机构类型：  {self.jglx}
生效日期：  {self.sxrq} 
科目：      {self.km}
币种：      {self.bz}
序号：      {self.xh}
户名规则：  {self.hmgz}
户名：      {self.hm}
透支额度：  {self.tzed}
初始状态：  {self.cszt}
计息标志：  {self.jxbz}'''

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

    @property
    def jb(self):
        return {
            '0': '明细科目',
            '1': '一级科目',
            '2': '二级科目',
            '3': '三级科目'}.get(self.kmjb, None)

    @property
    def jd(self):
        return {
            '0': '两性',
            '1': '借方',
            '2': '贷方',
            '3': '并列（借贷不轧差）'}.get(self.jdbz, None)

    @property
    def lx(self):
        return {
            '0': '汇总科目（不开户）',
            '1': '单账户科目',
            '2': '多账户科目'}.get(self.kmlx, None)

    @classmethod
    def search(cls, item):
        obj = cls.objects.filter(kmh=item).first()
        if obj:
            print(obj)


class ZhangHu(Document):
    _projects = '_id', 'name'
    load_options = {
        'encoding': 'gbk',
        'errors': 'ignore',
        'fields': "_id,,,name",
        'converter': {
            '_id': lambda x: x[13:22],
            'name': str.strip,
        }
    }

    @classmethod
    def show(cls, ac):
        objects = cls.objects.filter(P._id.startswith(ac)).order_by(P._id)
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

    @classmethod
    def proctxt(cls, file):
        datas = set()
        data = []
        with file.open('rb')as f:
            for row in f:
                s = row.split(b',')
                ac = s[0].decode()[13:22]
                if ac not in datas:
                    datas.add(ac)
                    name = s[3].decode('gbk', 'ignore')[1:-1].strip()
                    data.append((ac, name))
        [print(row)for row in data]
        return data

    @classmethod
    def import_file(cls, filename, drop=True, dupcheck=True):
        dupcheck and cls._dupcheck(filename)
        with open(str(filename), 'rb')as f:
            cls.drop()
            datas = set()
            data = []
            for row in f:
                s = row.split(b',')
                ac = s[0].decode()[13:22]
                if ac not in datas:
                    datas.add(ac)
                    name = s[3].decode('gbk', 'ignore')[1:-1].strip()
                    data.append((ac, name))
            cls._load_data(data=data, drop=True)
            dupcheck and cls._importsave(filename)
            print('文件 %s 已导入' % (filename))


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
            objects = AcTemplate.objects.filter(km=km, xh=int(xh))
            objects.show('jglx', 'km', 'xh', 'bz', 'sxrq', 'tzed', 'hm',
                         format_spec={5: '17.2f'})
