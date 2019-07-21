# 项目：   工作平台
# 模块：   内部账户
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-06-27 09:19

from orange import arg, command, R, tprint
from orange.utils.sqlite import db_config, fetch, fetchone, fetchvalue
from orange import now
from orange.utils.log import set_verbose, info

ZTZC = 'substr(zhzt,1,1)="0"'
YXH = 'substr(zhzt,1,1)="1"'
ZHXH = 'substr(zh,13,9) as zhxh'

db_config('params')

headers = '账号', '机构码', '币种', '户名', '科目', '余额方向', '余额', '切换额', '昨日余额', '正常利率', '罚息利率', '浮动系数',\
    '利息积数', '罚息积数', '起息日期', '开户日期', '销户日期', '上笔发生日期', '明细笔数', '账户状态',\
    '计息标志', '收息账号', '付息账号', '透支额度', "备注"

begin_date = f'{now().year - 2:04d}1231'
#print('开始日期：', begin_date)


@arg('-c', '--clear', action='store_true', help='生成清理内部户开立模板清单')
@arg('-e', '--export', action='store_true', help='生成清理账户文件')
@arg('ac', nargs='?', help='查询指定账户')
@arg('-t', '--tongji', nargs='?', dest='tac', metavar='ac', help='统计指定账户的情况')
@arg('-v', '--verbose', action='store_true', help='显示详情')
@arg('-E', '--exportall', action="store_true", help='导出全量模板')
def main(clear=False,
         export=False,
         ac=None,
         tac=None,
         verbose=False,
         exportall=False):
    if verbose:
        set_verbose()
    info(
        '参数文件版本：%s\n导入时间：%s',
        *fetchone('select period,time from param_period where name=?',
                  ['ggnbzhmb']))

    if clear:
        from .analysis import clear_nbzhmb
        clear_nbzhmb()
    if exportall:
        from .analysis import export_all
        export_all()
    if export:
        from .clearnbzh import clear_nbzh
        clear_nbzh(begin_date)
    if ac:
        if R / r'\d{9}' == ac:
            print(*headers, sep='\t')
            for row in fetch('select * from nbzh where substr(zh,13,9)=?',
                             [ac]):
                print(*row, sep='\t')
        elif R / r'\d{22}' == ac:
            data = fetchone('select * from nbzh where zh=?', [ac])
            if data:
                tprint(zip(headers, data), format_spec={0: '16'})
    if tac:
        if R / r'\d{9}' == tac:
            print('账号：', tac)
            print('机构类型    币种    最后发生日   最大余额', sep='\t')
            for row in fetch(
                    'select b.jglx,a.bz,max(a.sbfsr),max(a.ye) from nbzh a '
                    'left join ggjgm jg b '
                    'on a.jgm=b.jgm '
                    'where substr(zh,13,9)=? '
                    'group by b.jglx,a.bz ', [tac]):
                print(*row, sep='\t')
        else:
            print('账号的格式应为999999999')
