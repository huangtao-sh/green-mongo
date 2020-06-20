# 项目：   工作平台
# 模块：   账户信息编码
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2018-11-23 10:13
# 修订：2020-06-20 09:15 调整为使用 sqlite 数据库

from orange import HOME, R, tprint, arg
from orange.utils.sqlite import fprintf, fprint, fetch
from gmongo.params import get_ver
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


@arg('km', nargs='?', help='查询科目对应的信息编码')
@arg('-l', '--list', dest='list_', action='store_true', help='列出所有的科目清单')
def main(km=None, list_=False):
    print(f'数据版本：{get_ver("xxbm")}')
    if km:
        for kemu, bm, name in fetch("select km,bm,name from xxbm where km=?", [km]):
            print(f'\n{kemu}     {name}')
            print(f'编码       {bm}')
            tprint(
                zip(names.split(','), split(bm)),
                format_spec={0: '10'})
    if list_:
        fprintf("{:6s}  {:40s}  {:50s}", "select km,bm,name from xxbm")
