# 项目：参数数据模型
# 模块：汇率相关参数
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-12-29 10:50

from imongo import *
from orange.xlsx import *
from orange import *
from orange.hclient import *
from orange.parseargs import *

'''
说明：
1、汇率牌价数据来源于中国外汇交易中心。
2、人民币对林吉特、卢布、兰特、韩元汇率中间价采取间接标价法，即100人民币折合多少林吉特、卢布、兰特、韩元。人民币对其它10种货币汇率中间价仍采取直接标价法，即100外币折合多少人民币。
'''

JIANJIE={'林吉特','卢布','兰特','韩元'}  # 这些币种的汇率采取间接标价法

# 币种映射表，以下币种均为我行使用的币种
BIZHONG={'人民币':'01',
         '英镑':'12',
         '港币':'13',
         '港元':'13',
         '美元':'14',
         '瑞士法朗':'15',
         '瑞士法郎':'15',
         '新加坡元':'18',
         '日元':'27',
         '加元':'28',
         '澳元':'29',
         '欧元':'38',
         '新西兰元':'95',
         '林吉特':'32',
         }
BIZHONG2={'01':'人民币',
          '12':'英镑',
          '13':'港币',
          '14':'美元',
          '15':'瑞士法郎',
          '18':'新加坡元',
          '27':'日元',
          '28':'加元',
          '29':'澳元',
          '38':'欧元',
          '32':'林吉特',
          '88':'结算通',
          '95':'新西兰元'}
          
class HuiLv(EmbeddedDocument):
    ''' 汇率明细 '''
    bz=StringField()    # 币种
    huilv=FloatField()  # 公布汇率

    @property
    def hv(self):  # 如为间接牌价，则进行转换，否则直接输出
        return 10000/self.huilv if self.bz in JIANJIE else self.huilv

class WhPaijia(Document):
    ''' 外汇牌价表 '''
    rq=StringField()         # 发布日期
    huilv=ListField(EmbeddedDocumentField(HuiLv))  # 汇率清单

    @classmethod
    def get_hv(cls,rq=None):
        if rq:
            q=cls.objects(P.rq<=rq)
        else:
            q=cls.objects.order_by("rq").limit(1)
        hv=q.distinct('huilv') or []
        return {BIZHONG[x.bz]:x.hv for x in hv if x.bz in BIZHONG}
    
    @classmethod
    def load_data(cls,data,**kw):
        bzs=data[0][1:]
        for row in data[1:]:
            huilv=[]
            for bz,amount in zip(bzs,row[1:]):
                amount=0 if amount=='-' else float(amount)
                huilv.append(HuiLv(bz=bz,huilv=amount))
            cls.objects(rq=row[0]).upsert_one(huilv=huilv)

    @classmethod
    def export(cls,rq=None,filename=None):
        rq=rq or datetime.today().replace(day=1)%'%F'
        result=cls.objects(P.rq<rq).limit(1).first()
        ensure(result,'没有查询到相应的汇率')
        rq=result.rq
        hv={BIZHONG[x.bz]:x.hv for x in result.huilv \
                if x.bz in BIZHONG}
        filename=filename or '汇率相关参数表%s.xlsx'%(rq)
        with Book(filename) as book:
            book.worksheet='大额提示参数'
            book.add_table('A1',data=WhBigamt.export(rq),
                               columns=BigAmtHeader)
            # 导出金额授相关参数
            hv['01']=100
            hv['88']=100
            data=WhDengji.objects.order_by("dj").values_list('dj','name','edu')
            header=data[0][2]
            header_len=len(header)
            book.worksheet='额度登记配置'
            sheet=book.worksheet
            book.A1_A4='额度等级','mh2'
            book.B1_B4='等级名称','mh2'
            book.set_columns('B:B',width=35.5)
            book.set_columns('C:FO',width=21,
                             cell_format=book._formats.get('currency'))
            book.row=5
            for d, in book.iter_rows(data[1:]):
                book.A=['%02d'%(d[0]),d[1]]
            for i,d in enumerate(sorted(hv.items())):
                hv='%0.6f'%(d[1]/100)
                sheet.write_row(1,i*header_len+2,[hv]*header_len)
                sheet.write_row(2,i*header_len+2,[d[0]]*header_len)
                sheet.write_row(3,i*header_len+2,header)
                sheet.merge_range(0,i*header_len+2,0,(i+1)*header_len+1,
                                  BIZHONG2.get(d[0]),book._formats.get('mh2'))
                for k,row in enumerate(data[1:]):
                    ed=[round(x*100/d[1],0) for x in row[2]]
                    sheet.write_row(4+k,i*header_len+2,ed)

BigAmtHeader=[
    {'header':'客户类型','head_format':'h2'},
    {'header':'币种号','head_format':'h2'},
    {'header':'转账类型','head_format':'h2'},
    {'header':'金额','width':22.13,'head_format':'h2'}]

class WhBigamt(Document):
    customtype=StringField()
    bzh=StringField()
    trantype=StringField()
    amount=FloatField()

    @classmethod
    def export2xlsx(cls,rq=None,fn=None):
        fn=fn or '大额提示参数表%s.xlsx'%(rq)
        data=cls.export(rq)
        with Book(filename) as book:
            book.worksheet='大额提示参数'
            book.add_table('A1',data=WhBigamt.export(rq),
                               columns=BigAmtHeader)
                    
    @classmethod
    def export(cls,rq=None):
        _convert=lambda x:'+%019.2f'%(x)
        d=cls.objects(P.bzh.in_(['01','14'])).order_by('bzh','customtype',
                                                       'trantype')
        hv=WhPaijia.get_hv(rq)
        my=hv.pop('14')
        meiyuan=[]
        data=[]
        for i in d:
            if i.bzh=='14':
                meiyuan.append(i)
            data.append([i.customtype,i.bzh,i.trantype,
                         _convert(i.amount)])
        for bz,pj in sorted(hv.items()):
            for i in meiyuan:
                data.append([i.customtype,bz,i.trantype,
                            _convert(i.amount*my/pj)])
        return data

class WhDengji(Document):
    dj=StringField(primary_key=True)
    name=StringField()
    edu=ListField(FloatField())

    @classmethod
    def export(cls,rq=None):
        hv=WhPaijia.get_hv(rq)
        hv['01']=100
        hv['88']=100
        data=cls.objects.order_by("dj").values_list('dj','name','edu')
        datas=[]
        header=['币种','额度等级','等级名称']
        header.extend(data[0][2])
        datas.append(header)
        for bz,pj in sorted(hv.items()):
            for dj,name,edu in data[1:]:
                d=[bz,'%02d'%(dj),name]
                d.extend([round(x*100/pj,0) for x in edu])
                datas.append(d)
        return datas

    @classmethod
    def export2xlsx(cls,rq=None,fn=None):
        hv=WhPaijia.get_hv(rq)
        hv['01']=100
        hv['88']=100
        data=cls.objects.order_by("dj").values_list('dj','name','edu')
        header=data[0][2]
        header_len=len(header)
        fn=fn or '金额授权参数%s.xlsx'%(rq)
        with Book(fn) as book:
            book.worksheet='额度登记配置'
            sheet=book.worksheet
            book.A1_A4='额度等级','mh2'
            book.B1_B4='等级名称','mh2'
            book.set_columns('B:B',width=35.5)
            book.set_columns('C:FO',width=21,
                             cell_format=book._formats.get('currency'))
            book.row=5
            for d, in book.iter_rows(data[1:]):
                book.A=['%02d'%(d[0]),d[1]]
            for i,d in enumerate(sorted(hv.items())):
                hv='%0.6f'%(d[1]/100)
                sheet.write_row(1,i*header_len+2,[hv]*header_len)
                sheet.write_row(2,i*header_len+2,[d[0]]*header_len)
                sheet.write_row(3,i*header_len+2,header)
                sheet.merge_range(0,i*header_len+2,0,(i+1)*header_len+1,
                                  BIZHONG2.get(d[0]),book._formats.get('mh2'))
                for k,row in enumerate(data[1:]):
                    ed=[round(x*100/d[1],0) for x in row[2]]
                    sheet.write_row(4+k,i*header_len+2,ed)
                
    @classmethod
    def load_data(cls,data,**kw):
        if data[0][0]!='额度等级':
            return
        cls.objects.delete()
        datas=[]
        datas.append({'_id':0,
                      'edu':data[3][2:]})
        for row in data[4:]:
            datas.append({'_id':int(row[0]),
                         'name':row[1],
                         'edu':row[2:]})
        if datas:
            cls._batch_insert(datas)

class Waihui(Crawler):
    async def run(self):
        params={}
        end= datetime.today()
        start= end.add(months=-1)
        params['projectBean.startDate']=start.strftime('%Y-%m-%d')
        params['projectBean.endDate']=end.strftime('%Y-%m-%d')
        soup=await self.get_soup('http://www.safe.gov.cn/AppStructured/view/project!RMBQuery.action',params=params)
        table=soup.find('table',id='InfoTable')
        data=[]
        for tr in table.find_all('tr'):
            row=[col.text.strip() for col in tr.find_all(R/'t[hd]')]
            data.append(row)
        WhPaijia.load_data(data) 

def proc(fetch,date=None,files=None):
    if fetch:
        Waihui.start()
        print('导入假期表成功!')

    if files!="NULL":
        if files:
            pass
        else:
            path=max(Path('~/OneDrive/工作/参数备份').rglob('大额提示bigamt.del'))
            WhBigamt.load_files(path,clear=True)
            print('文件 %s 导入成功！'%(path))
            path=max(Path('~/OneDrive/工作/工作档案/运营参数').rglob('额度登记配置*.*'))
            WhDengji.load_files(path)
            print('文件 %s 导入成功！'%(path))
        
    if date!="NULL":
        WhPaijia.export(date)
        print('导出文件成功！')
        
main=Parser(
    Arg('-f','--fetch',action='store_true',help='从外汇管理局网站获取汇率'),
    Arg('-e','--export',metavar='DATE',dest='date',nargs="?",default='NULL',help='导出参数'),
    Arg('-i','--import',dest='files',metavar='filename',nargs='*',default='NULL',help='导入参数'),
    proc=proc)

if __name__=='__main__':
    main()

