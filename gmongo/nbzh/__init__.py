# 项目：   工作平台
# 模块：   内部账户
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-06-27 09:19

from orange import arg, command, R, tprint
from orange.utils.sqlite import db_config, fetch, fetchone

ZTZC = 'substr(zhzt,1,1)="0"'
YXH = 'substr(zhzt,1,1)="1"'
ZHXH = 'substr(zh,13,9) as zhxh'

db_config('params')

headers='账号','机构码','币种','户名','科目','余额方向','余额','切换额','昨日余额','正常利率','罚息利率','浮动系数',\
    '利息积数','罚息积数','起息日期','开户日期','销户日期','上笔发生日期','明细笔数','账户状态',\
        '计息标志','收息账号','付息账号','透支额度',"备注"


@arg('-c', '--clear', action='store_true', help='生成清理内部户开立模板清单')
@arg('ac', nargs='?', help='查询指定账户')
def main(clear=False, ac=None):
    if clear:
        from .analysis import clear_nbzhmb
        clear_nbzhmb()
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
