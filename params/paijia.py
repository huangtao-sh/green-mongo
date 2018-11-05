# 项目：   工作平台
# 模块：   外汇牌价模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2018-11-05 19:42

from glemon import Document, P, enlist
from orange import datetime, R, arg

JIANJIE = {'林吉特', '卢布', '兰特', '韩元'}  # 这些币种的汇率采取间接标价法


class PaiJia(Document):
    _projects = enlist('_id,huilv')

    @classmethod
    @arg('-f', '--fetch', action='store_true', help='获取当前的外汇牌价')
    @arg('-s', '--show', dest='rq', default='noset', nargs='?', help='查询指定日期牌价')
    def main(cls, **options):
        if options['fetch']:
            cls.fetch()
        rq = options.get('rq')
        if rq != 'noset':
            rq = rq or datetime.today() % ('%Y-%m-%d')
            obj = cls.objects.get(rq)
            if rq:
                print(f'日期：    {rq}')
                for k, v in obj.huilv.items():
                    print(k, v, sep='\t')

    @classmethod
    def fetch(cls):
        async def _fetch(sess):
            params = {}
            end = datetime.today()
            start = end.add(months=-1)
            params['projectBean.startDate'] = start.strftime('%Y-%m-%d')
            params['projectBean.endDate'] = end.strftime('%Y-%m-%d')
            soup = await sess.get_soup('http://www.safe.gov.cn//AppStructured/hlw/RMBQuery.do', params=params)
            table = soup.find('table', id='InfoTable')
            data = []
            for tr in table.find_all('tr'):
                row = [col.text.strip() for col in tr.find_all(R/'t[hd]')]
                data.append(row)
            header = data[0][1:]
            for d in data[1:]:
                data.append((d[0], dict(zip(header, d[1:]))))
            cls.bulk_write(data, method='upsert')
        from orange.utils.hclient import Crawler
        Crawler.start(target=_fetch)
