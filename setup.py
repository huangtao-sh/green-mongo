#!/usr/bin/env python3
#  项目：生产管理平台
#  作者：黄涛
#  创建：2018-3-15
#  修改：2018-05-25 20:50 删除lzwt
#  修改：2021-06-19 采用 setuptools 导入工具

from setuptools import setup, find_packages
from gmongo.__version__ import version
from pathlib import Path


def read_requires():
    path = Path('requirements.txt')
    if path.exists():
        requires = [x for x in path.read_text().splitlines() if x.strip()
                    and not x.startswith('#')]
        return requires


consoles = [
    'lxr=gmongo.params.txl:main',  # 查找联系人
    'bz=params.bz:GgBzb.main',  # 币种
    'jqb=gmongo.jqb:main',  # 假期表参数
    'wh=params.paijia:PaiJia.main',  # 外汇
    'xxbm=gmongo.params.zhxxbm:main',  # 性质编码
    # 'zfbb=gmongo.zfbb:main',  # 支付报表
    'lzbg=gmongo.lzbg:lzbg',  # 营业主管履职报告
    'fhlz=gmongo.lzbg:fhlz',  # 分行运营主管履职报告'
    'nbzh=gmongo.nbzh:main',  # 内部账户
    'tlr=gmongo.params.teller:main',  # 柜员表
    'lzwt=gmongo.lzwt:main',  # 履职问题
    'pa=gmongo.params.pa:main'  # 参数管理主程序
]

setup(
    name='gmongo',
    version=version,
    packages=find_packages(exclude=['testing']),
    package_data={
        '': ['sql/*.sql'],
    },
    install_requires=read_requires(),
    author='huangtao',
    author_email='hunto@163.com',
    description='work platform',
    long_description='work platform',
    entry_points={
        'console_scripts': consoles,
    },
    url='https://github.com/huangtao-sh/mongo.git',
    license='GPL',
)
