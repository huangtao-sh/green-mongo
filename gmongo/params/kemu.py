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


@arg('query', help='查询科目信息')
def main(query):
    ver = get_param_ver('kemu')[0]
    print('程序版本：', version)
    print('数据版本：', ver, end='\n\n')
    if R / r'\d{6}' == query or R / r'\d{4}' == query:
        data = fetchone('select * from kemu where km=?', [query])
        if data:
            print('%s\t%s\n%s' % (data))
    elif R / r'\d{1,5}' == query:
        for r in fetch(f'select km,name from kemu where km like "{query}%"'):
            print(*r, sep='\t')
    else:
        for r in fetch(
                f'select km,name from kemu where name like "%{query}%"'):
            print(*r, sep='\t')
