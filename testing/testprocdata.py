import unittest

from gmongo.utils import procdata


class TestLoadFile(unittest.TestCase):
    def testprocdata1(self):
        data = (
            (34, 26, 45),
            (77, 23, 45),
            (None, None, None),
            (89, 34, 35),
        )
        d = tuple(procdata(data, header=(1, 2), converter={0: str, 1: float}))
        self.assertEqual(2, len(d[0]))
        self.assertEqual(3, len(d))
        self.assertEqual(d[0][0],'26' )
        self.assertTrue(isinstance(d[0][0], str))
        self.assertTrue(isinstance(d[0][1], float))


    def testprocdata2(self):
        data = (
            ('姓名','年龄','生日'),
            (34, 26, 45),
            (77, 23, 45),
            (None, None, None),
            (89, 34, 35),
        )
        d = tuple(procdata(data, header=('年龄', '生日'), converter={0: str, 1: float}))
        self.assertEqual(2, len(d[0]))
        self.assertEqual(3, len(d))
        self.assertEqual(d[0][0],'26' )
        self.assertTrue(isinstance(d[0][0], str))
        self.assertTrue(isinstance(d[0][1], float))

    def testprocdata3(self):
        data = (
            ('姓名','年龄','生日'),
            (34, 26, 45),
            (77, 23, 45),
            (None, None, None),
            (89, 34, 35),
        )
        d = tuple(procdata(data, mapper={'年龄': str, '生日': float}))
        self.assertEqual(2, len(d[0]))
        self.assertEqual(3, len(d))
        self.assertEqual(d[0][0],'26' )
        self.assertTrue(isinstance(d[0][0], str))
        self.assertTrue(isinstance(d[0][1], float))

