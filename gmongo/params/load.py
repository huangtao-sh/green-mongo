# 项目：   参数管理程序
# 模块：   导入数据模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-07-10 08:22
from .loadzip import loadzip
from orange import HOME, R, datetime, Data, includer, mapper
from .loader import Loader, loadcheck
from orange.utils.sqlite import tran, executefile

Downloads = HOME/'Downloads'
Ver = R/r'\d+'


@mapper
def conv(row: list) -> list:
    row[10] = "-".join([row[10][:4], row[10][4:6], row[10][6:8]])
    return row


@tran
def load_yyzg():
    path = Downloads.find('营业主管信息*.xls*')
    ver = Ver.extract(path.pname,)
    loadcheck('yyzg', path.name, datetime(path.mtime) % '%F %H:%M:%S', ver)
    loader = Loader('yyzg', 11, includer(
        2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 11), conv)
    loader.data = path.sheets(0)[1:]
    if r := loader.load():
        print(f'导入 {path.name} 成功，行数：{r.rowcount}')
    else:
        raise Exception(f'导入 {path.name} 失败')


@tran
def load_nkwg():
    path = Downloads.find('resultReg*.xls*')
    ver = ""
    loadcheck('nkwg', path.name, datetime(path.mtime) % '%F %H:%M:%S', ver)
    loader = Loader('nkwg', 29, includer(*range(29)))
    loader.data = path.sheets(0)
    if r := loader.load():
        print(f'导入 {path.name} 成功，行数：{r.rowcount}')
    else:
        raise Exception(f'导入 {path.name} 失败')


loads = [
    load_yyzg,
    load_nkwg,
]


def loadall():
    loadzip()
    for load in loads:
        try:
            load()
        except Exception as e:
            print(e)
