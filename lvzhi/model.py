# 项目：会计主管履职报告
# 模块：数据库模型
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-04-19 08:36

from glemon import Document, P
from orange import R, Path, datetime, now, classproperty, wlen


#############################
#  以下内容为从OA上下载的内容
#############################
'''    
class Detail(EmbeddedDocument):  # 履职报告详细信息
    xh=IntField()         # 序号
    bgzl=StringField()    # 报告种类
    zyx=StringField()     # 重要性
    jtnr=StringField()    # 具体内容
'''


class LvZhi(Document):    # 履职报告
    # 标题，类型、期次、报告人、部门、机构、日期、附件，详细信息
    _projects = '_id', 'lx', 'qc', 'bgr', 'bm', 'jg', 'rq', 'fj', 'detail'
    '''
    bh=StringField(primary_key=True)   #  编号
    lx=StringField()      # 类型 0-会计主管 1-事后监督
    qc=StringField()      # 期次，格式为：YYYYMM
    gzl=StringField()     # 流程
    bt=StringField()      # 标题
    bgr=StringField()     # 报告人
    bm=StringField()      # 部门
    jg=StringField()      # 机构
    rq=StringField()      # 报告日期
    fj=ListField(StringField())   # 附件
    sbyx=BooleanField()           # 设备运行情况
    ycsbmc=StringField()          # 故障设备名称
    ycnr=StringField()            # 故障设备详情
    detail=ListField(EmbeddedDocumentField(Detail))  # 详细信息
'''

    _textfmt = '''标题：{self.bt}
类型：{self.lx}
报告人：{self.bgr}
部门：{self.bm}
机构：{self.jg}
期次：{self.qc}
报告日期：{self.rq}
内容：{self.detail}
'''

    @classmethod
    def load_files(cls):
        ROOT = Path(r'~\OneDrive\工作\工作档案\会计履职报告')
        filename = max(ROOT.glob('会计履职报告*.xls'))
        if not filename.exists():
            raise Exception("文件不存在")
        print('即将导入文件  %s' % (filename))
        sheet = filename.sheets(0)
        bt = None
        d = {}
        count = 0
        for row in sheet[1:]:
            if row[0] and bt != row[0]:
                if d:
                    cls.objects(_id=bt).upsert_one(**d)
                    count += 1
                xh = 1
                d = dict(bgr=row[2],
                         bm=row[3], jg=row[4], rq=row[5], fj=row[7],
                         lx='0' if '会计主管履职' in row[18] else '1',
                         detail=[{'xh': xh, 'bgzl': row[18], 'zyx':row[19],
                                  'jtnr':row[20]}],
                         qc=datetime(row[5]).add(months=-1) % ('%Y-%m'))
                bt = row[0]
            elif row[0]:
                xh += 1
                if row[18] and row[20]:
                    d['detail'].append({'xh': xh, 'bgzl': row[18], 'zyx': row[19],
                                        'jtnr': row[20]})
        if d:
            cls.objects(_id=bt).upsert_one(**d)
            count += 1
        print('共导入 %d 条数据' % (count))

    @classproperty
    def cur_qc(self):
        return max(self.objects.distinct('qc'))

    @staticmethod
    def get_path(is_root=False):
        month = datetime.today().add(months=-1).strftime('%Y-%m')
        root = Path('~/OneDrive/工作/工作档案/会计履职报告/%s' % (month))
        root.ensure()
        if is_root:
            return root
        else:
            path = root/'附件'
            path.ensure()
            return path

    @staticmethod
    def get_begin_date():        # 获取起始日期
        begin = datetime.today().add(months=-1).replace(day=25)  # 从上个月25日起
        return begin % '%F'  # 开始日期

    @classmethod
    def report(cls):
        # 报告分行上报情况
        from collections import defaultdict
        cur = now().add(months=-1) % ('%Y-%m')
        prev = now().add(months=-2) % ('%Y-%m')
        print('当前期次：%s\n上一期次：%s' % (cur, prev))
        a = cls.aggregate()
        a.match(P.qc.in_([cur, prev]))
        a.project(-P._id, P.bgr, P.qc, jg={'$concat': ['$jg', '$bm']})
        a.group(P.jg, P.data.push({"bgr": "$bgr", "qc": "$qc"}))
        result = defaultdict(lambda: [])
        for i in a:
            rqs = [x['qc'] for x in i['data']]
            if all([rq == cur for rq in rqs]):
                result['cur'].append(i)
            elif all([rq == prev for rq in rqs]):
                result['prev'].append(i)
        for k in ('cur', 'prev'):
            d = result[k]
            if k == 'cur':
                print('上月未提交记录：')
            else:
                print('本月未提交记录：')
            for i in sorted(d, key=lambda x: x['_id']):
                jg = i['_id']
                jg = jg+' '*(30-wlen(jg))
                print('%s\t会计履职报告\t%s' % (jg, i['data'][0]['bgr']))
            print('共 %d 条记录。' % (len(d)))
