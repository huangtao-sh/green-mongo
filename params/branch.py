# 项目：数据库
# 模块：机构代码
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-09-11 22:05
# 修订：2018-01-19 重新构造代码

from orange import Path, R, classproperty, arg
from orange.coroutine import run
from glemon import Document, P


class Branch(Document):
    _projects = 'tp', 'order', 'br', 'name', 'fax', 'tel', 'addr', 'zipcode'
    # tp 00-总行 10-分行 12-支行

    @classproperty
    def branchs(self):
        '''返回分行字典，其值为： 分行名称：顺序'''
        return {obj.br: obj.order for obj in self.objects(P.tp == '10')}

    @classmethod
    async def amport_file(cls, filename, drop=True, **kw):
        if drop:
            cls.drop()
            Contacts.drop()
        cls._dupcheck(filename)
        await super().amport_file(filename, **kw)
        cls._importsave(filename)
        print('导入文件 %s 成功' % (filename))

    @classmethod
    def _proc_sheet(cls, index, name, data, **kw):
        if name == '全行通讯录':
            for i, row in enumerate(data):
                if row[0] == '总行':
                    break
            data_ = []
            order = 0
            br = ''
            flag = True
            for row in data[i:]:
                if row[0] and (not row[0].startswith('注：')):
                    if flag:
                        br = row[0]
                        if br.endswith('总行'):
                            tp = '00'
                        else:
                            tp = '10'
                        flag = False
                    else:
                        tp = '12'
                    a = [tp, order, br]
                    a.extend(row)
                    data_.append(a)
                    order += 1
                else:
                    flag = True
            return cls, data_
        else:
            for row in data:
                if row[0]:
                    br = row[0]
                else:
                    row[0] = br
                if row[1]:
                    dept = row[1]
                else:
                    row[1] = dept
                if row[2]:
                    sub_dept = row[2]
                else:
                    row[2] = sub_dept
            return Contacts, data


class Contacts(Document):
    _projects = 'br', 'dept', 'sub_dept', 'name', 'title', 'tel', 'mobile', 'fax'
    _load_mapper = {
        'br': '机构名称',
        'dept': '部门',
        'sub_dept': '中心',
        'name': '姓名',
        'title': '职务',
        'tel': '办公电话',
        'mobile': '手机',
        'fax': '传真'}

    _textfmt = '''
机构：    {self.br}
部门：    {self.dept}{self.sub_dept}
姓名：    {self.name}   {self.title}
电话：    {self.tel}
手机：    {self.mobile}'''

    @classmethod
    def search(cls, query=None, yunying=False):
        if query is None:
            filter = None
        elif yunying:
            filter = P.sub_dept.startswith('运营')
            filter = filter & P.br.startswith(query)
            filter = filter & (
                (P.title.endswith('总经理') | (P.title == '主要负责人')))
            return ['{name:10}{title:10}{tel:20}{mobile}' .format(**obj) for obj in cls.objects(filter)]
        else:
            if R / r'1[3578]\d{1,9}' == query:
                filter = P.mobile.startswith(query)
            elif R / r'9\d{3}' == query:
                filter = P.tel.endswith('8765' + query)
            elif R / r'\d{1,}' == query:
                filter = P.tel.contains(query)
            else:
                filter = P.name.contains(query)
            return cls.objects(filter)

    @classmethod
    @arg('query', nargs="?", help='请输入查找条件')
    @arg('-l', '--list', dest='list_', action='store_true', help='列出分行')
    @arg('-y', '--yunying', action='store_true', help='运营部')
    def main(cls, query, list_=False, yunying=False):
        if query:
            for obj in cls.search(query, yunying):
                print(obj)
        if list_:
            d = Branch.branchs
            for obj in sorted(d.items(), key=lambda x: x[1]):
                print('%s\t%s' % (obj[1], obj[0]))
            print('%d branchs listed.' % (len(d)))


if __name__ == '__main__':
    # from parameters.sjdr import sjdr
    # sjdr()
    print(Branch.branchs)
