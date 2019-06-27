from itertools import islice
from gmongo import fetch, db_config
from gmongo import db_config, executemany, executescript, fetch, fetchone, loadcheck, HOME, execute, fetchvalue
from orange.utils.sqlite import insert
from orange.xlsx import Header
from orange import Path, split

db_config('d:/内部账户/nbzh.db')


def zhidingzhanghu(km: str, xh: int):
    zh = f'{km}{xh:03d}'
    print(f'查询指定账户：{zh}')
    for r in fetch('select * from nbzh where substr(zh,13,9)=?', [zh]):
        print(*r)


def export_dump():
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

    with Path('D:/OneDrive/工作/当前工作/20190614内部账户模板清理/内部账户模板清理.xlsx').write_xlsx(
            force=True) as book:
        book.add_table('A1',
                       '内部账户模板删除',
                       data=data2,
                       columns=[
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
                           Header('备注', width=9.88)
                       ])


createsql = '''
create table if not exists nbzh(
        zh text primary key,    --  账号
        jgm text,               --  机构码
        bz text,                --  币种
        hm text,                --  户名
        km text,                --  科目
        yefx text,              --  余额方向 1:借 2:贷 0:两性 记帐以借方为准
        ye real,                --  余额
        qhe real,               --  切换额
        zrye real,              --  昨日余额
        zcll real,              --  正常利率
        fxll real,              --  罚息利率
        fdll real,              --  浮动利率系数
        lxjs real,              --  利息积数
        fxjs real,              --  罚息积数
        qxrq text,              --  起息日期
        khrq text,              --  开户日期
        xhrq text,              --  销户日期
        sbfsr text,             --  上笔发生日期
        mxbs int,               --  明细笔数
        zhzt text,              --  账户状态
        /*
第一位:销户状态
0:未销户
1:已销户
9:被抹帐
第二位:冻结状态
0:未冻结
1:借方冻结
2:贷方冻结
3:双向冻结
第三位:收付现标志
0:不可收付现
1:可收付现
jxbz char 2 N.N 计息标志
第一位:计息方式
0:不计息
1:按月计息
2:按季计息
3:按年计息
第二位:入帐方式
0:计息不入帐
1:计息入帐收息
2:计息入帐付息
        */
        jxbz text,  -- 计息标志
        sxzh text,  -- 收息账号
        fxzh text,  --  付息账号
        tzed real,  -- 透支额度
        memo text); -- 备注
    create table if not exists branch(
        branch text primary key,
        type text
    );

create table if not exists ggnbzhmb (
    jglx text,
    -- 机构类型，00-总行清算中心，01-总行营业部，10-分行清算中心，11-分行营业部，12-支行营业部
    whrq date,
    -- 维护日期
    kmh text,
    -- 科目号
    bzh text,
    -- 币种号  00-所有币种，B1-常用币种
    zhxx int,
    -- 账户序号
    hmgz int,
    -- 户名规则 0-按科目，1-指定名称
    hm text,
    -- 指定户名
    tzed real,
    -- 透支额度
    zhzt text,
    -- 账户状态 第1位：0-开户，1-销户；第二位：0-正常，1-借冻，2-贷冻，3-双冻；第三位：0-不可收付现，1-可收付现
    jxbz text,
    -- 计息标志 第1位：0-不计息，1-按月，2-按季，3-按年；第2位：0-计息不入账，1-入收息，2-入付息
    primary key (jglx, kmh, bzh, zhxx)
);
'''


def load():
    executescript(createsql)
    loadnbzh()
    loadbranch()
    loadmb()


def loadnbzh():
    @loadcheck
    def _(path):
        execute('delete from nbzh')
        for row in split(path.iter_csv(errors='ignore', encoding='gbk'),
                         10000):
            insert('nbzh', row)

    path = (HOME / 'OneDrive/工作/参数备份').find('fhnbhzz.del')
    return _(path)


def loadmb():
    path = (HOME / 'OneDrive/工作/参数备份').find('ggnbzhmb.del')

    @loadcheck
    def _(path: Path):
        execute('delete from ggnbzhmb')
        insert(
            'ggnbzhmb',
            path.iter_csv(encoding='gbk',
                          errors='ignore',
                          converter={
                              0: str.strip,
                              6: str.strip,
                          }))
        print(f'{path.name} 导入成功')

    return _(path)


def loadbranch():
    @loadcheck
    def _(path):
        execute('delete from branch')
        insert('branch',
               path.iter_csv(encoding='gbk', errors='ignore', columns=(0, 15)))

    path = (HOME / "OneDrive/工作/参数备份").find('ggjgm.del')
    return _(path)


header = [
    Header('账号', 24.38),
    Header('序号', 10),
    Header('户名', 45),
    Header('余额', 12, format='currency'),
    Header('账户状态', 9.38)
]

accounts = ['223099001']
account = ','.join('"%s"' % ac for ac in accounts)
# print(account)
data = fetch('select zh,substr(zh,13,9) as ac,hm,ye,zhzt  from nbzh '
             f'where ac in ({account}) '
             'and substr(zhzt,1,1)="0" '
             'order by ac,zh')

# with (HOME/'OneDrive/工作/当前工作/20190422参数维护/销户清单.xlsx').write_xlsx(force=True)as book:
#    book.add_table("A1", '批量销户清单', data=data, columns=header)
exit()
accounts = [row[0] for row in data]
print(len(accounts))
exit()
for i, rows in enumerate(split(accounts, 1000), 1):
    (HOME /
     f'OneDrive/工作/当前工作/20190422参数维护/批量销户清单/批量销户清单-{i:02d}.txt').lines = rows

exit()
'''
for row in fetch('select substr(a.zh,13,9) as ac,b.type as tp,max(a.sbfsr)as sbfsr,'
                'max(a.ye)as ye,a.hm from nbzh a '
                'join branch b on a.jgm=b.branch '
                'group by ac,tp '
                'order by ac,tp'
                ):
    print(*row,sep='|')
'''
r = fetchone('select * from nbzh where zh=?', ['331001000192180020017'])
if r:
    print(*r)
'''
# 总行开立的账户

zhzh=set()
for r in fetch(select distinct substr(zh,13,9)from nbzh where jgm=331000000):
    zhzh.add(r[0])
fhzh=set()
for r in fetch(select distinct substr(zh,13,9)from nbzh where jgm!=331000000):
    fhzh.add(r[0])

print(仅在总行开立账户)
print(*sorted(zhzh-fhzh),sep=\n)
print(仅在分行开立账户)
print(*sorted(fhzh-zhzh),sep=\n)

for r in fetch(select substr(zh,13,9)as ac,max(sbfsr)as sbfsr,max(ye)as ye from nbzh group by ac having sbfsr<20161231 order by zh):
    print(*r)

# for r in fetch(select substr(zh,13,9)as zh,sum(ye)as yehj,max(sbfsr) as zhrq from nbzh where ye=0 group by km having yehj=0):
#    print(*r)
'''
