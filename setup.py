#!/usr/bin/env python3
#  项目：生产管理平台
#  作者：黄涛
#  创建：2018-3-15

from setuptools import setup, find_packages
from orange import get_ver

consoles = [
    'jym=parameters.transaction:JyJiaoyi.main',
    'sjdr=parameters.sjdr:sjdr',
    'jgm=parameters.jgm:GgJgm.main',
    'kemu=parameters.accounting:Accounting.run'
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
