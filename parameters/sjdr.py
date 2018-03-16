# 项目：工作平台
# 模块：数据导入模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-05-05 14:31

from orange import *

ROOT = Path('~/Documents/工作/参数备份')
CANSHU = max(ROOT.glob('运营管理*'))
FileList = {x.pname: x for x in CANSHU.rglob('*.*')}  # 列出参数文件清单

from .bz import *
from .zh import ZhangHu
from orange.coroutine import run
from .transaction import *
from gmongo.parameters.accounting import Accounting
from .jgm import GgJgm
from .branch import Branch

ShuJuList = ((GgBzb, FileList.get('ggbzb')),
             (GgQzb, FileList.get('ggqzb')),
             )
AioList = ((ZhangHu, FileList.get('fhnbhzz')),
           (JyJiaoyi, FileList.get('transactions_output')),
           (JyMenu, max((ROOT / '交易菜单').glob('menu*.xml'))),
           (JyShbs, FileList.get('是否需要事后补扫')),
           (JyCdjy, FileList.get('是否校验磁道信息')),
           (JyGangwei, max((ROOT / '岗位与交易组').glob('*.xls'))),
           (Accounting, max((ROOT / '科目说明').glob('*.txt'))),
           (Branch, max((ROOT / '全行通讯录').glob('全行通讯录*.xls*'))),
           (GgJgm, FileList.get('ggjgm')),
           )


async def load(coro):
    try:
        await coro
    except Exception as e:
        print(e)


def sjdr():
    print('开始数据导入')
    print('导入数据目录：%s' % (ROOT))
    print('导入参数目录：%s' % (CANSHU))
    for cls, fn in ShuJuList:
        print('处理文件：%s' % (fn))
        cls.load_files(fn)
    from parameters.zhanghu import AcTemplate
    print('导入内部账户模板')
    AcTemplate.load_files()
    aiolist = [load(cls.amport_file(fn, drop=True, dupcheck=True)) for cls, fn in AioList]
    run(*aiolist)

if __name__ == "__main__":
    sjdr()



