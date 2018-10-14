# 项目：工作平台
# 模块：用户
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-11 18:52

from glemon import Document, Descriptor


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
            str.strip: (0,2,6,36,37,55,56,59)
            }
    }
    
