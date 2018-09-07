# 项目：工作平台
# 模块：内部账户表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-10-14 11:28
# 修订：2017-12-18 修正导入文件的算法，以提高导入速度
# 修订：2018-09-06 修正内部账户导入问题
# 修订：2018-09007 由于性能问题，不再支持 aiofiles 

from glemon import Document, P
from orange import R, arg, Path


class AcTemplate(Document):
    _projects = 'jglx', 'sxrq', 'km', 'bz', 'xh', 'hmgz', 'hm', 'tzed', 'cszt', 'jxbz'


class ZhangHu(Document):
    _projects = '_id', 'name'

    @classmethod
    def show(cls, ac):
        objects = cls.objects(P._id.startswith(ac)).order_by(P._id)
        if objects.count() > 0:
            print('已开账户情况：')
            wy = None
            for i, obj in enumerate(objects, 1):
                xh = obj._id[6:]
                if not wy and i != int(xh):
                    wy = i
                print('%s-%s    %s' % (obj._id[:6], xh, obj.name))
            if not wy:
                wy = int(xh) + 1
            print('最小未用账户序号：%03d' % (wy))
        else:
            print('尚未开立账户')

    @classmethod
    async def amport_file(cls, filename, drop=True, dupcheck=True):
        dupcheck and cls._dupcheck(filename)
        with open(str(filename), 'rb')as f:
            cls.drop()
            datas = set()
            for row in f.readlines():
                s = row.split(b',')
                ac = s[0].decode()[13:22]
                if ac not in datas:
                    datas.add(ac)
                    name = s[3].decode('gbk', 'ignore')[1:-1].strip()
                    await cls(_id=ac, name=name).asave()
            dupcheck and cls._importsave(filename)
            print('文件 %s 已导入' % (filename))


@arg('ac', nargs='?', help='账户，格式应为：999999')
def main(ac=None):
    if ac:
        if R / r'\d{6}' == ac:
            from .accounting import Accounting
            q = Accounting.search(query=ac).first()
            if q:
                print('科目信息：%s\n' % (q))
            ZhangHu.show(ac)
        elif R/r'\d{6}\-\d{1,3}':
            km, xh = ac.split('-')
            for obj in AcTemplate.objects((P.km == km) & (P.xh == int(xh))):
                print(obj.jglx, obj.km, obj.xh, obj.bz,
                      obj.sxrq, obj.hm, obj.tzed)


if __name__ == '__main__':
    file = max(Path('d:/工作/参数备份').rglob('ggnbzhmb.del'))
    print(file)
    from orange.coroutine import run
    run(AcTemplate.amport_file(file, drop=True, encoding='gbk'))
    obj = AcTemplate.objects.first()
