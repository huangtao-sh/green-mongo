# 项目：工作平台
# 模块：币种相关参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-06-23 09:43
# 修订：2018-10-27 采用 profile 来显示内容

from orange import command, arg, R
from glemon import Document, P


class GgBzb(Document):
    _projects = 'bz', 'gbh', 'bzmc', 'ywsx', 'hltzcs', 'hltzrq', 'ws', 'qybz', 'qyrq', 'zyrq', 'dgqygz'
    _profile = {
        '代码': 'bz',
        '英文缩写': 'ywsx',
        '币种名称': 'bzmc',
        '国标号': 'gbh',
        '启用标志': 'qybz',
        '启用日期': 'qyrq',
    }

    @classmethod
    @command(description='币种代码查询程序')
    @arg('codes', metavar='bz', nargs='*', help='币种代码列表')
    @arg('-d', '--detail', action='store_true', help='显示详细信息')
    @arg('-a', '--all', action='store_true', help='显示所有币种')
    def main(cls, codes=None, detail=False, all=False):
        if codes:
            filter_ = []
            for d in codes:
                if R / r'\d{2}' == d:
                    s = {'bz': d}
                elif R/'[a-zA-Z]{3}' == d:
                    s = {'ywsx': d}
                else:
                    s = {'bzmc': {'$regex': d}}
                filter_.append(s)
            if len(filter_) == 1:
                filter_ = filter_[0]
            else:
                filter_ = {'$or': filter_}
            for d in cls.find(filter_):
                if not detail:
                    print('%s\t%s\t%s' % (d['bz'], d['ywsx'], d['bzmc']))
                else:
                    d.show()
                    print('\n')
        elif all:
            for d in cls.objects:
                if not detail:
                    print('%s\t%s\t%s' % (d['bz'], d['ywsx'], d['bzmc']))
                else:
                    d.show()
                    print('\n')


class GgQzb(Document):   # 公共券别表
    _projects = 'bz', 'code', 'name', 'amount'


if __name__ == '__main__':
    GgBzb.main()
