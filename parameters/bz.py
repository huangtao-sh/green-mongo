# 项目：工作平台
# 模块：币种相关参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-06-23 09:43

from orange import command, arg, R
from glemon import Document, P


class GgBzb(Document):
    _projects = 'bz', 'gbh', 'bzmc', 'ywsx', 'hltzcs', 'hltzrq', 'ws', 'qybz', 'qyrq', 'zyrq', 'dgqygz'

    @classmethod
    @command(description='币种代码查询程序')
    @arg('codes', metavar='bz', nargs='*', help='币种代码列表')
    @arg('-d', '--detail', action='store_true', help='显示详细信息')
    def main(cls, codes=None, detail=False):
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
            for d in cls._get_collection().find(filter_):
                if not detail:
                    print('%s\t%s\t%s' % (d['bz'], d['ywsx'], d['bzmc']))
                else:
                    print('\n代码      ：%s' % (d['bz']))
                    print('英文缩写  ：%s' % (d['ywsx']))
                    print('名称      ：%s' % (d['bzmc']))
                    print('国标号    ：%s' % (d['gbh']))
                    print('启用标志  ：%s' % (d['qybz']))
                    print('启用日期  ：%d' % (d['qyrq']))


class GgQzb(Document):   # 公共券别表
    _projects = 'bz', 'code', 'name', 'amount'


if __name__ == '__main__':
    GgBzb.main()
