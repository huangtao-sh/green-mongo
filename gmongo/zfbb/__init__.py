# 项目：   工作平台
# 模块：   支付报表
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-15 21:59


from orange import command, arg, Path, R, now
from gmongo import db_config, find, execute, executemany, findone, procdata, loadcheck, findvalue
from orange.utils.config import JsonConfig, YamlConfig

DefaultConfig = {
    'datapath': '~/OneDrive/文档/支付报表数据',
    'database': 'zfbb',
    'parameterfile': '~/OneDrive/文档/支付报表数据/核心指标参数.xlsx'
}
config = YamlConfig(default=DefaultConfig, filename='~/.zfbb.yaml')

db_config(config['database'])

InPattern = R/r'[0-9A-Z]{10}'


@loadcheck
def loadconfig(ConfigFile):
    if ConfigFile:
        rows = ConfigFile.sheets('报表参数')
        data = procdata(rows, mapper={
            '序号': int,
            '指标代码': None,
            '维度代码': None,
            '指标名称': None,
            '取值': int,
        })
        execute('delete from parameter')
        cur = executemany('insert into parameter values(?,?,?,?,?)', data)
        print(f'导入数据 {cur.rowcount} 条')


@command(description='支付报表程序')
@arg('-l', '--load', nargs='?', dest='path', default='NOSET', help='导入数据库文件')
@arg('-s', '--show', action='store_true', help='显示')
@arg('-c', '--config', action='store_true', help='导入参数配置文件')
@arg('-t', '--count', nargs='*', dest='xhs', metavar='xh', help='统计指标')
@arg('-r', '--report', nargs='?', dest='qc', default='NOSET', help='生成报表')
def main(path=None, show=False, xhs=None, qc=None, **options):
    if options['config']:
        loadconfig(Path(config['parameterfile']))
    if path != 'NOSET':
        path = path or Path(config['datapath'])
        from .loadfile import load
        load(path)
    if qc != 'NOSET':
        if not qc:
            qc = now() % "%Y%m"
            qc = findvalue(
                'select subno from PaymentData order by subno desc limit 1')
            if not int(qc[4:]) % 3:
                qc = qc[:4] + '-'+str((int(qc[4:])+2)//3)
            else:
                qc = '-'.join([qc[:4], qc[4:]])
        from .rpt import export
        try:
            export(qc)
        except Exception as e:
            print(e)
    if show:
        print('数据明细清单')
        print('期次\t条数')
        for r in find('select subno,count("in")as num from PaymentData group by subno order by subno'):
            print(*r, sep='\t')
    if xhs:
        for xh in xhs:
            xh, zb, dn, name, rule = findone(
                'select * from parameter where "id"=?', [xh])
            print(zb, name)
            qc = now().add(months=-1) % '%Y%m'
            sq = now().add(months=-3) % '%Y%m'
            if not rule:
                vv, vv2 = findone('select sum(vv)as vv,sum(vv2)as vv2 from PaymentData ' +
                                  'where subno=? and "in"=? and dn=? and at="CITY" group by "in" ',
                                  [qc, zb, dn])

            else:
                vv, vv2 = findone('select sum(vv)as vv,sum(vv2)as vv2 from PaymentData ' +
                                  'where subno between ? and ? and "in"=? and dn=? and at="CITY" group by "in" ',
                                  [sq, qc, zb, dn])
            print(f'值1：{vv:19,.2f}')
            print(f'值2：{vv2:19,.2f}')
