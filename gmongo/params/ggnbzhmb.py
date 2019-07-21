# 项目：   工作平台
# 模块：   内部账户批量开立模板
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 16:52

from gmongo.params import loadcheck, insert, ROOT, execute, fetch, fetchvalue, transaction, load_file
from orange import Path, R, extract, arg
from orange.utils.sqlite import fix_db_name

fields = 'jglx', 'whrq', 'km', 'bz', 'xh', 'hmgz', 'hm', 'tzed', 'zhzt', 'jxbz'


def loadfile():
    path = ROOT.find('ggnbzhmb.del')
    return load_file(path,
                     table='ggnbzhmb',
                     fields=fields,
                     drop=True,
                     encoding='gbk',
                     errors='ignore',
                     converter={
                         0: str.strip,
                         6: str.strip,
                     })
