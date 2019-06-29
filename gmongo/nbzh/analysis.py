# 项目：   工作平台
# 模块：   内部账户分析
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-06-27 14:14

from orange.utils.sqlite import fetch, fetchone, fetchvalue, db_config
from orange.xlsx import Header
from orange import HOME, now, datetime
from . import ZTZC, ZHXH

# db_config('~/OneDrive/db/params.db')

TingyongKemu = {
    '710501': '关于停用“7105再贴现及卖出票据”科目的通知',
    '710502': '关于停用“7105再贴现及卖出票据”科目的通知',
    '137021': '浙商银办【2018】12号',
    '137052': '浙商银办【2018】12号',
    '140075': '浙商银办【2018】12号',
}

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


def clear_nbzhmb(begin_date):
    with (HOME / 'OneDrive/工作/当前工作/20190614内部账户模板清理/内部账户模板清理.xlsx').write_xlsx(
            force=True) as book:
        dump_nbzhmb(book)
        useless_nbzhmb(book, begin_date)
        export_mb(book)
        tingyong_mb(book)


def tingyong_mb(book):
    data = []
    for km, bz in TingyongKemu.items():
        for row in fetch('select * from ggnbzhmb where kmh=?', [km]):
            data.append([*row, bz])
    if data:
        book.add_table('A1', '停用科目', data=data, columns=Headers)


def export_mb(book):
    sql = 'select * from ggnbzhmb order by kmh,zhxx,jglx,bzh'
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
    book.add_table('A1', '满三年未使用账户', data=useless_data, columns=Headers)
    print('生成不再使用模板成功')


def dump_nbzhmb(book):
    data = []
    for kmh, zhxx, jglx, bzh, tzed in fetch(
            'select kmh,zhxx,jglx,group_concat(bzh,","),group_concat(tzed,",") '
            'from ggnbzhmb '
            'group by kmh,zhxx,jglx '
            'order by kmh,zhxx,jglx'):
        bzh = set(bzh.split(','))
        tzed = set(tzed.split(','))
        if len(bzh) > 1:
            if '00' in bzh:
                bzh.remove('00')
                for bz in bzh:
                    data.append([kmh, zhxx, jglx, bz, '已有00模板'])
            elif 'B1' in bzh:
                bzh.remove('B1')
                for bz in bzh:
                    data.append([kmh, zhxx, jglx, bz, '已有B1模板'])

    data2 = []
    for r in data:
        row = fetchone(
            'select * from ggnbzhmb where kmh=? and zhxx=? and jglx=? and bzh=? ',
            r[:-1])
        data2.append([*row, r[-1]])
    book.add_table('A1', '重复模板', data=data2, columns=Headers)
    print('导出重复模板成功')
