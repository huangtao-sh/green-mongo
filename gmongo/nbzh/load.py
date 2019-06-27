# 项目：   工作平台
# 模块：   内部账户
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-06-27 08:59

from orange.utils.sqlite import loadcheck, execute, insert
from orange import split, HOME


def loadnbzh():
    @loadcheck
    def _(path):
        execute('delete from nbzh')
        for row in split(path.iter_csv(errors='ignore', encoding='gbk'),
                         10000):
            insert('nbzh', row)

    path = (HOME / 'OneDrive/工作/参数备份').find('fhnbhzz.del')
    return _(path)