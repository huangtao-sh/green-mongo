# 项目：数据库模型
# 模块：公共凭证种类表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-10-14 22:41

from glemon import Document, P


class Pzzl(Document):
    '''凭证种类表
字段名 字段属性 长度 空值标志 备注 包括中文注释和取值范围 
pzzl int N.N 凭证类别号 
kmkzz char 6 N.N 对应科目控制字 
pzmc char 20 凭证名称 
qyrq date 启用日期
zyrq date 止用日期
bzh char 2 币种
djje dec 16,2 单价金额/面额
sybz char 1 使用标志
1:柜员 
2:网点 
kzbz char 8 控制标志
第一位:重空标志
0:不控制号码 
1:控制号码 
第二位:顺序使用标志
0:不顺序使用
1:顺序使用
第三,四位:汇总类别
11:存折
12:存单
13:储蓄卡
14:信用卡
15:一本通
16:一卡通
21:现金支票
22:转帐支票
23:普通支票
24:带支付密码现金支票
25:带支付密码转帐支票
26:带支付密码普通支票
31:全国汇票
32:省辖汇票
33:市辖汇票
34:县辖汇票
35:全国联行汇票
36:区域联行汇票
41:不定额本票
42:定额本票
51:银行承兑汇票
52:商业承兑汇票
61:委托收款
62:托收承付
63:特种委托收款
71:债券
72:股票
73:股金证
79:其它有价单证
81:信用证
82:消费卡
83:IC卡
00:其它
第五位:出售标志
0:不可出售
1:可出售
2:密码支票
第六位:支付密码校验标志
0:不校验
1:校验
mbzs int N.N 每本张数 不按本为1 
hyhs int N.N 换页行数 无为0 
hbhs int N.N 换本行数 无为0 
'''
    _projects = 'pzzl', 'kmkzz', 'pymc', 'qyrq', 'zyrq', 'bzh', 'djje', 'sybz', 'kzbz',\
        'mbzs', 'hyhs', 'hbhs'


if __name__ == '__main__':
    from orange import Path
    from orange.coroutine import run
    run(Pzzl.load_files(Path(
        r'C:\Users\huangtao\OneDrive\工作\参数备份\运营管理2017-09\shendawei\凭证种类表ggpzzl.del')))
    for obj in Pzzl.objects.limit(10):
        print(obj.pzzl, obj.kmkzz, obj.pymc)
