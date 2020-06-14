# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20
# 修订：2018/07/29 程序调整

from collections import defaultdict
from orange import Path, R, arg, cstr, datetime, now
from orange.utils.sqlite import connect, execute, executemany, find, findone,\
    executescript, trans, Values
import json

ROOT = Path('~/OneDrive/工作/工作档案/履职报告')
if not ROOT:
    ROOT.ensure()


def _get_period(date: str) -> str:
    date = datetime(date).add(days=-25)
    return date % ('%Y-%m')


def read_yyzg():
    path = ROOT.find('营业主管信息.*')
    print(f'导入营业主管文件 {path}')
    for row in path.sheets(0)[1:]:
        yield *row[:8], row[9], row[11], row[10]


def load_file():
    bg = []
    files = ROOT.glob('会计履职报告*.xls')
    if not files:
        print('当前目录无文件')
    else:
        filename = max(files)
        print('当前导入文件：%s' % (filename))
        data = []
        for rows in filename.iter_sheets():
            rows = rows[-1]
            if len(rows) < 1:
                continue
            title = None
            for row in rows[1:]:
                if row[0]:
                    if title != row[0]:
                        title = row[0]
                        nr = [row[19:]]
                        data.append([title, _get_period(row[5]), row[2], row[4]+row[3], row[5],
                                     row[6], row[7], row[8], row[10], row[11], row[12], row[13], row[14],
                                     row[16], row[17], nr])
                        bg.append([title, _get_period(row[5]),
                                   row[2], row[4], row[5], row[18]])
                    else:
                        nr.append(row[19:])
        data2 = []
        for r in data:
            r[-1] = json.dumps(r[-1])
            data2.append((r[3], r[2]))
    with trans():
        sql = f'insert or replace into report values({",".join(["?"]*16)})'
        cur = executemany(sql, data)
        sql = 'insert or ignore into branch values(?,?)'
        executemany(sql, data2)
        print(f'已导入数据：{cur.rowcount}')
        execute('delete from yyzg')
        executemany(f'insert into yyzg {Values(11)}', read_yyzg())
        executemany(f'insert or replace into bg {Values(6)}', bg)
