# 项目：   工作平台
# 模块：   清理内部账户
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-06-29 18:14

import params
from orange.utils.sqlite import fetch, fetchone, fetchvalue, tran, execute
from orange.xlsx import Header
from orange import HOME, now, datetime
from gmongo.nbzh import ZTZC, ZHXH

Headers = [
    Header('机构码', width=10),
    Header('账号', width=25),
    Header('户名', width=45),
    Header('开户日期', width=9.38),
    Header('余额', width=13, format='currency'),
    Header('上笔发生日', width=10),
    Header('账户状态', width=10)
]

sql = (
    'select a.jgm,a.zh,a.hm,a.khrq,a.ye,a.sbfsr,a.zhzt from nbzh a '
    'left join ggjgm b on a.jgm=b.jgm '  # 连接机构表，获取机构类型
    'left join ggnbzhmb c '  # 连接内部账户模板表
    'on c.jglx=b.jglx and a.km = c.kmh and c.bzh in ("00","B1",a.bz) '
    'and cast(substr(a.zh,19,3) as int )=c.zhxx '
    'where c.jglx is null and substr(a.zhzt,1,1)="0" '
    'and a.ye=0 and not km like "7114%" '
    'and a.sbfsr <=? '
    'order by a.zh ')


def clear_nbzh(rq=None):
    '''清理内部账户，清理条件：
    1、无内部账户批量开立模板
    2、余额为 0 
    3、指定日期之后，无发生
    '''
    execute('update ggnbzhmb a set zt=2,memo="已有00查模板" '
            'where zt=0 and bz <>"00" and '
            'exists (select jglx from ggnbzhmb b '
            'where a.jglx=b.jglx and a.km=b.km and a.xh=b.xh and b.bz="00" ')
    count = fetchvalue('select * from ggnbzhmb where zt=2')
    print(count)

    return
    with (HOME / 'OneDrive/工作/当前工作/20190614内部账户模板清理/内部账户清理.xlsx').write_xlsx(
            force=True) as book:
        book.add_table('A1', '内部账户清理', data=fetch(sql, [rq]), columns=Headers)
        print('导出不再使用的内部账户成功')
