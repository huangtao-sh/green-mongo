# 项目：   工作平台
# 模块：   通讯录
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-10-20 20:23

from orange import HOME, arg, R, tprint
from . import load_file, fetch, get_param_ver


def loadfile():
    path = (HOME / 'OneDrive/工作/参数备份/通讯录').find('通讯录*.xls')
    period = path.pname[-10:]
    def reader(path): return path.sheets(0)[1:]
    return load_file(path, 'txl', proc=reader, period=period)


@arg('query', help='输入查询条件')
def main(query):
    header='机构','部门','姓名','职务','办公电话','传真','手机','电子邮件'
    ver = get_param_ver('txl')
    ver = ver and ver[0]
    print('Version:', ver)
    if R / r'1[3578]\d{1,9}' == query:
        sql = f'select * from txl where mobile like "{query}%" '
    elif R / r'9\d{3}' == query:
        sql = f'select * from txl where tel like "%8765{query}" '
    elif R / r'\d{1,}' == query:
        sql = f'select * from txl where tel like "%{query}%" '
    elif R / r'[A-Za-z].*' == query:
        sql = f'select * from txl where email like "%{query}%" '
    else:
        sql = f'select * from txl where name like "%{query}%" or br like "%{query}%"'
    for r in fetch(sql):
        tprint(zip(header, r), {0: '10'})
        print('\n')
