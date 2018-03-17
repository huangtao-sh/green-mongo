# 项目：数据库模型
# 模块：内部账户表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-03-07 14:11

from orange import *
from imongo import *
from collections import defaultdict

RootPath = r'~/Documents/工作/参数备份'


class _TemplateData(EmbeddedDocument):
    br = StringField()
    qyrq = LongField()
    bz = StringField()
    hmgz = StringField()
    hm = StringField()
    tzed = FloatField()
    cszt = StringField()
    jxbz = StringField()


class AcTemplate(Document):
    ac = StringField()
    data = ListField(EmbeddedDocumentField(_TemplateData))

    @classmethod
    def load_files(cls, path=None):
        root = Path(path or RootPath)
        filename = max(root.rglob('ggnbzhmb.del'))
        if filename.exists():
            data = defaultdict(lambda: [])
            print('开始打开文件 %s 成功！' % (filename))
            with open(str(filename), 'rb')as fn:
                d = fn.read().splitlines()
            print('读取数据完成')
            for row in d:
                x = row.split(b',')
                ac = '%s%03d' % (dco(x[2]), int(x[4].decode()))
                data[ac].append(_TemplateData(br=dco(x[0]),
                                              qyrq=x[1].decode(),
                                              bz=dco(x[3]),
                                              hmgz=dco(x[5]),
                                              hm=dco(x[6]),
                                              tzed=float(x[7].decode()),
                                              cszt=dco(x[8]),
                                              jxbz=dco(x[9])))
            cls.drop_collection()
            for k, v in data.items():
                cls(ac=k, data=v).save()
            print('导入账户模板数据完成!\n共导入 %d 条数据。' % (len(data)))


def dco(by):
    by = by[1:-1]
    try:
        return by.decode('gbk')
    except:
        s = []
        i, l = 0, len(by)
        while i < l:
            if by[i] < 127:
                s.append(chr(by[i]))
                i += 1
            else:
                try:
                    s.append(by[i:i+2].decode('gbk'))
                    i += 2
                except:
                    i += 1
        return ''.join(s)


class _Data(EmbeddedDocument):
    ac = StringField()
    hm = StringField()


class ZhangHu(Document):
    ac = StringField()
    data = ListField(EmbeddedDocumentField(_Data))

    @classmethod
    def load_files(cls, path=None):
        root = Path(path or RootPath)
        filename = max(root.rglob('fhnbhzz.del'))
        if filename.exists():
            data = defaultdict(lambda: [])
            print('打开文件 %s 成功！' % (filename))
            with open(str(filename), 'rb')as fn:
                d = fn.read().splitlines()
            print('读取数据完成')
            for row in d:
                x = row.split(b',')
                ac = dco(x[0])
                hm = dco(x[3]).rstrip()
                aac = ac[12:21]
                data[aac].append(_Data(ac=ac, hm=hm))
            print('解析数据完成')
            cls.drop_collection()
            for k, v in data.items():
                cls(ac=k, data=v).save()
            print('导入数据完成!\n共导入 %d 条数据。' % (len(data)))

    @classmethod
    def search(cls, ac):
        if '-' in ac:
            km, xh = ac.split('-')
            ensure(R/r'\d{6}'/km, '科目格式不正确')
            ac = '%s%03d' % (km, int(xh))
        if R/r'\d{9}'/ac:
            k = cls.objects(ac=ac).first()
            if k:
                print('已开立账户情况')
                print('  机构   币种        账号                户名')
                for d in k.data:
                    ac_ = d.ac
                    print(ac_[:9], ac_[9:11], ac_, d.hm)
            k = AcTemplate.objects(ac=ac).first()
            if k:
                print('\n现存账户模板')
                print('机构类型  币种   户名')
                for d in k.data:
                    print(d.br, d.bz, d.hm)

        else:
            print('账户的格式不正确，应为：999999999')

    @classmethod
    @arg('ac', nargs='?', help='账户，格式应为：999999999或：999999-9')
    @arg('-i', '--import', nargs='?', dest='root', default='NOSET', help='导入文件')
    def main(cls, ac=None, root='NOSET'):
        if root != 'NOSET':
            cls.load_files(root)
            AcTemplate.load_files(root)
        if ac:
            cls.search(ac)


if __name__ == '__main__':
    ZhangHu.main()
