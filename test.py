from orange.utils.data import filterer, converter
from orange import Path, R, limit
from orange.xlsx import Header

path = Path('~/OneDrive/工作/参数备份').find('users_output.csv')
def read(path):
    for row in limit(path.iter_csv(),10):
        yield [*row[:3],*row[4:8],','.join(map(str.strip,row[8:-25])),row[-25],*row[-23:-20],*row[-10:-3],*row[-2:]]

for r in limit(read(path),1):
    r=[x.strip() for x in r]
    print(len(r))
    print(*tuple(zip(range(22),r)),sep='\n')