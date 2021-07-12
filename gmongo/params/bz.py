# 项目：工作平台
# 模块：币种相关参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-06-23 09:43
# 修订：2018-10-27 采用 profile 来显示内容

from orange import command, arg, R
from orange.utils.sqlite import fprintf


@command(description='币种代码查询程序')
@arg('codes', metavar='bz', nargs='*', help='币种代码列表')
@arg('-a', '--all', action='store_true', help='显示所有币种')
def main(**options):
    if codes := options.get('codes'):
        print('代码  英文简称   币种名称')
        fmt = '{}     {}       {}'
        for code in codes:
            if R/r'\d{2}' == code:
                fprintf(fmt, 'select bz,ywsx,bzmc from bzb where bz=?', [code])
            elif R/'[a-zA-Z]{3}' == code:
                fprintf(fmt, 'select bz,ywsx,bzmc from bzb where ywsx=?', [
                        code.upper()])
            else:
                fprintf(fmt, 'select bz,ywsx,bzmc from bzb where bzmc like ?', [
                        f'%{code}%'])
    if options.get('all'):
        print('代码  英文简称   币种名称')
        fmt = '{}     {:3}       {}'
        fprintf(fmt, 'select bz,ywsx,bzmc from bzb where qybz="1" order by bz')
        
 