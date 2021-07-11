# 项目：   参数管理程序
# 模块：   导入数据模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2021-07-10 08:22
from .loadzip import loadzip
from orange import HOME, R, datetime, Data, includer, mapper, Path
from .loader import Loader, loadcheck
from orange.utils.sqlite import tran, executefile, fetchvalue, execute, executemany, fetch

Downloads = HOME/'Downloads'
Canshu = HOME/'Documents/参数备份'
Ver = R/r'\d+'


@mapper
def conv(row: list) -> list:
    row[10] = "-".join([row[10][:4], row[10][4:6], row[10][6:8]])
    return row


@tran
def load_yyzg():
    path = Downloads.find('营业主管信息*.xls*')
    ver = Ver.extract(path.pname,)
    loadcheck('yyzg', path.name, path.mtime, ver)
    loader = Loader('yyzg', 11, includer(
        2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 11), conv)
    loader.data = path.sheets(0)[1:]
    loader.load()


@tran
def load_nkwg():
    path = Downloads.find('resultReg*.xls*')
    ver = datetime(path.mtime) % '%F'
    loadcheck('nkwg', path.name, path.mtime, ver)
    loader = Loader('nkwg', 29, includer(*range(29)))
    loader.data = path.sheets(0)
    loader.load()


@tran
def load_kemu():
    path = (Canshu/'科目说明').find('会计科目说明*.txt')
    ver = Ver.extract(path.pname)
    loadcheck('kemu', path.name, path.mtime, ver)
    loader = Loader('kemu', 3)

    def read():
        KEMU = R / r'(?P<_id>\d{4,6})\s*(?P<name>\w*)'
        BLANKS = R / r'第.章。*', R / r'本科目为一级科目.*'
        AcPattern = R / r'\d{1,6}'
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
        for row in data.values():
            row[-1] = "\n".join(row[-1])
            yield row
    loader.data = read()
    loader.load()


@tran
def load_djr():
    path = (Canshu/'考核记录人').find('考核记录人.xls*')
    ver = Ver.extract(path.pname)
    loadcheck('djr', path.name, path.mtime, ver)
    loader = Loader('djr', 2)
    loader.data = path.sheets(0)[1:]
    loader.load()


loads = [
    load_yyzg,
    load_nkwg,
    load_kemu,
    load_djr,
]


@tran
def CreateNbzhhz():
    sql = """insert into nbzhhz
select b.jglx,a.bz,a.km,cast(substr(a.zh,19,3)as int) as xh,a.hm,sum(abs(a.ye)),
max(a.sbfsr) from nbzh a
left join ggjgm b on a.jgm=b.jgm
where a.zhzt like "0%"
group by b.jglx,a.km,a.bz,xh;"""
    verNbzh = fetchvalue("select ver from LoadFile where name=?", ["nbzh"])
    verHz = fetchvalue("select ver from LoadFile where name=?", ["nbzhhz"])
    if verNbzh != verHz:
        execute("delete from nbzhhz")
        execute(sql)
        execute("insert or replace into LoadFile(name,ver) values(?,?)", [
                "nbzhhz", verNbzh])
        print("创建内部账户汇总完成！")
    else:
        print("无需创建内部账户汇总")


@tran
def CreateBranch():
    sql = """
select jgm,mc,case when substr(jgm,1,2) in ("33","34") then "9"||substr(jgm,2,8)  -- 浙江省机构排最后
when jgm="653000000" then "650000000"                       -- 重庆分行提前
else jgm end as brorder 
from ggjgm where jgm like "%000" and jglx="10" and jgm not in("998930000"); -- 剔除香港分行
"""
    verjgm = fetchvalue("select ver from LoadFile where name=?", ["ggjgm"])
    verbr = fetchvalue("select ver from LoadFile where name=?", ["branch"])
    if verjgm != verbr:
        execute("delete from branch")
        Pattern = R/r'(浙商银行)?(股份.*?公司)?(.*?分行)'
        data = Data(fetch(sql), converter=lambda row: [
                    row[0], Pattern.extract(row[1], 3), row[2][:4]])
        executemany('insert into branch values(?,?,?)', data)
        execute("insert or replace into LoadFile(name,ver) values(?,?)", [
                "branch", verjgm])
        print("创建分行汇总完成！")
    else:
        print("无需创建分行汇总")


def loadall():
    loadzip()
    for load in loads:
        try:
            load()
        except Exception as e:
            print(e)
    CreateNbzhhz()
    CreateBranch()
