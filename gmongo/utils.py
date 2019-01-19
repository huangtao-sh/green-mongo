# 项目：   工作平台
# 模块：   重复导入文件检查
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-19 08:46

from orange.utils.sqlite import executescript, findvalue, execute, trans
from orange import Path

need_create = True


def createtable():
    global need_create
    executescript('''
    create table if not exists LoadFile( -- 文件重复检查表
        filename text primary key,       -- 文件名
        mtime int                        -- 修改时间
    );
    ''')
    need_create = False


def checkload(filename: str, loadfile: "function", *args, **kw)->bool:  # 检查文件是否已经导入
    '''
    检查指定的文件是否已经导入数据库，如未导入执行 loadfile 函数
    filename: 待导入的文件
    loadfile: 导入文件的程序
    *args,**kw : loadfile 除 filename 以外的参数
    '''
    need_create and createtable()       # 第一次执行本函数时建表
    file = Path(filename)
    name = file.name
    a = findvalue('select mtime from LoadFile where filename=?',
                  [name])  # 查询是否已导入
    is_imported = a and a >= file.mtime  # 判断是否已经导入
    if not is_imported:
        loadfile(filename, *args, **kw)
        with trans():
            execute('insert or replace into LoadFile values(?,?)',  # 保存记录
                    [name, file.mtime])
    return is_imported


def procdata(data, header: list = None, converter: dict = None, mapper: dict = None):
    converter = converter or {}
    if isinstance(mapper, dict)and mapper:
        header = list(mapper.keys())
        for i, v in enumerate(mapper.values()):
            if v:
                converter[i] = v
    if any(isinstance(x, str)for x in header):
        for i, row in enumerate(data):
            if all(x in row for x in header):
                header = [row.index(x)for x in header]
                data = data[i+1:]
                break
        else:
            return
    for row in data:
        if any(row):
            if header:
                row = [row[i]for i in header]
            for i, c in converter.items():
                row[i] = c(row[i])
            yield row
