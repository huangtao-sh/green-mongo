# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20
# 修订：2018/07/29 程序调整
# 修订：2020-06-15 08:15 调整未及时报送统计功能

from collections import defaultdict
from orange import Path, R, arg, cstr, datetime, now, extract
from orange.utils.sqlite import connect, execute, executemany, fetch, fetchone,\
    executescript, trans, Values, fprint
import json

ROOT = Path('~/OneDrive/工作/工作档案/履职报告')
if not ROOT:
    ROOT.ensure()


def _get_period(date: str) -> str:
    date = datetime(date).add(days=-25)
    return date % ('%Y-%m')


def read_yyzg():
    path = Path("~/Documents/参数备份/营业主管").find('营业主管信息*.*')
    print(f'导入营业主管文件 {path}')
    for row in path.sheets(0)[1:]:
        yield (*row[2:10], *row[:2], row[11])


def load_file():
    files = Path("~/Downloads").glob('会计履职报告????-??.xls*')
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
                if row[0]:  # 防止空行出现
                    if title != row[0]:
                        title = row[0]
                        nr = [row[20:]]
                        gh = extract(row[3], r"[a-zA-Z]{1,2}\d{4}")
                        data.append([title, _get_period(row[6]), row[2], gh, row[5]+row[4], row[6],
                                     row[7], row[8], row[9], row[11], row[12], row[13], row[14], row[15],
                                     row[17], row[18], row[19], nr])
                    else:
                        nr.append(row[20:])
        for r in data:
            r[-1] = json.dumps(r[-1])
    with trans():
        sql = f'insert or replace into report {Values(18)}'
        cur = executemany(sql, data)
        print(f'已导入数据：{cur.rowcount}')
        execute('delete from yyzg')
        executemany(f'insert into yyzg {Values(11)}', read_yyzg())
        print('已导入营业主管数据')
