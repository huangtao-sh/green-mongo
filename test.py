from orange.utils.data import filterer, converter
from orange import Path, R
from orange.xlsx import Header

path=Path('~/OneDrive/工作/参数备份').find('users_output.csv')
for r in path.iter_csv():
    print(*r)