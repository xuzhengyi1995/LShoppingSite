# For one products
# XUZhengyi, 24/01/2018

import tornado.web


class OneProductMoudle(tornado.web.UIModule):
    def render(self, pinfo):
        pres = {}
        pres['id'] = pinfo['id']
        pres['org_website'] = pinfo['org_website']
        pres['price'] = pinfo['price']
        pres['img_url'] = 'https://static.chemistwarehouse.com.au/ams/media/pi/%d/hero_150.jpg' % pinfo['id']
        pres['name_cn'] = pinfo['name_cn']
        pres['name_en'] = pinfo['name_en']

        r = int(pinfo['rate'])
        pres['rate_s'] = range(r)
        pres['rate_e'] = range(5 - r)
        if(pinfo.get('cid')):
            pres['large'] = 4
            pres['add_div'] = True if(pinfo['cid'] % 3 == 0) else False
        else:
            pres['add_div'] = False
            pres['large'] = 3
        return self.render_string('modules/products_one.html', product=pres)
