# 项目：工作平台
# 模块：用户
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-11 18:52

from glemon import Document, Descriptor, profile, P
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
            '_id,telephone,branch,zzjb,xjjb,czbz,fqjyz,zjhm': str.strip,
        },
    }
    _profile = {
        '柜员号': '_id',
        '姓名': 'name',
        '员工号': 'userid',
        '证件号码': 'zjhm',
        '电话': 'telephone',
        '机构': 'brname',
        '启用日期': 'qyrq',
        '中止日期': 'zzrq',
        '状态': 'zt',
    }

    @property
    def brname(self):
        br = GgJgm.objects.filter(_id=self.branch).first()
        if br:
            return br.jgmc

    @classmethod
    def check(cls):
        print(f'当前参数月份：{profile.param_yf}')
        print('-'*20)
        print('采用密码认证有柜员清单')
        for r in Teller.objects.filter(
                P.zt.regex('[12356].')
                & (P.rzlx == '0')).order_by(P.branch).scalar('_id', 'branch',  'qyrq', 'name'):
            print(*r, sep='\t')

        print('-'*20)
        print('证件号码错误')
        a = Teller .aggregate()
        a.match(P.zt.regex('[12356].'))
        a.group(P.zjzl, P.zjhm, P.names.addToSet(
            '$name'), P.branches.addToSet('$branch'))
        for zjhm, names, branches in a.scalar('_id.zjhm', 'names', 'branches'):
            if(len(names) > 1)and all(map(lambda x: len(x) <= 5, names)):
                print(f'证件号码： {zjhm}')
                print('姓名：', *names)
                print('机构：', *branches, '\n')

    @classmethod
    @arg('-c', '--check', action='store_true', help='检查柜员表是否存在问题')
    @arg('query', nargs='*', help='输入查询条件')
    def main(cls, check=False, query=None):
        if check:
            cls.check()
        if query:
            for q in query:
                if R/r'\d{3,5}' == q:
                    obj = cls.find(_id='%05d' % int(q)).first()
                    obj and obj.show()
                if R/r'\d{9}' == q:
                    for obj in cls.find(branch=q):
                        print('\n')
                        obj.show()
                if R/r'[\u4e00-\u9fa5]+' == q:
                    for obj in cls.find(P.name.contains(q)):
                        print('\n')
                        obj.show()
                if R/r'[A-Z]+\d+' == q:
                    for obj in cls.find(P.userid.startswith(q)):
                        print('\n')
                        obj.show()
                if R/r'1\d+' == q:
                    for obj in cls.find(P.telephone.startswith(q)):
                        print('\n')
                        obj.show()
