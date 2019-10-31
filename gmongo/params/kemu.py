# 项目：   工作平台
# 模块：   科目查询
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-10-31 09:43

from orange import R, arg
from orange.utils.sqlite import fetch, fetchone
from gmongo.params import get_param_ver
from gmongo.__version__ import version


def list_kemu(sql):
    print(*fetch(sql), sep='\t')


def show_kemu(sql, arg=None):
    data = fetchone(sql, arg)
    if data:
        print('%s\t%s\n%s' % (data))
        return True


@arg('query', help='查询科目信息')
def main(query):
    ver = get_param_ver('kemu')[0]
    print('程序版本：', version)
    print('数据版本：', ver, end='\n\n')
    if R / r'\d{4}' == query:
        if show_kemu('select * from kemu where km=?', [query]):
            print('\n子科目列表')
            list_kemu(
                f'select km,name from kemu where km like "{query}__" order by km'
            )
    elif R / r'\d{6}' == query:
        if show_kemu('select * from kemu where km=?', [query]):
            ...
    elif R / r'\d{1,5}' == query:
        list_kemu(f'select km,name from kemu where km like "{query}%"')
    else:
        list_kemu(f'select km,name from kemu where name like "%{query}%"')
