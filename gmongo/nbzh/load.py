# 项目：   工作平台
# 模块：   内部账户
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-06-27 08:59
# 修改：使用load_file 来导入文件
from orange import HOME, R
from gmongo.params import load_file, transaction, executescript


def loadnbzh():
    return load_file(path=(HOME / 'OneDrive/工作/参数备份').find('fhnbhzz.del'),
                     table='nbzh',
                     drop=True,
                     encoding='gbk',
                     errors='ignore')


@transaction
def create_hz():
    executescript(
        'delete from nbzhhz;'
        'insert into nbzhhz '
        'select b.jglx,a.bz,a.km,cast(substr(a.zh,19,3)as int) as xxh,a.hm,sum(abs(a.ye)), '
        'max(a.sbfsr) from nbzh a '
        'left join ggjgm b on a.jgm=b.jgm '
        'where a.zhzt like "0%" '
        'group by b.jglx,a.km,a.bz,xxh;')
    print('创建内部账户统计表成功！')


KEMU = R / r'(?P<_id>\d{4,6})\s*(?P<name>\w*)'
BLANKS = R / r'第.章。*', R / r'本科目为一级科目.*'
AcPattern = R / r'\d{1,6}'


def proctxt(path):
    data = {}
    kemu = None
    for line in path.lines:
        line = line.strip()
        if any([blank.match(line) for blank in BLANKS]):
            continue
        elif KEMU.match(line):
            kemu = KEMU.match(line).groupdict()
            description = []
            data[kemu['_id']] = [kemu['_id'], kemu['name'], description]
        else:
            if kemu:
                description.append(line)
    for km, name, desc in data.values():
        yield km, name, "\n".join(desc)


def loadkemu():
    path = (HOME / 'OneDrive/工作/参数备份/科目说明').find('会计科目说明*.txt')
    return load_file(path, 'kemu', proc=proctxt, period=path.pname[-6:])


loadkemu()
