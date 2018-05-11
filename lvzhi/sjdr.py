# 项目：运营主管履职报告
# 模块：数据导入
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-04-19 14:40

from orange import Path
from .model import LvZhi
from lzwt import LzWenTi


def import_wenti():
    # 从档案数据中导入问题
    ROOT = Path(r"~/OneDrive/工作/工作档案/会计履职报告/履职报告梳理")
    fields = LzWenTi._fields_without_id
    fields.remove('dfr')
    LzWenTi.objects(status='发布').delete()
    for fn in ROOT.glob('营业主管履职报告重点问题与答复意见*.xls?'):
        print('处理文件 %s ' % (fn))
        for idx, name, data in fn.iter_sheets():
            i = 0
            if data:
                zdwt = '重点' in name
                for row in data[2:]:
                    d = dict(zip(fields, row))
                    LzWenTi(**d, zdwt=zdwt, status='发布').save()
                    i += 1
            print('%s：共导入 %d 条数据 %s' % (name, i, zdwt))
