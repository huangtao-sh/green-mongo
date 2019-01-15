# 项目：   工作平台
# 模块：   支付报表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-15 21:59

from asyncio import run
from orange.sqlite import db_config, execute, executescript, find, findone, executemany, connect
from orange import Path, HOME

sql = '''
create table if not exists LoadFile(
    filename text primary key,
    mtime   int
);

create table if not exists PaymentData(
    subno text,
    at text,
    ac text,
    "in" text,
    dn text,
    vv real,
    vv2 real,
    primary key(subno,at,ac,"in",dn)
);
'''


async def checkload(filename, loader):
    file = Path(filename)
    a = await findone('select mtime from LoadFile where filename=?', [str(file)])
    if not a or a[0] < file.mtime:
        await loader(filename)
        await execute('insert into LoadFile values(?,?)', [str(file), file.mtime])
    else:
        print(f'{file} has been loaded, skipped!')

db_config('zfbbtest')


async def loadfile(filename):
    print(filename, 'proced')


async def main():
    async with connect():
        await executescript(sql)
        await checkload(HOME/'abc.txt', loadfile)
        await checkload(HOME/'abc.txt', loadfile)
        for r in await find('select * from LoadFile'):
            print(*r)
        await execute('delete from LoadFile')

run(main())
