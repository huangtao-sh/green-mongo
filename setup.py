#!/usr/bin/env python3
#  项目：生产管理平台
#  作者：黄涛
#  创建：2018-3-15
# 修改：2018-05-25 20:50 删除lzwt


from setuptools import setup, find_packages
from orange import get_ver

consoles = [
    'jym=params.transaction:JyJiaoyi.main',
    'sjdr=params.sjdr:sjdr',
    'jgm=params.jgm:GgJgm.main',
    'ac=params.zh:main',
    'km=params.accounting:Accounting.run',
    'fhlz=lvzhi.fhlz:main',
    'lz=lvzhi:main',
    #   'lzwt=lvzhi:lvzhiwenti',
    'br=params.branch:Contacts.main'
]
guis = []

setup(
    name='green-mongo',
    version=get_ver(),
    author='huangtao',
    author_email='hunto@163.com',
    platforms='any',
    description='work platform',
    long_description='work platform',
    install_requires=None,
    entry_points={
        'gui_scripts': guis,
        'console_scripts': consoles},
    packages=find_packages(exclude=['testing']),
    url='https://github.com/huangtao-sh/mongo.git',
    license='GPL',
)
