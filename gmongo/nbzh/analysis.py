# 项目：   工作平台
# 模块：   内部账户分析
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-06-27 14:14

from orange.utils.sqlite import fetch, fetchone, fetchvalue, db_config, execute
from orange.xlsx import Header
from orange import HOME, now, datetime, Path
from . import ZTZC, ZHXH
from orange.utils.log import info

Headers = [
    Header('机构类型', width=9.88),
    Header('日期', width=9.88),
    Header('科目'),
    Header('币种'),
    Header('序号'),
    Header('户名规则'),
    Header('户名', width=44),
    Header('透支额度', width=19.88, format='currency'),
    Header('初始状态'),
    Header('计息标志'),
    Header('清理原因', width=45)
]


def clear_nbzhmb():
    result = execute(
        'update ggnbzhmb set zt=2,memo="已有00模板" '
        'where zt=0 and bz <>"00" and '
        'exists (select jglx from ggnbzhmb b '
        'where ggnbzhmb.jglx=b.jglx and ggnbzhmb.km=b.km and ggnbzhmb.xh=b.xh and b.bz="00") '
    )
    info('与00模板重复数：%d', result.rowcount)
    result = execute(
        'update ggnbzhmb set zt=2,memo="已有B1模板" '
        'where zt=0 and bz not in ("00","B1") and '
        'exists (select jglx from ggnbzhmb b '
        'where ggnbzhmb.jglx=b.jglx and ggnbzhmb.km=b.km and ggnbzhmb.xh=b.xh and bz="B1") '
    )
    info('与B1模板重复数：%d', result.rowcount)

    count = fetchvalue('select count(*) from ggnbzhmb where zt=2')
    if count:
        with Path('内部账户模板清理.xlsx').write_xlsx(force=True) as book:
            book.add_table(
                'A1',
                '删除模板',
                data=fetch(
                    'select jglx,whrq,km,bz,xh,hmgz,hm,tzed,zhzt,jxbz,memo from ggnbzhmb '
                    'where zt=2 '
                    'order by km,xh,jglx'),
                columns=Headers)
    print(f'导出文件成功，记录数：{count}')


def export_all():
    sql = ('select jglx,whrq,km,bz,xh,hmgz,hm,tzed,zhzt,jxbz '
           'from ggnbzhmb '
           'order by km,xh,jglx ')
    with Path('内部账户批量开立模板.xlsx').write_xlsx(force=True) as book:
        book.add_table('A1', '全量模板', data=fetch(sql), columns=Headers[:-1])
        print('导出全量模板成功')


def useless_nbzhmb(book, begin_date):
    '截止日期后未使用账户'
    useless_data = []
    for zhxh, rq in fetch(
            f'select {ZHXH},max(sbfsr) as zdfsr from nbzh '
            f'where ({ZTZC}) '
            'group by zhxh '
            # 最大的发生日期大于起始日期，最大余额等于0
            'having max(ye)=0.0 and (zdfsr <= ?) '
            'order by zhxh',
        [begin_date]):
        zh, xh = zhxh[:6], int(zhxh[6:])
        bz = f'所有账户余额为0，且最近发生日期：{rq}'
        for row in fetch('select * from ggnbzhmb where kmh=? and zhxx=?',
                         [zh, xh]):
            useless_data.append([*row, bz])
    book.add_table('A1', '满一年使用账户', data=useless_data, columns=Headers)
    print('生成不再使用模板成功')
