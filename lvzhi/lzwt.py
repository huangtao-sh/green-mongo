# 项目：营业主管履职管理平台
# 模块：履职问题管理模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-11-11 09:10

from glemon import Document, P
from orange import Path


class LzWenTi(Document):
    # 履职报告的问题表
    # 月份、问题分类、机构、具体内容、报告人、部门、答复人、答复意见、状态，
    # 重点标志
    _projects = 'yf', 'wtfl', 'jg', 'jtnr', 'bgr', 'bm', 'dfr', 'dfyj', 'zt', 'zdwt'

    @classmethod
    def load_files(cls):
        # 从文件中读取收集到的问题
        from .model import LvZhi
        qc = LvZhi.cur_qc
        path = Path('~/OneDrive/工作/工作档案/会计履职报告') / qc
        fn = path/('营业主管履职报告一览表（%s）.xlsx' % (qc))
        print('导入文件 %s' % (fn))
        data = fn.sheets('明细表')
        yf = qc
        count = 0
        cls.objects(yf=qc).delete()
        for row in data[1:]:
            if row[0]:
                jg = row[0]
            if row[1]:
                bgr = row[1]
            if row[5]:
                for jtnr in row[5].split('\n\n'):
                    LzWenTi(yf=yf, jg=jg, bgr=bgr, jtnr=jtnr).save()
                    count += 1
        print('共导入 %d 条数据' % (count))
