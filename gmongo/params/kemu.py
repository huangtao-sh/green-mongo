# 项目：   工作平台
# 模块：   科目查询
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-10-31 09:43
# 修订：2019-10-31 11:22 修改

from gmongo.params import get_ver
from orange import R, arg
from orange.utils.sqlite import fetch, fetchone, fetchvalue, fprintf
from gmongo.params import get_param_ver
from gmongo.__version__ import version


def list_kemu(sql):
    for row in fetch(sql):
        print(*row, sep='\t')


def show_kemu(sql, arg=None):
    data = fetchone(sql, arg)
    if data:
        print('%s\t%s\n%s' % (data))
        return True


def khqk(km):
    print('\n已开账户情况')
    data = fetch('select distinct xh,hm from nbzhhz where km=? order by xh',
                 [km])
    for row in data:
        print(f'{km}-{row[0]:03d} {row[1]}')
    xh = min(set(range(1, len(data) + 2)) - set([x[0] for x in data]))
    print('\n最小未用序号：', xh)


def nbzhmb(km):
    print('\n内部账户模板')
    fprintf('{:2s}  {:10s}  {:6s}  {:2s}  {:3d}  {:50s}',
            'select jglx,whrq,km,bz,xh,hm from nbzhmb where km=?', [km])


@arg('query', help='查询科目信息')
def main(query):
    #ver = get_param_ver('kemu')[0]
    #print('程序版本：', version)
    print(f'数据版本：{get_ver("kemu")}')
    if R / r'\d{4}' == query:
        if show_kemu('select * from kemu where km=?', [query]):
            print('\n子科目列表')
            list_kemu(
                f'select km,name from kemu where km like "{query}__" order by km'
            )
    elif R / r'\d{6}' == query:
        if show_kemu('select * from kemu where km=?', [query]):
            khqk(query)
            nbzhmb(query)
    elif R / r'\d{1,5}' == query:
        list_kemu(f'select km,name from kemu where km like "{query}%"')
    else:
        list_kemu(f'select km,name from kemu where name like "%{query}%"')
