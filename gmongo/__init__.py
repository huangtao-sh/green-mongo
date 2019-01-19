# 项目：工作平台
# 模块：数据库模型
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-25 18:53

from .__version__ import version as __version__
from orange import R, Path, HOME
from .utils import checkload, procdata
from orange.utils.sqlite import db_config, execute, executemany, executescript, executefile,\
    find, findone, findvalue, trans

WORKPATH = Path('~/Documents/工作')

__all__ = '__version__', 'R', 'Path', "WORKPATH", "checkload", "HOME"
