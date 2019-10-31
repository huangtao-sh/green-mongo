# 项目：   工作平台
# 模块：   柜员表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-10-31 14:37

from gmongo.params import load_file, ROOT, fetchone
from orange import R, arg, tprint


def read(path):
    for row in path.iter_csv():
        yield tuple(
            map(str.strip, [
                *row[:3], *row[4:8], ','.join(map(str.strip, row[8:-25])),
                row[-25], *row[-23:-20], *row[-10:-3], *row[-2:]
            ]))


def load_teller():
    path = ROOT.find('users_output.csv')
    return load_file(path, 'teller', proc=read)


def show_teller(teller):
    tlr = fetchone('select * from teller where id=?', [teller])
    header = '柜员号，姓名，电话，柜员级别，柜组，机构号，员工号，岗位，执行交易组，转账限额，现金限额，认证类型，状态，屏蔽交易，岗位性质，启用日期，停用日期，交易币种，发起交易组，证件种类，证件号码'.split(
        '，')
    if tlr:
        tprint(zip(header, tlr), {0: '15'})


@arg('teller', help='柜员号')
def main(teller=None):
    if teller:
        show_teller(teller)