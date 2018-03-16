#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-10 12:47:03
# @Author  : 黄涛 (huang.t@live.cn)
# @Link    : http://www.jianshu.com/u/3bf5919e38a7
# @Version : $Id$

from orange import *
from glemon import *


class JyGangwei(Document):
    '''交易岗位及组的设置'''
    _projects = '_id', 'name', 'gangwei'
    _mapper = 0, 1, 2

    @classmethod
    def _proc_sheet(cls, index, name, data, **kw):
        _conv = lambda x: '%02d' % (x) if isinstance(x, (int, float)) else '%s' % (x)
        if data:
            da = []
            gangwei = ['%s-%s' % (_conv(row[1]), row[2]) for row in
                       data[2:] if row]
            rows = len(data)
            for i in range(2, len(data[0])):
                d = []
                for k in range(2, rows):
                    if data[k][i]:
                        d.append(gangwei[k - 2])
                da.append((data[1][i], data[0][i], d))
            return cls, da

    @classproperty
    def gangweis(cls):
        ''' 获取岗位清单'''
        obj = cls.objects(_id='').first()
        return obj and obj.gangwei

    @classproperty
    def jyzs(cls):
        ''' 获取交易组清单'''
        return {obj._id: obj.name for obj in cls.objects if obj._id}

if __name__ == "__main__":
    from orange.coroutine import run
    root = Path(r'C:\Users\huangtao\OneDrive\工作\参数备份\岗位与交易组')
    filename = max(root.glob('*.xls'))
    print(filename)

    run(JyGangwei.amport_file(filename, drop=True))
    print(JyGangwei.gangweis)
    print(JyGangwei.jyzs)
