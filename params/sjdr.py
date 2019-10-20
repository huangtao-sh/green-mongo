# 项目：工作平台
# 模块：数据导入模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-05-05 14:31
# 修订：2018-09-06 忽略已导入文件的异常
# 修订：2018-10-31 20:47 增加 dengji 的处理

from orange import Path
from .bz import GgBzb, GgQzb
from .zh import ZhangHu, AcTemplate, GgKmzd
from trans import JyGangwei, JyJiaoyi, JyMenu, JyCdjy, JyShbs
from .accounting import Accounting
from .jgm import GgJgm
from .branch import Branch, Contacts
from .dzzz import GgDzzz
from glemon import FileImported, profile
from contextlib import suppress
from .user import Teller
from .pzzl import Pzzl
from .jszh import GgJszh
from .dengji import EduDengji
from .zhxxbm import Zhxxbm
from gmongo.params.loaddata import load_files

ROOT = Path('~/OneDrive/工作/参数备份')
CANSHU = ROOT.find('运营管理*')
Files = {x.pname: x for x in CANSHU.rglob('*.*')}  # 列出参数文件清单
LoadFiles = (
    (JyShbs, Files.get('是否需要事后补扫')),
    (JyCdjy, Files.get('是否校验磁道信息')),
    (GgBzb, Files.get('ggbzb')),
    (GgQzb, Files.get('ggqzb')),
    (Teller, Files.get('users_output')),
    (GgJgm, Files.get('ggjgm')),
    (GgDzzz, Files.get('DZZZCSB')),
    (AcTemplate, Files.get('ggnbzhmb')),
    (GgKmzd, Files.get('ggkmzd')),
    (Pzzl, Files.get('ggpzzl')),
    (GgJszh, Files.get('ggjszh')),
    (JyJiaoyi, Files.get('transactions_output')),
    (ZhangHu, Files.get('fhnbhzz')),
    (JyMenu, (ROOT / '交易菜单').find('menu*.xml')),
    #(Contacts, (ROOT / '通讯录').find('通讯录*.xls')),
    (Branch, (ROOT / '分行表').find('分行顺序表.xlsx')),
    (JyGangwei, (ROOT / '岗位与交易组').find('岗位及组*.xls')),
    (EduDengji, (ROOT / '额度登记配置').find('额度登记配置*.xls')),
    (Accounting, (ROOT / '科目说明').find('*.txt')),
    (Zhxxbm, Files.get('ggxxbmdzb')),
)


def sjdr():
    print('开始数据导入')
    print('导入数据目录：%s' % (ROOT))
    print('导入参数目录：%s' % (CANSHU))
    yf = str(CANSHU)[-7:]
    profile.param_yf = yf
    print(f'当前月份：{yf}')
    for cls, filename in LoadFiles:
        if filename:
            with suppress(FileImported):
                print(f'开始处理 {cls.__name__}')
                result = cls.loadfile(filename)
                print(f'{cls.__name__} 处理成功，共导入数据 {result.inserted_count}条')

    load_files()


if __name__ == "__main__":
    sjdr()
