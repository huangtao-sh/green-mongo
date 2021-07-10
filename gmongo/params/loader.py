# 项目：   参数管理模块
# 模块：   数据导入类
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-07-10 11:40

from orange import Path, info, fatal, decode, Data, limit, datetime
from orange.utils.sqlite import fetchvalue, execute, load


def loadcheck(name: str, path: str, mtime: datetime, ver: str):
    checkSQL = "select count(name) from loadfile where name=? and path=? and mtime>=datetime(?)"
    doneSQL = "insert or replace into loadfile values(?,?,datetime(?),?)"
    if value := fetchvalue(checkSQL, [name, path, mtime]):
        raise Exception(f'文件：{path} 已导入')
    else:
        execute(doneSQL, [name, path, mtime, ver])


class Loader():
    __slots__ = ('clear', 'converters', 'kwargs', 'method',
                 'table', 'fields', 'data')

    def __init__(self, table: str,  fields: str, *converters, method: str = 'insert',  **kw):
        self.table = table
        self.fields = fields
        self.clear = True
        self.converters = converters
        self.kwargs = kw
        self.data = None
        self.method = method

    def test(self):
        if self.data:
            data = Data(self.data, *self.converters,  **self.kwargs)
            for row in limit(data, 10):
                print(len(row), row)

    def load(self):
        if self.data:
            data = Data(self.data, *self.converters, **self.kwargs)
            return load(data, self.table, self.method, self.fields, self.clear)
