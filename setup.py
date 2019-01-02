#!/usr/bin/env python3
#  项目：生产管理平台
#  作者：黄涛
#  创建：2018-3-15
#  修改：2018-05-25 20:50 删除lzwt


from orange import setup

consoles = [
    'jym=trans:JyJiaoyi.main',               # 交易码表
    'jycs=trans.jycs:main',                  # 交易码参数
    'sjdr=params.sjdr:sjdr',                 # 数据导入
    'jgm=params.jgm:GgJgm.main',             # 机构码表
    'ac=params.zh:main',                     # 内部账户
    'km=params.accounting:Accounting.run',   # 科目表
    'fhlz=lvzhi.fhlz:main',                  # 分行运营主管履职报告
    'lz=lvzhi:main',                         # 营业主管履职报告
    # 'jqb=vacation:Vacation.main',
    'lxr=params.branch:Contacts.main',       # 查询联系人
    'teller=params.user:Teller.main',        # 柜员表
    'bz=params.bz:GgBzb.main',               # 币种
    'ed=params.dengji:EduDengji.main',       # 额度配置
    'jq=vacation:Holiday.main',              # 假期表
    'wh=params.paijia:PaiJia.main',          # 外汇
    'xxbm=params.zhxxbm:Zhxxbm.main',        # 性质编码
]

setup(
    name='gmongo',
    author='huangtao',
    author_email='hunto@163.com',
    platforms='any',
    description='work platform',
    long_description='work platform',
    cscripts=consoles,
    url='https://github.com/huangtao-sh/mongo.git',
    license='GPL',
)
