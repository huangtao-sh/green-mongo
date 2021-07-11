# 项目：工作平台
# 模块：币种相关参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-06-23 09:43
# 修订：2018-10-27 采用 profile 来显示内容

from orange import command, arg, R

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
        objects = cls.find(filter_)
        if detail:
            objects.show_detail()
        else:
            print('代码  英文简称   币种名称')
            objects.show('bz,ywsx,bzmc', sep='    ')
    elif all:
        objs = cls.objects
        if detail:
            objs.show_detail()
        else:
            print('代码  英文简称   币种名称')
            objs.show('bz,ywsx,bzmc', sep='    ')

