# 项目：   参数管理
# 模块：   机构码表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-05-14 14:01
# 修订：2019-09-17 21:06 调整调用方式
# 修订：2020-06-15 19:21 和 go 语言的 grape 共享数据库

from orange import R, extract, arg, tprint
from orange.utils.sqlite import connect, fetchone,fprint
from contextlib import closing
from gmongo.params import get_ver


@arg('query', nargs='?', help='查询条件')
@arg('-o', '--order', nargs='?', metavar='branchs', dest='branchs', help='对指定的分行进行排序')
def main(**options):
    header = "  机构码   机构名称                                 简称        行号    类型   开立日期  分行"
    print(f'数据版本：{get_ver("ggjgm")}')
    with connect()as db:
        if query := options.get('query'):
            if R / r'\d{2}' == query:
                data = db.fetch('select * from ggjgm where jglx=?', [query])
            elif R / r'316\d{1,9}' == query:
                data = db.fetch(
                    f'select * from ggjgm where zfhh like "{query}%"')
            elif R / r'\d{3,9}' == query:
                data = db.fetch(
                    f'select * from ggjgm where jgm like "{query}%"')
            else:
                data = db.fetch(
                    f'select * from ggjgm where mc like "%{query}%"')
            if data:
                print(header)
                tprint(data, {
                    0: '9',
                    1: '<40s',
                    2: '<10s',
                })
        if brs := options.get('branchs'):
            query=" or ".join(f"mc like '%{br}%' " for br in brs.split('、'))
            sql=(
                'select group_concat(mc,"、") from '
                f'(select mc,brorder from  branch where {query} order by brorder)'
            )
            fprint(sql)
