# 项目：   工作平台
# 模块：   柜员表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-10-31 14:37
# 修订：2019-12-13 16:51 更新个别字段的显示

from orange.xlsx import Header
from orange import Path, Data
from gmongo.params import get_ver
from gmongo.params import load_file, ROOT, fetchone, fetch, show_version
from orange import R, arg, tprint
from orange.utils.sqlite import fetchvalue, fprint

POST = (
    'R01:交易发起岗 R02:前台授权岗 R03:凭证管理岗 R04:分中心授权岗 '
    'R05:权限申请发起岗 R06:权限管理岗 R07:审查比对岗 R08:人工验印岗 '
    'R09:后台录入岗 R10:附加要素补录岗 R11:后台授权岗 R12:业务监测岗 '
    'R13:异常授权岗 R14:异常处理岗 R15:权限管理授权岗 R16:审查复核岗 '
    'R17:附加要素复核岗 R18:数据录入岗 R19:数据复核岗 R20:验票与保管岗 '
    'R21:审查岗 R22:信用卡审查岗 R41:放款受理人 R42:放款审核人 R43:放款核准人 '
    'R44:放款复核人 R45:业务审核岗 R51：审计岗'
).split()


def show_teller(sql, arg):
    header = '柜员号，姓名，电话，柜员级别，柜组，机构号，员工号，执行交易组，转账限额，现金限额，认证类型，状态，屏蔽交易，岗位性质，启用日期，停用日期，交易币种，发起交易组，证件种类，证件号码，是否运营人员'.split(
        '，')
    for tlr in fetch(sql, arg):
        tlr = list(tlr)
        tlr[3] = {
            '0': '0-经办',
            '1': '1-主办',
            '2': '2-主管'
        }.get(tlr[3])
        tlr[-11] = {'0': '0-密码', '1': '1-指纹'}.get(tlr[-11])
        tlr[-8] = {
            '0': '0-非管库员',
            '1': '1-管库员',
            '2': '2-机器柜员',
            '3': '3-行外人员'
        }.get(tlr[-8])
        tlr[-3] = {'1': '1-身份证'}.get(tlr[-3], tlr[-3])
        gw = tlr.pop(7)
        tprint(zip(header, tlr), {0: '20'})
        g = []
        jndj = set()
        for i, y in enumerate(gw.split(',')):
            if i % 2 == 0 and y:
                x = POST[i//2]
                v = fetchvalue(
                    f"select group_concat(memo,'，') from eddj where code in ('{y[:2]}','{y[2:]}')")
                g.append((x, v))
            elif i % 2 == 1:
                jndj.add(y)

        tprint(g, {0: '20'})
        jndj.remove('')
        print('技能等级：          ', *jndj)


def list_teller(cond, arg=[]):
    print('柜员号    姓名                员工号     机构    状态')
    tprint(
        fetch(f'select id,name,userid,branch,zt from teller where {cond} order by id',
              arg), {
                  0: '8',
                  1: '20',
                  2: '8',
                  3: '10'
        })


def teller_check():
    print('密码用户列表')
    sql = 'rzlx="0" and substr(zt,1,1) not in ("3","4") and gwxz <> "2" '
    list_teller(sql)
    print('\n同一机构多个柜员号（员工号）')
    sql = (
        'select userid,branch,group_concat(name),group_concat(id)from teller '
        'where substr(zt,1,1) not in ("3","4") and gwxz <> "2"'
        'group by userid,branch '
        'having count(id)>1')
    for r in fetch(sql):
        print(*r)

    print('\n同一员工号多个姓名')
    sql = (
        'select userid,group_concat(name) from '
        '(select distinct userid,name from teller where substr(zt,1,1) not in ("3","4") and gwxz <> "2")'
        'group by userid '
        'having count(name)>1')
    for r in fetch(sql):
        print(*r)


query_sql = '''
select id,name,telephone,
case grade when "0" then "0-经办" when "1" then "1-主办" when "2" then "2-主管" end,
[group],
userid,post,zxjyz,zzxe,xjxe,
case rzlx when "0" then "0-密码" when "1" then "1-指纹" end,
case substr(zt,1,1) when "1" then "1-签到" when "2" then "2-签退" when "3" then "3-临时停用"
when "4" then "4-永久停用" when "5" then "5-轧账" when "6" then "6-临时签退" end,
pbjy,
case gwxz when "0" then "0-非管库员" when "1" then "1-管库员" when "2" then "2-机器柜员" when "3" then "3-行外人员" end,
qyrq,zzrq,jybz,fqjyz,sfyy,
case zjlx when "1" then "1-居民身份证" else "2-其他" end,
zjhm
from teller
where branch=?
order by id
'''


def conv(row):
    posts = []
    jn = ""
    row = list(row)
    for i, post in enumerate(row[6].split(',')):
        if post:
            if i % 2 == 0:
                posts.append(f"{POST[i//2]}：{post}")
            else:
                jn = post[2:]
        row[6] = "\n".join(posts)
    return [*row, jn]


def export_teller(branchs):
    captial = ""
    Ver = fetchvalue('select ver from LoadFile where name="teller" ')
    with Path(f'~/Documents/业务检查用柜员表（截至{Ver}）.xlsx').write_xlsx(force=True)as book:
        for br in branchs.split(','):
            if captial and len(br) < 9:
                br = captial[:-len(br)]+br
            name = fetchvalue('select mc from ggjgm where jgm=?', [br])
            if not name:
                continue
            book.add_table(
                sheet=f'{br}-{name}',
                data=Data(fetch(query_sql, [br]), converter=conv),
                columns=[
                    Header('柜员号', 11, 'normal'),
                    Header('姓名', 15, 'normal'),
                    Header('电话', 12, 'normal'),
                    Header('柜员级别', 12, 'normal'),
                    Header('柜组', 9, 'normal'),
                    Header('工号', 9, 'normal'),
                    Header('岗位', 25, 'normal'),
                    Header('执行交易组', 80, 'normal'),
                    Header('转账限额', 12, 'normal'),
                    Header('现金限额', 12, 'normal'),
                    Header('认证类型', 10, 'normal'),
                    Header('状态', 11, 'normal'),
                    Header('屏蔽交易', 30, 'normal'),
                    Header('岗位性质', 12, 'normal'),
                    Header('启用日期', 12, 'normal'),
                    Header('终止日期', 12, 'normal'),
                    Header('交易币种', 20, 'normal'),
                    Header('发起交易组', 45, 'normal'),
                    Header('是否运营人员', 12, 'normal'),
                    Header('证件类型', 15, 'normal'),
                    Header('证件号码', 19, 'normal'),
                    Header('技能等级', 8, 'normal'),
                ]
            )
            captial = br
        print('导出文件成功！')


@arg('query', nargs='?', help='查询条件')
@arg('-c', '--check', action='store_true', help='柜员表校验')
@arg('-e', '--export', nargs='?', dest='branchs', help='导出指定机构柜员，格式为')
def main(query=None, check=False, branchs=None):
    print(f'数据版本：{get_ver("teller")}')
    if query:
        if R / r'\d{5}' == query:
            show_teller('select * from teller where id=?', [query])
        elif R / r'[A-Z]{1,2}\d{4}' == query:
            list_teller('userid=?', [query])
        elif R / r'\d{9}' == query:
            list_teller(f'branch={query} and substr(zt,1,1) not in("3","4")')
        else:
            list_teller(f'name like "{query}%"')
    if check:
        teller_check()
    if branchs:
        export_teller(branchs)
