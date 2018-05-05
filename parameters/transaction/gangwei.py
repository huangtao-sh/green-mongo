#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-10 12:47:03
# @Author  : 黄涛 (huang.t@live.cn)
# @Link    : http://www.jianshu.com/u/3bf5919e38a7
# @Version : $Id$

from orange import classproperty
from glemon import Document, P


class JyGangwei(Document):
    '''交易岗位及组的设置'''
    _projects = '_id', 'name', 'gangwei'
    _mapper = 0, 1, 2

    @classmethod
    def _proc_sheet(cls, index, name, data, **kw):
        def _conv(x): return '%02d' % (x) if isinstance(
            x, (int, float)) else '%s' % (x)
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
    def gangweis(self):
        ''' 获取岗位清单'''
        obj = self.objects(_id='').first()
        return obj and obj.gangwei

    @classproperty
    def jyzs(self):
        ''' 获取交易组清单'''
        return {obj._id: obj.name for obj in self.objects if obj._id}
