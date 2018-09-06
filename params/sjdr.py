# 项目：工作平台
# 模块：数据导入模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-05-05 14:31

from orange import Path
from .bz import GgBzb, GgQzb
from .zh import ZhangHu, AcTemplate
from orange.coroutine import run
from trans import JyGangwei, JyJiaoyi, JyMenu, JyCdjy, JyShbs
from .accounting import Accounting
from .jgm import GgJgm
from .branch import Branch
from .dzzz import GgDzzz
from glemon import FileImported
from contextlib import suppress

ROOT = Path('~/Documents/工作/参数备份')
CANSHU = max(ROOT.glob('运营管理*'))
Files = {x.pname: x for x in CANSHU.rglob('*.*')}  # 列出参数文件清单

Coros = (
    (AcTemplate, {'filename': Files.get('ggnbzhmb'),
                  'dupcheck': True, 'drop': True, 'encoding': 'gbk'}),
    (ZhangHu, {'filename': Files.get('fhnbhzz'),
               'dupcheck': True, 'drop': True}),
    (JyJiaoyi, {'filename': Files.get('transactions_output'),
                'dupcheck': True, 'drop': True}),
    (JyShbs, {'filename': Files.get('是否需要事后补扫'),
              'dupcheck': True, 'drop': True}),
    (JyCdjy, {'filename': Files.get('是否校验磁道信息'),
              'dupcheck': True, 'drop': True}),
    (GgJgm, {'filename': Files.get('ggjgm'), 'dupcheck': True, 'drop': True}),
    (GgBzb, {'filename': Files.get('ggbzb'), 'dupcheck': True, 'drop': True}),
    (GgQzb, {'filename': Files.get('ggqzb'), 'dupcheck': True, 'drop': True}),
    (JyMenu, {'filename': max((ROOT / '交易菜单').glob('menu*.xml')),
              'dupcheck': True, 'drop': True}),
    (JyGangwei, {'filename': max((ROOT / '岗位与交易组').glob('*.xls')),
                 'dupcheck': True, 'drop': True}),
    (Accounting, {'filename': max((ROOT / '科目说明').glob('*.txt')),
                  'dupcheck': True, 'drop': True}),
    (Branch, {'filename': max((ROOT / '全行通讯录').glob('全行通讯录*.xls*')),
              'dupcheck': True, 'drop': True}),
    #(GgDzzz, {'filename': Files.get('DZZZCSB'), 'dupcheck': True, 'drop': True})
)


async def _import(coro):
    cls, kw = coro
    try:
        with suppress(FileImported):
            await cls.amport_file(**kw)
    except Exception as e:
        print('%s 导入失败，错误：%s' % (cls.__name__, e))


def sjdr():
    print('开始数据导入')
    print('导入数据目录：%s' % (ROOT))
    print('导入参数目录：%s' % (CANSHU))
    run(*list(map(_import, Coros)))


if __name__ == "__main__":
    sjdr()
