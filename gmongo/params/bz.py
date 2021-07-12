# 项目：工作平台
# 模块：币种相关参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-06-23 09:43
# 修订：2018-10-27 采用 profile 来显示内容

from orange import command, arg, R, tprint
from orange.utils.sqlite import fetch, combine, fprintf
from gmongo.params import get_ver


def mapper(code):
    if R/r'\d{2}' == code:
        return f'bz="{code}"'
    elif R/'[a-zA-Z]{3}' == code:
        return f'ywsx="{code.upper()}"'
    else:
        return f'bzmc like "%{code}%"'


@command(description='币种代码查询程序')
@arg('codes', metavar='bz', nargs='*', help='币种代码列表')
@arg('-a', '--all', action='store_true', help='显示所有币种')
def main(**options):
    print(f'数据版本：{get_ver("bzb")}')
    print('代码  英文简称   币种名称')
    fmt = '{}     {:<3}       {}'
    if codes := options.get('codes'):
        fprintf(
            fmt, f'select bz,ywsx,bzmc from bzb where {combine(*codes, mapper=mapper)} order by bz')
    if options.get('all'):
        fprintf(fmt, 'select bz,ywsx,bzmc from bzb where qybz="1" order by bz')
