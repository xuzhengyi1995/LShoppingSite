# BasicHandlers.py
# XUZhengyi, 22/01/2018

import re
import tornado.web


class BasicHandler(tornado.web.RequestHandler):
    def get(self):
        self.write_error(404)

    def initialize(self):
        self.collectionP = self.application.db.getCollection('products')
        self.reInput = re.compile(r"[^\w ]+")
        self.info = {}
        self.info['title'] = '子健代购'
        self.info['cart_product_num'] = 0
        self.info['cart_sum_price'] = 0
        self.info['cat'] = []

    def write_error(self, status_code, **kwargs):
        if(status_code == 404):
            self.render('404.html', info=self.info)
