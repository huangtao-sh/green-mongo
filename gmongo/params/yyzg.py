# 项目：   参数管理程序
# 模块：   营业主管查询模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-07-12 22:22

from orange import arg, command, R
from orange.utils.sqlite import fprintf, combine
from gmongo.params import get_ver


def mapper(q):
    if R/r'\d{4,9}' == q:
        return f'jg like "{q}%"'
    else:
        return f'xm like "{q}%" or jgmc like "%{q}%"'


@command(description='营业主管查询模块')
@arg('-t', '--type', nargs='?', help='指定主管类型')
@arg('query', nargs='*', help='查询条件')
def main(**options):
    query = []
    if typ := options.get('type'):
        query.append(f'js like "{typ}%"')
    if qrs := options.get('query'):
        query.append(combine(*qrs, mapper=mapper))
    q = combine(*query, mapper=lambda x: f'({x})', oper='and')
    print(f'数据版本：{get_ver("yyzg")}')
    print("工号   姓名       角色            联系电话           手机         机构")
    fprintf("{:<6} {:<10} {:15} {:<15} {:11}   {:<30}",
            f"select ygh,xm,js,lxdh,mobile,jgmc from yyzg where {q} order by jg,js")
