# 项目：工作平台
# 模块：测试平台
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-10-14 16:23

import unittest
from glemon import P, Document, FileImported
from orange import Path, HOME
from params.user import Teller

text = (HOME/'OneDrive/工作/参数备份').find('是否校验磁道信息.*').text


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

    def testLoadFile1(self):
        with Path.tempfile(text, suffix=".del")as f:
            TestLoad.loadfile(f)
            data1 = list(TestLoad.objects.scalar('_id'))
            data2 = [x[0] for x in f]
        self.assertListEqual(data1, data2)

    def testLoadFile2(self):
        options = {'dupcheck': True}
        with Path.tempfile(text, suffix=".del")as f:
            TestLoad.loadfile(f, options)
            with self.assertRaises(FileImported):
                TestLoad.loadfile(f, options)
