from gmongo.lzbg.publish import restore, publish_wt, get_md5, update_wenti
from gmongo.lzbg import *
from orange import Path, extract

# restore()
from orange.utils.sqlite import *


@tran
def update_zt():
    root = Path(r'~/OneDrive/工作/工作档案/履职报告/进度反馈')
    for path in root.glob('*.xlsx'):
        print(path.name)
        for sheet in path.worksheets:
            data = sheet._cell_values
            for row in data[1:]:
                rq = extract(row[0], '(\d{4}年\d{2})月份', 1)
                if rq and row[9]:
                    period = f'{rq[:4]}-{rq[5:7]}'
                    bh = get_md5(row[4])
                    zt = row[9]
                    if '北京' in path.name:
                        if zt == '是':
                            zt = '已解决'
                        else:
                            continue
                    r = execute(
                        'update lzwt set status=? where bh=?', [zt, bh])
                    if r.rowcount == 0:
                        print(zt, period, bh)


update_wenti()
