# 项目：营业主管履职报告
# 模块：分派任务模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-06-14 15:24

from .model import LvZhi, P
from .lzwt import LzWenTi


def assign_task():
    print('开始分派任务')
    yf = max(LzWenTi.objects.distinct('yf'))
    print('当前处理月份为：%s' % (yf))
    for t in LzWenTi.objects((P.yf == yf) & ((P.wtfl == None) | (P.bm == None))):
        print('问题分类：%s' % (t.wtfl or ""))
        print('机构    ：%s' % (t.jg))
        print('报告人  ：%s' % (t.bgr))
        print('具体内容：%s' % (t.jtnr))
        print('答复部门：%s' % (t.bm or ""))
        print('答复人  ：%s' % (t.dfr or ""))
        result = input('请输入处理意见：\n回复格式为：分类 答复人\nS键跳过,T键结束）\n请输入：')
        if result.upper() == 'T':
            break
        elif result.upper() != 'S':
            a = result.split(' ')
            if len(a) == 2:
                t.wtfl = a[0]
                if a[1].endswith('部') or a[1].endswith('中心'):
                    t.bm = a[1]
                    t.dfr = ""
                else:
                    t.bm = '运营管理部'
                    t.dfr = a[1]
                print('分类：%s\t部门：%s\t答复人：%s\n' % (t.wtfl, t.bm, t.dfr or ""))
                t.save()
            else:
                print('录入信息错误，跳转至下一条\n')
