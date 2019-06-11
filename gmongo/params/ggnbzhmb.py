# 项目：   工作平台
# 模块：   内部账户批量开立模板
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 16:52

from gmongo.params import loadcheck, insert, ROOT, execute, fetch, fetchvalue, transaction
from orange import Path, R, extract, arg
from orange.utils.sqlite import fix_db_name


def loadfile():
    path = ROOT.find('ggnbzhmb.del')

    @loadcheck
    def _(path: Path):
        execute('delete from ggnbzhmb')
        insert(
            'ggnbzhmb',
            path.iter_csv(encoding='gbk',
                          errors='ignore',
                          converter={
                              0: str.strip,
                              6: str.strip,
                          }))
        print(f'{path.name} 导入成功')

    return _(path)

