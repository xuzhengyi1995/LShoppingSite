# SearchHandler
# XUZhengyi, 23/01/2018

import re
import tornado.web
import json
from handlers.BasicHandler import BasicHandler


class SearchHandler(BasicHandler):
    def get(self):
        keyword = self.get_argument('keyword')
        keyword_s = self.reInput.sub("", keyword).split(' ')

        query_s = {'$or': [{'$and': []}, {'$and': []}]}
        for i in keyword_s:
            rec = re.compile(i, re.IGNORECASE)
            query_s['$or'][0]['$and'].append({'name_en': rec})
            query_s['$or'][1]['$and'].append({'name_cn': rec})

        sump = self.collectionP.count(query_s)

        try:
            page = int(self.get_argument('page'))
        except:
            page = 1
        try:
            sp = int(self.get_argument('sp'))
        except:
            sp = 12

        try:
            sort = int(self.get_argument('sort'))
        except:
            sort = 0

        if(sp > 48):
            sp = 48
        if(page * sp > sump):
            page = int(sump / sp) + 1
        if(sort < -1 or sort > 4):
            sort = 0

        query = {'$query': query_s}

        if(sort == 1):
            query['$orderby'] = {'rate': -1}
        if(sort == 2):
            query['$orderby'] = {'price': 1}
        if(sort == 3):
            query['$orderby'] = {'price': -1}
        if(sort == 4):
            # TODO: Add sold count
            query['$orderby'] = {'rate': 1}

        result = self.collectionP.find(query, limit=sp, skip=sp * (page - 1), projection={
                                       '_id': False, 'id': True, 'name_en': True, 'name_cn': True, 'rate': True, 'org_website': True, 'price': True})

        s = 1
        res = []
        for i in result:
            i['cid'] = s
            s += 1
            res.append(i)
        accept = self.request.headers['Accept']

        if(str(accept).lower().find('json') != -1):
            self.set_header("Content-Type", 'application/json')
            self.write(json.dumps({'data': res}))
            self.finish()
            return

        self.info['cat'] = ['Search']
        self.info['title'] = keyword + " 结果"
        _page = {
            'page_now': page,
            'page_sum': int(sump / sp) + 1,
            'sp': sp,
            'sort': sort,
            'keyword': keyword
        }
        self.render('products.html', products=res, page=_page, info=self.info)
