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

db_config('~/OneDrive/db/params.db')

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


def mb_exists(zh):
    br, bz, km, xh = zh[:9], zh[9:11], zh[12:18], int(zh[18:21])
    lx = fetchvalue('select jglx from ggjgm where jgm = ?', [br])
    if lx:
        #print(lx)
        return fetchone(
            'select jglx,bzh,kmh,zhxx from ggnbzhmb where '
            'jglx=? and bzh in ("B1","00",?) and kmh=? and zhxx=? ',
            [lx, bz, km, xh])


def clear_nbzh():
    for jgm, zh, hm, khrq, ye, sbfsr, zhzt in fetch(
            'select jgm,zh,hm,khrq,ye,sbfsr,zhzt from nbzh '
            f'where ({ZTZC}) and ye=0 and not km like "7114%"  '
            'order by zh'):
        if not mb_exists(zh):
            print(jgm, zh, hm, khrq, ye, sbfsr, zhzt)


def clear_nbzhmb():
    with (HOME / 'OneDrive/工作/当前工作/20190614内部账户模板清理/内部账户模板清理.xlsx').write_xlsx(
            force=True) as book:
        dump_nbzhmb(book)
        useless_nbzhmb(book)


def useless_nbzhmb(book):
    '满三年未使用账户'
    '清理发生日期在两年前的账户'
    begin_date = f'{now().year - 2:04d}0101'
    print('开始日期：', begin_date)
    useless_data = []
    for zhxh, rq in fetch(
            f'select {ZHXH},max(sbfsr) as zdfsr from nbzh '
            f'where ({ZTZC}) '
            'group by zhxh '
            'having (zdfsr < ?) and (max(ye)=0.0) '  # 最大的发生日期大于起始日期，最大余额等于0
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