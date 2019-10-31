# 项目：   工作平台
# 模块：   柜员表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-10-31 14:37

from gmongo.params import load_file, ROOT, fetchone, fetch, get_param_ver
from orange import R, arg, tprint
from gmongo.__version__ import version

POST = 'R01:交易发起岗 R02:前台授权岗 R03:凭证管理岗 R04:分中心授权岗 R05:权限申请发起岗 R06:权限管理岗 R07:审查比对岗 R08:人工验印岗 R09:后台录入岗 R10:附加要素补录岗 R11:后台授权岗 R12:业务监测岗 R13:异常授权岗 R14:异常处理岗 R15:权限管理授权岗 R16:审查复核岗 R17:附加要素复核岗 R18:数据录入岗 R19:数据复核岗 R20:验票与保管岗 R21:审查岗 R22:信用卡审查岗 R41:放款受理人 R42:放款审核人 R43:放款核准人 R44:放款复核人 R45:业务审核岗'.split(
)


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


def show_teller(sql, arg):
    header = '柜员号，姓名，电话，柜员级别，柜组，机构号，员工号，执行交易组，转账限额，现金限额，认证类型，状态，屏蔽交易，岗位性质，启用日期，停用日期，交易币种，发起交易组，证件种类，证件号码'.split(
        '，')
    for tlr in fetch(sql, arg):
        tlr = list(tlr)
        gw = tlr.pop(7)
        tprint(zip(header, tlr), {0: '20'})
        g = []
        for x, y in zip(POST, gw.split(',')):
            if y:
                g.append((x, y))
        tprint(g, {0: '20'})
        print()


def list_teller(cond, arg=[]):
    print('柜员号  姓名                   用户号     机构    状态')
    tprint(
        fetch(f'select id,name,userid,branch,zt from teller where {cond}', arg), {
            0: '8',
            1: '20',
            2: '8',
            3: '10'
        })


@arg('query', help='查询条件')
def main(query=None):
    ver = get_param_ver('teller')[0]
    print('程序版本：', version)
    print('数据版本：', ver, end='\n\n')
    if R / r'\d{5}' == query:
        show_teller('select * from teller where id=?', [query])
    elif R / r'[A-Z]{1,2}\d{4}' == query:
        list_teller('userid=?', [query])
    else:
        list_teller(f'name like "{query}%"')