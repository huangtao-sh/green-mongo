# 项目：数据库模型
# 模块：会计科目模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-09-24 11:26
# 修订：2017-10-17 使用 glemon 定义的模型
# 修订：2018-09-06 修正数据导入错误

from glemon import Document, P
from orange import R, arg
from .zh import GgKmzd, AcTemplate


KEMU = R / r'(?P<_id>\d{4,6})\s*(?P<name>\w*)'
BLANKS = R / r'第.章。*', R / r'本科目为一级科目.*'
AcPattern = R / r'\d{1,6}'


class Accounting(Document):
    _textfmt = '{self._id}\t{self.name}\n'\
        '{self.descrip}'
    _projects = '_id', 'name', 'description'

    @property
    def descrip(self):
        return "\n".join(self.description)

    @property
    def as_html(self):
        return "<h2>%s  %s</h2><p>%s</p>" % (self.id, self.name,
                                             "</p><p>".join(self.description))

    @property
    def has_child(self):
        if len(self.id) == 4:
            return self.search(items=self.id).count() > 0

    @property
    def parent(self):
        if len(self.id) == 6:
            return self.id[:4]

    @classmethod
    def proctxt(cls, file, options=None):
        data = {}
        kemu = None
        for line in file.lines:
            line = line.strip()
            if any([blank.match(line) for blank in BLANKS]):
                continue
            elif KEMU.match(line):
                kemu = KEMU.match(line).groupdict()
                description = []
                data[kemu['_id']] = [kemu['_id'], kemu['name'], description]
            else:
                if kemu:
                    description.append(line)
        return list(data.values())

    @classmethod
    def search(cls, query=None, category=None, items=None):
        if query:
            if AcPattern.match(query):
                q = P.id.startswith(query)
            else:
                q = P.name.regex(query)
        elif category:
            q = P.id.regex(r'^%s\d{3}$' % (category))
        elif items:
            q = P.id.regex(r'^%s\d{2}$' % (items))
        else:
            q = P.id.regex(r'\d{4}$')
        return cls.find(q).order_by(P.id)

    @classmethod
    @arg('-i', '--import', dest='filename', help='导入科目文件')
    @arg('query', nargs='*', help='查找会计科目')
    @arg('-c', '--category', help='按类别查询')
    @arg('-t', '--items', help='查找科目的子目')
    def run(cls, filename=None, query=None, category=None, items=None):
        if filename:
            cls.import_file(filename)
        for _query in query:
            q = cls.search(_query)
            if q.count() > 1:
                for i in q:
                    print(i.id, i.name, sep='\t')
            elif q.count() == 1:
                print(q.first())
            if R/r'\d{6}' == _query:
                print('\n科目属性')
                print('-'*20)
                GgKmzd.search(_query)
                print('\n内部账户开立模板')
                print('-'*20)
                AcTemplate.search(_query)
        if category or items:
            for i in cls.search(category=category, items=items):
                print(i.id, i.name, sep='\t')


if __name__ == '__main__':
    Accounting.run()
