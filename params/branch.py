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
from glemon.document import enlist


class Branch(Document):
    _projects = enlist('br,order')
    load_options = {
        'header': {
            '分行名称': 'br',
            '顺序': ('order', int)
        }
    }

    @classmethod
    def procdata(cls, file, options):
        data = file.sheets('分行顺序表')
        return super().procdata(data, options)

    @classproperty
    def branchs(self):
        '''返回分行字典，其值为： 分行名称：顺序'''
        return dict(self.objects.scalar('br,order'))


class Contacts(Document):
    _projects = enlist('br,dept,name,title,tel,fax,mobile,email')
    load_options = {
        'header': {
            '机构': 'br',
            '部门': 'dept',
            '姓名': 'name',
            '职务（old）': 'title',
            '办公电话': 'tel',
            '传真': 'fax',
            '手机': 'mobile',
            '电子邮件': 'email',
        }
    }

    @classmethod
    def procdata(cls, file, options):
        data = file.sheets('通讯录')
        data = super().procdata(data, options)
        return data

    @classmethod
    def search(cls, query=None, yunying=False):
        if query is None:
            filter = None
        elif yunying:
            filter = P.sub_dept.startswith('运营')
            filter = filter & P.br.startswith(query)
            filter = filter & (
                (P.title.endswith('总经理') | (P.title == '主要负责人')))
            return ['{name:10}{title:10}{tel:20}{mobile}' .format(**obj) for obj in cls.find(filter)]
        else:
            if R / r'1[3578]\d{1,9}' == query:
                filter = P.mobile.startswith(query)
            elif R / r'9\d{3}' == query:
                filter = P.tel.endswith('8765' + query)
            elif R / r'\d{1,}' == query:
                filter = P.tel.contains(query)
            else:
                filter = P.name.contains(query)
            return cls.find(filter)

    @classmethod
    @arg('query', nargs="?", help='请输入查找条件')
    @arg('-y', '--yunying', action='store_true', help='运营部')
    def main(cls, query, yunying=False):
        if query:
            for obj in cls.search(query, yunying):
                print(obj)


if __name__ == '__main__':
    # from parameters.sjdr import sjdr
    # sjdr()
    print(Branch.branchs)
