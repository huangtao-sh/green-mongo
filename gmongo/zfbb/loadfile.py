# 项目： 工作平台
# 模块： 支付报表
# 作者： 黄涛
# License: GPL
# Email: huangtao.sh@icloud.com
# 创建：2019-01-15 21:59

from orange import Path, HOME, tempdir
from gmongo import checkload, execute, executescript, find, findone, executemany, executefile, loadcheck


@loadcheck
def loadfile(path):
    with tempdir() as tmp:
        Path(path).extractall(tmp)
        for f in tmp.rglob('*.zip'):
            f.extractall(tmp)
        for file in tmp.rglob('*CITY*.xml'):
            print(f'处理文件 {file.name}')
            root = file.xmlroot
            header = [root.find(key).text for key in ('SubNo', 'AT', "AC")]
            objs = []
            for rw in root.iterfind('RW'):
                data = header.copy()
                data.extend(d.text for d in rw)
                for i in range(5, len(data)):
                    data[i] = 0 if data[i] == 'NAP' else float(data[i])
                if len(data) < 7:
                    data.append(0)
                objs.append(data)
            executemany('insert or replace into PaymentData(subno,at,ac,"in",dn,vv,vv2)'
                        'values(?,?,?,?,?,?,?)', objs)
    print(f'{path.name} 文件导入成功')


def load(path):
    executefile('gmongo', 'sql/zfbb.sql')                # 建立数据库表
    for file in path.glob('*.zip'):   # 导入文件
        loadfile(file)
