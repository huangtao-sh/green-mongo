# 项目：工作平台
# 模块：测试平台
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-10-14 16:23

import unittest
from glemon import P, Document
from orange import Path, HOME


class TestLoad(Document):
    _projects = '_id'

    load_options = {
        'dupcheck': False
    }


class TestLoadFile(unittest.TestCase):
    def setUp(self):
        TestLoad.drop()

    def tearDown(self):
        TestLoad.drop()

    def testLoadFile(self):
        filename = (HOME/'OneDrive/工作/参数备份').find('是否校验磁道信息.*')
        TestLoad.loadfile(filename)
        data1 = list(TestLoad.objects.scalar('_id'))
        data2=[x[0] for x in filename]
        self.assertListEqual(data1,data2)
