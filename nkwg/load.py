from orange import Path
from orange.utils.sqlite import executemany, tran, Values

ROOT = Path('~/Downloads')


@tran
def load_reg():
    path = ROOT.find('resultReg*.xls')
    data = path.sheets(0)[1:]
    executemany(f'insert or replace into nkwg {Values(29)}', data)
    print(f'导入文件 {path.pname} 完成')


def check_reg():
    ...
    
