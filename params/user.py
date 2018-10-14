# 项目：工作平台
# 模块：用户
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-11 18:52

from glemon import Document, Descriptor
from orange import arg, R
from .jgm import GgJgm


class Teller(Document):
    _projects = ('_id', 'name', 'telephone', 'grade', 'branch', 'userid',
                 'gangwei', 'jyz', 'jgz', 'zzjb', 'xjjb', 'rzlx', 'zt', 'pbjy',
                 'gwxz', 'qyrq', 'zzrq', 'czbz', 'fqjyz', 'gwjyz', 'zjzl', 'zjhm')
    load_options = {
        'fields': ('_id,name,telephone,,grade,,branch,userid,'
                   ',,,,,,,,,,,,,,,,,,,,,,,,,,,'
                   'jyz,jgz,zzjb,xjjb,rzlx,'
                   ',,,,,,,,,,'
                   'zt,pbjy,gwxz,qyrq,zzrq,czbz,fqjyz,gwjyz,zjzl,zjhm'),
        'converter': {
            str.strip: (0, 2, 6, 36, 37, 55, 56, 59)
        }
    }

    @property
    def brname(self):
        br = GgJgm.objects.filter(_id=self.branch).first()
        if br:
            return br.jgmc

    @classmethod
    @arg('-c', '--check', action='store_true', help='检查柜员表是否存在问题')
    @arg('query', nargs='*', help='输入查询条件')
    def main(cls, check=False, query=None):
        if check:
            print('check')
        if query:
            for q in query:
                if R/r'\d{3,5}' == q:
                    obj = cls.objects.filter(_id='%05d' % int(q)).first()
                    if obj:
                        print(obj._id)
                        print(obj.userid)
                        print(obj.name)
                        print(obj.telephone)
                        print(obj.branch)
                        print(obj.brname)
                if R/r'\d{9}' == q:
                    for obj in cls.objects.filter(branch=q):
                        print(obj._id)
                        print(obj.userid)
                        print(obj.name)
                        print(obj.telephone)
                        print(obj.branch)
                        print(obj.brname)
                        print('\n')
