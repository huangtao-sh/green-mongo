#!/usr/bin/env python3
#  项目：生产管理平台
#  作者：黄涛
#  创建：2018-3-15
#  修改：2018-05-25 20:50 删除lzwt


from orange import setup

consoles = [
    'jym=trans:JyJiaoyi.main',
    'sjdr=params.sjdr:sjdr',
    'jgm=params.jgm:GgJgm.main',
    'ac=params.zh:main',
    'km=params.accounting:Accounting.run',
    'fhlz=lvzhi.fhlz:main',                  # 分行运营主管履职报告
    'lz=lvzhi:main',                         # 营业主管履职报告
    # 'jqb=vacation:Vacation.main',
    'lxr=params.branch:Contacts.main',       # 查询联系人
    'teller=params.user:Teller.main',
    'bz=params.bz:GgBzb.main',
    'ed=params.dengji:EduDengji.main',
    'jq=vacation:Holiday.main',
    'wh=params.paijia:PaiJia.main',
    'xxbm=params.zhxxbm:Zhxxbm.main',
]
guis = []

setup(
    name='gmongo',
    author='huangtao',
    author_email='hunto@163.com',
    platforms='any',
    description='work platform',
    long_description='work platform',
    entry_points={
        'gui_scripts': guis,
        'console_scripts': consoles},
    url='https://github.com/huangtao-sh/mongo.git',
    license='GPL',
)
