# 项目：   工作平台
# 模块：   账户信息编码
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2018-11-23 10:13

from orange import HOME, R, tprint, arg
from glemon import Document, P
LENGTH = 3, 2, 1, 1, 2, 2, 2, 2, 4
names = "存款种类,存款属性,期限标志,存款性质,帐户类型,期限码,币种号,产权性质,行业归类"


def split(s):
    for l in LENGTH:
        r = s[:l]
        flag = '}' if '{' in r else ')' if '(' in r else None
        if flag:
            l += s.find(flag)-s.find('/')+2
        yield s[:l]
        s = s[l:]


class Zhxxbm(Document):
    _projects = 'bm', 'name', 'kemu'
    load_options = {
        'mapper': {
            'bm': 0,
            'name': 1,
            'kemu': 2
        }
    }

    @classmethod
    @arg('km', nargs='?', help='查询科目对应的信息编码')
    @arg('-l', '--list', dest='list_', action='store_true', help='列出所有的科目清单')
    def main(cls, km=None, list_=False):
        if km:
            for obj in cls.find(kemu=km):
                print(f'\n{obj.kemu}     {obj.name}')
                print(f'编码       {obj.bm}')
                tprint(
                    zip(names.split(','), split(obj.bm)),
                    format_spec={0: '10'})
        if list_:
            for km, name in cls.objects.order_by('kemu').scalar('kemu,name'):
                print(km, name)
