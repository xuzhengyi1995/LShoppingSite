# Get a product
# XUZhengyi, 24/01/2018

import re
import tornado.web
import json
from handlers.BasicHandler import BasicHandler


class GetProductHandler(BasicHandler):
    def get(self, website, pid):
        result = self.collectionP.find_one(
            {'org_website': website, 'id': int(pid)}, projection={'_id': False})
        result['rate'] = int(result['rate'])
        if(not result.get('description_cn')):
            result['description_cn'] = "<h2>暂未翻译</h2>"
        accept = self.request.headers['Accept']

        if(str(accept).lower().find('json') != -1):
            self.set_header("Content-Type", 'application/json')
            self.write(json.dumps(result))
            self.finish()
            return

        recommand = self.collectionP.find(
            {'$query': {'categories': result['categories'][len(result['categories']) - 1]}, '$orderby': {'rate': -1}}, limit=4,
            projection={'_id': False, 'id': True, 'name_en': True, 'name_cn': True, 'rate': True, 'org_website': True, 'price': True})

        rec = [i for i in recommand]
        self.info['cat'] = result['categories']
        self.info['title'] = result['name_en']
        self.render('product-page.html', info=self.info, product=result, recommands=rec)
