# 项目：工作平台
# 模块：营业主管履职报告
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-25 20:47
# 修订：2018-05-30 增加答复意见

from orange import Path, R, datetime, wlen
from glemon import Document, P
from collections import defaultdict

ROOTPATH = Path('~/Documents/工作/工作档案/分行履职报告')


def wprint(s, width=20):
    l = wlen(s)
    if l < width:
        s = s+" "*(width-l)
    print(s, end='')


def _get_qc(dt):
    dt = datetime(dt)
    if dt.day <= 20:
        dt = dt.add(months=-1)
    return dt % '%Y%m'


class LzBranchs(Document):
    _projects = '_id', 'name'

    @classmethod
    def update(cls, jg, name):
        cls.objects(_id=jg).upsert_one(name=name)

    @classmethod
    def remove(cls, brs):
        for br in brs:
            objs = cls.objects(P._id == br)
            if objs.count() == 1:
                objs.delete()
            elif objs.count() == 0:
                print('未找到机构： %s ，忽略' % (br))
            else:
                print('机构 %s 存在多条记录，忽略' % (br))


class LzBaogao(Document):
    _projects = '_id', 'name', 'dept', 'br', 'date',\
        'cc', 'atts', 'dev_st', 'err_devs', 'dev_errs', 'spyj',\
        'fhjj', 'zhjj', 'shryj', 'fzryj', 'nr', 'qc'

    @classmethod
    def cur_qc(cls):
        obj = cls.objects.order_by(-P.qc).first()
        return obj and obj.qc

    @classmethod
    def report(cls):
        qc = cls.cur_qc()
        if qc:
            print('当前期次：%s' % (qc))
            yb = defaultdict(lambda: [])
            count = 0
            for br, dept, name in cls.objects(P.qc == qc).scalar('br', 'dept', 'name'):
                yb[br+dept].append(name)
                count += 1
            print('当期共 %d 条记录\n' % (count))
            print('错误机构数据')
            print('-'*50)
            ybs = []
            for br, names in yb.items():
                if len(names) > 1:
                    wprint(br, width=30)
                    ybs.extend(names)
                    print(*names, sep='\t')
            brs = set(yb.keys())
            print('\n未上报人员清单')
            print('-'*50)
            count = 0
            ybs = set(ybs)
            for jg, name in LzBranchs.objects.order_by(P._id).scalar('_id', 'name'):
                if (jg not in brs)and(name not in ybs):
                    wprint(jg, width=30)
                    print(name)
                    count += 1
            print('合计：%s' % count)

    @classmethod
    def import_file(cls):
        path = max((ROOTPATH / '1下载报告').glob('会计履职报告*.xls'))
        rows = path.sheets('会计履职报告')[1:]
        mapper = 0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17
        print('处理文件：%s' % (path))
        data = []
        _id = None
        for row in rows:
            if not row[0]:
                continue
            if _id != row[0]:
                nr = []
                if cls.objects(P._id == row[0]).count() == 0:
                    LzBranchs.update('%s%s' % (row[4], row[3]), row[2])
                    line = [row[x] for x in mapper]
                    line.extend([nr, _get_qc(row[5])])
                    data.append(line)
                _id = row[0]
            nr.append({'zl': row[18], 'nr': row[20]})
        if data:
            data = [dict(zip(cls._projects, d))for d in data]
            cls.objects.insert(data)
        print('共更新了 %d 条数据' % (len(data)))

    @classmethod
    def export(cls):
        for obj in cls.objects(P.dev_st == False):
            print(obj.br, obj.name, obj.err_devs, obj.dev_errs)


class LzWenTi(Document):
    # 履职报告的问题表
    # 月份、问题分类、机构、具体内容、报告人、部门、答复人、答复意见、状态，
    # 重点标志
    _projects = 'yf', 'wtfl', 'jg', 'jtnr', 'bgr', 'bm', 'dfr', 'dfyj', 'zt', 'zdwt'

    @classmethod
    def load_files(cls):
        # 从文件中读取收集到的问题
        qc = LzBaogao.cur_qc()
        fn = ROOTPATH / '2报告一览表'/('营业主管履职报告一览表（%s）.xlsx' % (qc))
        print('导入文件 %s' % (fn))
        data = fn.sheets(0)[1:]
        data.extend(fn.sheets(1)[1:])
        count = 0
        cls.objects(yf=qc).delete()
        for row in data:
            if row[3]:
                for jtnr in row[3].split('\n\n'):
                    LzWenTi(yf=qc, jg=row[0],
                            bgr=row[1], jtnr=jtnr).save()
                    count += 1
        print('共导入 %d 条数据' % (count))


def _get_date(rq):
    Pattern = R / r'(\d{4}).*?(\d{1,2}).*?'
    result = Pattern.match(rq)
    if result:
        result = result.groups()
        return '%s%02d' % (result[0], int(result[1]))


WIDTH1 = {
    'A:B': 13.75,
    'C:C': 21,
    'D:D': 46.63,
    'E:E': 8.63,
    'F:F': 11.25,
    "G:G": 37.63,
    "H:H": 15.5
}


class LzDafu(Document):
    # 月份，重要性，问题分类，机构，具体内容，报告人，部门，答复人，答复意见，后续跟踪
    _projects = 'yf', 'zyx', 'wtfl', 'jg', 'jtnr', 'bgr', 'bm', 'dfr', 'dfyj', 'hxgz'

    @classmethod
    def publish(cls):
        path = max((ROOTPATH/'4正式答复意见').glob('营业主管履职报告重点问题与答复意见*.xlsx'))
        print('处理文件： %s' % (path.name))
        mapper = {
            '提出时间': 'yf',
            '重要性': 'zyx',
            '问题分类': 'wtfl',
            '机构': 'jg',
            '具体内容': 'jtnr',
            '报告人': 'bgr',
            '反馈部门': 'bm',
            '答复人': 'dfr',
            '答复意见': 'dfyj',
            '后续跟踪': 'hxgz',
            '状态': 'hxgz',
        }
        curyf = None
        years = set()
        objs = []
        for idx, name, data in path.iter_sheets():
            if (len(data)) > 3:
                header = data[1]
                mapper1 = {}
                for k, v in mapper.items():
                    if k in header:
                        mapper1[v] = header.index(k)
                for row in data[2:]:
                    obj = {k: row[v]for k, v in mapper1.items()}
                    obj['yf'] = _get_date(obj['yf'])
                    years.add(obj['yf'][:4])
                    if name in ('重点问题', '一般问题'):
                        obj['zyx'] = name
                        curyf = obj['yf']
                    else:
                        if obj['yf'] == curyf:
                            continue
                    objs.append(obj)
        cls.drop()
        cls.objects.insert(objs)
        from .rpt import PUBLISH_FORMAT

        def mk_date(x): return '%s年%s月' % (x[:4], x[4:])
        print('当前月份：%s' % (curyf))
        with Path('~/abc.xlsx').write_xlsx(formats=PUBLISH_FORMAT)as book:
            book.worksheet = '重点问题'
            book.set_widths(WIDTH1)
            book.A1_H1 = '营业主管履职报告重点问题与答复意见（%s）' % (mk_date(curyf)), 'title'
            book.A2 = ['提出时间', '问题分类', '机构', '具体内容',
                       '报告人', '反馈部门', '答复意见', '后续跟踪'], 'header'
            book += 1
            for row in cls.objects((P.yf == curyf) & (P.zyx == '重点问题')).scalar('yf', 'wtfl', 'jg', 'jtnr', 'bgr', 'bm', 'dfyj', 'hxgz'):
                book.row += 1
                book.A = [mk_date(row[0]), row[1], row[2]], 'center'
                book.D = row[3], 'nr'
                book.E = row[4:6], 'center'
                book.G = row[6], 'nr'
                book.H = row[7], 'center'
            book.set_border('A2:H%s' % book.row)

            book.worksheet = '一般问题'
            book.set_widths(WIDTH1)
            book.A1_H1 = '营业主管履职报告重点问题与答复意见（%s）' % (mk_date(curyf)), 'title'
            book.A2 = ['提出时间', '问题分类', '机构', '具体内容',
                       '报告人', '反馈部门', '答复意见', '后续跟踪'], 'header'
            book += 1
            for row in cls.objects((P.yf == curyf) & (P.zyx == '一般问题')).scalar('yf', 'wtfl', 'jg', 'jtnr', 'bgr', 'bm', 'dfyj', 'hxgz'):
                book += 1
                book.A = [mk_date(row[0]), row[1], row[2]], 'center'
                book.D = row[3], 'nr'
                book.E = row[4:6], 'center'
                book.G = row[6], 'nr'
                book.H = row[7], 'center'
            book.set_border('A2:H%s' % book.row)
