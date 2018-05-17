# 项目：工作平台
# 模块：定制转账参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-14

from glemon import P, Document
from orange import arg


class GgDzzz(Document):
    # 定制转账编号，定制转账序号，操作机构号，
    # 操作机构类型：0全部，1总行，2分行，3分行营业部，4支行营业部，5分支行营业部
    # 操作机构所在分行、操作机构例外机构
    # 币种
    # 借贷标志：1-借，2-贷
    # 账户所在机构码
    # 账户所在机构类型：0全部，1总行，2分行，3分行营业部，4支行营业部，5分支行营业部
    # 账户所在分行，账户机构例外机构，科目，账户序号，
    # 是否允许跨机构：0不允许，1允许
    # 是否允许红字：0不允许，1允许

    _projects = 'bh', 'xh', 'mc', 'czjg', 'czjglx', 'czjgfh', 'czjglw', 'bz', 'jdbz', 'zhjglx', 'zhjgfh', 'zhjglw', 'km', 'zhxh', 'kjg', 'yxhz'

    @classmethod
    @arg('-e', '--export', action='store_true', help('导出参数表')
    def main(cls, export=False):
        for obj in cls.objects:
            print(*obj.values('bh', 'xh'))
