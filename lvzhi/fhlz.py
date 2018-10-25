# 项目：工作平台
# 模块：分行履职报告
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-07-06 11:34
# 修订：2018-5-14 增加分行履职报告格式转换功能

from orange import Path, R, classproperty, arg, ensure, extract
from glemon import Document, P
from glemon.loadcheck import LoadFile
from collections import namedtuple
from orange.coroutine import run, wait
from params.branch import Branch, Contacts

WenTi = namedtuple('WenTi', ('fh', 'tcr', 'ms'))

SAVEPATH = Path('~/Documents/工作/工作档案/分行履职报告')
ROOT = SAVEPATH / "分行上报"
BRANCHS = Branch.branchs()
print(BRANCHS)


def transbr(name):
    for br in BRANCHS:
        if br in name:
            return br


LeiBieTrans = {'分管行长': '分管行长',
               '行领导': '分管行长',
               '部门负责人': '运营主管'}


def translb(name):
    for k, v in LeiBieTrans.items():
        if k in name:
            return v


Date1 = R / r'.*?(\d{4}).*?(\d{1,2}).*?(\d{1,2})?'
Date2 = R / r'\d{8}'
Baogaoren = R / r'报告人[:：]?\s*(.*?)\s.*?'

FORMATS = {
    'bt': {'font_name': '黑体', 'font_size': 18,
           'align': 'center', 'valign': 'vcenter'},
    'normal': {'font_name': '微软雅黑', 'font_size': 12, 'text_wrap': True,
               'valign': 'center', 'align': 'left'},
    'vnormal': {'font_name': '微软雅黑', 'font_size': 12, 'text_wrap': True,
                'align': 'center', 'valign': 'vcenter'}, }

WIDTHS = {'A:A': 13,
          'B:B': 86}


class FhLvzhi(Document):
    _projects = 'qc', 'lb', 'jg', 'bgr', 'headers', 'data', 'br_order'
    '期次、类别：运营主管，分行管长、报告机构，报告人，表头，报送内容'

    @classproperty
    def curqc(self):
        return max(self.objects.distinct('qc'))

    @classmethod
    def report(cls, qc=None):
        # 报告当前各分行上报情况
        qc = qc or cls.curqc
        print('分行未上报情况统计')
        print('报告期次：%s' % (qc))
        fghz = set(cls.find(qc=qc, lb='分管行长').distinct('jg'))
        kjzg = set(cls.find(qc=qc, lb='运营主管').distinct('jg'))
        print('  分行    分管行长     运营主管')
        for x in sorted(BRANCHS):
            def test(a): return "    " if x in a else "未报"
            if ((x not in fghz)or(x not in kjzg)):
                print('%s    %s         %s' % (x, test(fghz), test(kjzg)))
        print(' 合计        %d           %d' % ((len(BRANCHS) - len(fghz)),
                                              (len(BRANCHS) - len(kjzg))))

    @classmethod
    def export(cls, qc=None):
        qc = qc or cls.curqc
        print('导出期次：%s' % (qc))
        wentis = []
        for lb in ('分管行长', '运营主管'):
            query = (P.qc == qc) & (P.lb == lb)
            with (SAVEPATH / '报告' / ('%s履职报告（%s）.xlsx' % (lb, qc))).write_xlsx()\
                    as book:
                book.add_formats(FORMATS)
                count = 0
                for bg in cls.find(query).order_by('br_order'):
                    print("%-10s%s" % (bg.jg, bg.bgr))
                    book.worksheet = bg.jg
                    book.set_widths(WIDTHS)
                    book.A1_B1 = bg.headers[0], 'bt'
                    book.A2_B2 = bg.headers[1], 'normal'
                    book.A3_B3 = bg.headers[2], 'normal'
                    r1 = 4
                    for d in bg.data:
                        r2 = r1 + len(d['nr']) - 1
                        range_ = "A%s" % (r1)
                        if r2 > r1:
                            range_ = '%s:A%s' % (range_, r2)
                        book[range_] = d['xm'], 'vnormal'
                        for i, n in enumerate(d['nr']):
                            book['B%s' % (i + r1)] = str(n).strip(), 'normal'
                        r1 = r2 + 1
                        if '意见或建议' in d['xm']:
                            for n in d['nr']:
                                if n and n != '无':
                                    wentis.append(WenTi(bg.jg, bg.bgr,
                                                        n.strip()))
                    count += 1
                print('%s，共 %d 条记录' % (lb, count))
        filename = SAVEPATH / '问题' / ('分行运营主管履职报告问题%s.xlsx' % (qc))

        with filename.write_xlsx() as book:
            book.add_formats(FORMATS)
            book.worksheet = '分行履职报告问题表'
            book.set_widths({'A:B': 9, 'C:C': 80, 'D:E': 15, 'F:F': 80})
            book.A = '分行 提出人 问题描述 答复部门 答复人 答复意见'.split(), 'h2'
            book + 1
            for d in wentis:
                book.A = [d.fh, d.tcr], "vnormal"
                book.C = d.ms, 'normal'
                book.D = ['', ''], 'vnormal'
                book.F = '', 'normal'
                book + 1
            print('共导出问题 %d 条' % (len(wentis)))

    @classmethod
    def test(cls):
        a = cls.objects.first()
        print(a.lb, a.qc)
        print(a.jg)
        for x in a.data:
            print(x['xm'], x['nr'])

    @classmethod
    async def load_files(cls, *files):
        files = [x for x in (files or ROOT.rglob('*履职报告*.*'))
                 if x.lsuffix.startswith('.xls')]
        files = LoadFile.check('fhlz', *files)
        if files:
            coros = [cls.load_file(filename)for filename in files]
            await wait(coros)
        else:
            print('无需要导入的文件')

    @classmethod
    async def load_file(cls, filename):
        print('开始处理文件', filename.pname)
        fn = filename
        try:
            data = fn.sheets(0)
            headers = [data[i][0] for i in range(3)]
            lb = translb(headers[0])
            ensure(lb is not None, '类别不正确')
            jg = transbr(headers[1])
            ensure(jg is not None, '报告机构格式不正确')
            d = headers[2]
            if Date2 / d:
                qc = list(Date2 / d)
                qc = qc and qc[0][:6]
            elif Date1 / d:
                qc = list(Date1 / d)
                qc = qc and qc[0]
                qc = '%s%02d' % (qc[0], int(qc[1]))
            qc = int(qc[:4]) * 4 + (int(qc[4:]) - 2) // 3
            qc = '%s-%s' % (qc // 4, qc % 4 + 1)
            d = []
            bgr = Baogaoren == headers[2]
            bgr = bgr.groups()[0]
            for r in data[3:]:
                if r[0]:
                    x = {'xm': r[0], 'nr': []}
                    d.append(x)
                x['nr'].append(r[1])
            print('报告机构：%s' % (jg))
            print('报告期次：%s' % (qc))
            print('报告类别：%s' % (lb))
            print('报告人：  %s' % (bgr))
            await cls.find(qc=qc, lb=lb, jg=jg).upsert_one(
                headers=headers, bgr=bgr, data=d)
            LoadFile.save('fhlz', fn)
        except Exception as e:
            print('文件 %s 处理存在问题' % (fn.pname))
            print(e)


WIDTHS2 = {
    'A:A': 9.13,
    'B:B': 75.4,
    'C:C': 9.13,
    'D:D': 13,
    'E:E': 53.53
}
FORMATS2 = {
    'title': {'font_name': '黑体', 'font_size': 16, 'align': 'center', 'bold': True},
    'h2': {'font_name': '仿宋_GB2312', 'font_size': 12, 'align': 'center', 'bold': True,
           'bg_color': 'black', 'font_color': 'white'},
    'cnormal': {'font_name': '仿宋_GB2312', 'font_size': 12, 'align': 'center',
                'valign': 'vcenter', 'text_wrap': True, },
    'normal': {'font_name': '仿宋_GB2312', 'font_size': 12,  'valign': 'vcenter', 'text_wrap': True, },
}


class FhWenTi(Document):
    _projects = 'qc', 'fh', 'tcr', 'wtms', 'dfbm', 'dfr', 'dfyj', 'order'

    @classmethod
    def import_file(cls, filename):
        qc = extract(filename.pname, r'\d{4}\-\d')
        hz = set(FhLvzhi.find((P.qc == qc) &
                                 (P.lb == '分管行长')).distinct('bgr'))
        data = filename.sheets('分行履职报告问题表')
        if data:
            cls.find(P.qc == qc).delete()
            for d in data[1:]:
                d = d[:6]
                if not d[3].strip():
                    d[3] = '运营管理部'
                order = BRANCHS.get(d[0], 150)*10
                if d[1] not in hz:
                    order += 1
                d.append(order)
                d.insert(0, qc)
                obj = cls(zip(cls._projects, d))
                obj.save()
            data = [x for x in cls.find(P.qc == qc).order_by(P.order).scalar(
                'fh', 'wtms', 'tcr', 'dfbm', 'dfyj'
            )]
            title = "%s年%s季度分管行领导及部门负责人履职报告问题的答复意见" % tuple(qc.split('-'))
            filename = SAVEPATH / '正式答复意见' / ('关于%s.xlsx' % (title))
            print(filename)
            with filename.write_xlsx()as book:
                book.worksheet = '分行履职报告问题表'
                book.set_widths(WIDTHS2)
                book.add_formats(FORMATS2)
                book.A1_E1 = title, 'title'
                book.A2 = ['分行名称', '问题描述', '提出人', '答复部门', '答复意见'], "h2"
                fh_start, tcr_start = 3, 3
                tcr, fh = None, None
                for line, row in enumerate(data, 3):
                    book.row = line
                    book.B = row[1], 'normal'
                    book.D = row[3], 'cnormal'
                    book.E = row[4], 'normal'
                    if fh != row[0]:
                        if fh:
                            book['A%d:A%d' %
                                 (fh_start, line-1)] = fh, 'cnormal'
                        fh_start = line
                        fh = row[0]
                    if tcr != row[2]:
                        if tcr:
                            book['C%d:C%d' %
                                 (tcr_start, line-1)] = tcr, 'cnormal'
                        tcr_start = line
                        tcr = row[2]
                if fh:
                    book['A%d:A%d' % (fh_start, line)] = fh, 'cnormal'
                if tcr:
                    book['C%d:C%d' % (tcr_start, line)] = tcr, 'cnormal'
                book.set_border('A2:E%d' % (line))


@arg('-i', '--import', dest='imp', action='store_true', help='导入分行履职报告')
@arg('-e', '--export', action='store_true', help='导出分行履职报告')
@arg('-r', '--report', action='store_true', help='报告分行的上报情况')
@arg('-c', '--clear', action='store_true', help='清理已导入的记录')
@arg('-q', '--qici', dest='qc', nargs='?', help='指定期次')
@arg('-v', '--convert', action='store_true', help='转换正式答复意见格式')
def main(imp=False, export=False, report=False, clear=False, qc=None, convert=False):
    if imp:           # 导入履职报告文件
        run(FhLvzhi.load_files())
    if export:        # 导出报告
        FhLvzhi.export(qc)
    if report:        # 报告分行报送情况
        FhLvzhi.report(qc)
    if clear:         # 清理已导入数据
        LoadFile.find(category='fhlz').delete()
        FhLvzhi.drop_collection()
        print('清理完成')
    if convert:
        ROOT = Path('~/Documents/工作/工作档案/分行履职报告/答复意见')
        filename = max(ROOT.glob('分行运营主管履职报告问题*.xlsx'))
        print('开始处理文件%s' % (filename))
        FhWenTi.import_file(filename)
