# 项目：参数平台
# 模块：额度等级
# 作者：黄涛
# License: GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-10-31 20:43


from glemon import Document, enlist, FileImported, P
from contextlib import suppress
from orange import arg, tprint


class EduDengji(Document):
    _projects = enlist('_id,name,ed')
    _header = None

    @classmethod
    def header(cls):
        if not cls._header:
            d = cls.find(_id='00').first()
            if d:
                cls._header = d.ed
        return cls._header

    @classmethod
    @arg('dj', nargs='*', help='查询额度等级')
    @arg('-l', '--list', dest='list_', action='store_true', help='列出等级代码清单')
    def main(cls, dj=[], list_=False):
        if list_:
            print('代码    等级名称')
            tprint(cls.find(P._id != '00').scalar('_id,name'), sep='    ')
        header = cls.header()
        for d in dj:
            a = cls.objects.get(d)
            if a:
                tprint(
                    [
                        ('等级代码', d),
                        ('等级名称', a.name)
                    ],
                    format_spec={0: '25'}
                )
                tprint(
                    [(n, v)for n, v in zip(
                        header, a.ed) if v],
                    format_spec={0: '25', 1: '18,.2f'}
                )

    @classmethod
    def procdata(cls, file, options):
        data = file.sheets('调整后的额度等级表')
        header = ('00', '额度等级', data[3][2:15])
        d = [header]
        for row in data[4:77]:
            dj = row[0]
            dj = dj if isinstance(dj, str) else '%02d' % (dj)
            d.append((dj, row[1], row[2:15]))
        return d
