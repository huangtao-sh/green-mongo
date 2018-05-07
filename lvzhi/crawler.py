# 项目：会计主管履职报告
# 模块：提取数据模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-04-19 10:04

from orange.hclient import *
from .model import *
from orange import *

class CLvZhi(Crawler):
    root='http://oa.czbank.com'
    async def login(self):
        auth=Shadow.get('oa')
        self.qc=now().add(months=-1)%('%Y-%m')
        url='login/VerifyLoginSSO.jsp'
        async with self.post(url,data=auth)as resp:
            if resp.status==200:
                print('登录系统成功！')
                print('当前期次：%s'%(self.qc))

    async def run(self):
        await self.login()
        self.begin=LvZhi.get_begin_date()
        self.bhs=LvZhi.bhs(self.begin)
        await self.yiban()
        
    async def yiban(self):
        url='workflow/search/WFSearchResult.jsp?resourceid=&needHeader=false&query=1&pagenum=1&iswaitdo=0&docids=&date2during=0&viewType=0&viewScope=&numberType='
        text=await self.get_text(url)
        Path('d:/a.html').text=text
        for k in text.splitlines():
            if'/weaver/weaver.common.util.taglib.SplitPageXmlServlet' in k:
                tableString=list(R/'[0-9A-F]{32}'/k)[0]
        tasks=[]
        for page in range(1,2):
            tasks.append(self.list_yiban(tableString=tableString,
                                         pageIndex=str(page)))
        await wait(tasks)

    async def list_yiban(self,**kw):
        listdata={'tableInstanceId':"",
        "tableString":"",
        "pageIndex":"0",
        "orderBy":"null",
        "otype":"null",
        "mode":"run",
        "customParams":"null",
        "selectedstrs":"",
        #"pageId":"Wf:workflow_common_list"
        "pageId":"Wf:handledMatters"
                      }
        listdata.update(kw)
        LISTURL2="weaver/weaver.common.util.taglib.SplitPageXmlServlet"
        datas=[]

        text=await self.get_text(LISTURL2,data=listdata,method="POST")
        table=await self.get_soup(LISTURL2,data=listdata,method='POST')
        for row in table.find_all('row'):
            _get_value=lambda column:row.find('col',column=column)['value']
            bh=_get_value('requestid')
            gzl=_get_value('workflowid')
            rq=_get_value('createdate')
            sts=_get_value('currentnodeid')
            if(gzl=='219')and(rq>=self.begin)and(sts=='701'):
                datas.append(bh)
        datas=set(datas)-self.bhs
        if datas:
            self.bhs.update(datas)
            tasks=[self.get_page(requestid=i) for i in datas]
            await wait(tasks)
        print('第 %s 页数据导入完成！'%(kw['pageIndex']))
        
    async def get_page(self,**kw):
        rptdata={'requestid':'',
          'isovertime':'0'}
        path=LvZhi.get_path(False)
        DownURL='weaver/weaver.file.FileDownload'
        dparams={'f_weaver_belongto_userid':'1124',
            "f_warver_belongto_usertype":'null',
            'fileid':'',
            'download':'1',
            'requestid':''}
        rptdata.update(kw)
        bh=kw['requestid']
        await self.get_text('workflow/request/ViewRequest.jsp',params=rptdata)
        text=await self.get_text('workflow/request/ViewRequestIframe.jsp',
                                 params=rptdata)
        s=text.splitlines()
        text='\n'.join(s[423:])
        soup=BS4(text,'lxml')
        t=soup.find('table',class_='excelMainTable tablefixed')
        bt=t.find('span',id='requestnamespan').text.strip() # 标题
        bgr=t.find('span',id='field7175span').text.strip()  # 报告人
        bm=t.find('span',id='field7176span').text.strip()   # 部门
        jg=t.find('span',id='field7177span').text.strip()   # 机构
        rq=t.find('span',id='field7178span').text.strip()   # 报告日期
        sbyx=t.find('input',id='field10075')['value']=='1'  # 设备运行情况
        ycsbmc=t.find('td',_fieldid='10077').text.strip()   # 异常设备名称
        ycnr=t.find('td',_fieldid='10078').text.strip()     # 异常设备内容
        mx=t.find('table',id='oTable0').tbody
        d=[x for x in mx.find_all('tr')][2:]
        tb=t.find('table',id='field7180_tab')
        fj=[]
        for x in tb.find_all('a',onmouseover=True):
            val=list(R/r'\d+'/x['onclick'])
            dparams['fileid']=val[-2]
            dparams['requestid']=val[0]
            p=path/('%s-%s'%(bh,x['title']))
            fj.append(x['title'])
            await self.download(DownURL,params=dparams,path=p)
        detail=[]
        for x in d:
            p=[x.td.text.strip()]
            for o in x.find_all('option',selected=True):
                p.append(o.text)
            if x.textarea:
                p.append(x.textarea.text.strip())
            if p[0]=='序号':
                continue
            detail.append(Detail(**dict(zip(('xh','bgzl','zyx','jtnr'),p))))

        if all([x.bgzl.startswith('会计主管履职') for x in detail]):
            lx='0'
        else:
            lx='1'

        LvZhi(bh=bh,qc=self.qc,bt=bt,gzl='会计履职报告表单',bgr=bgr,bm=bm,\
                  jg=jg,rq=rq,lx=lx,\
            fj=fj,detail=detail,sbyx=sbyx,ycsbmc=ycsbmc,ycnr=ycnr).save()
        print('获取：%s 成功，日期：%s'%(bt,rq))  
