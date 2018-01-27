# Get product list from websites and sent them to ProductGetter class
# XUZhengyi, 23/01/2018

from abc import ABCMeta, abstractmethod
import re
from ProductGetters import ProductGetter_CWH
from Db import Db
from GetHtml import GetHtml
import settings
import threadpool


class WebSiteProductManager:
    __metaclass__ = ABCMeta
    '''
    Website product manager abstract based class.
    '''

    def __init__(self, _webSiteUrl, _pageBaseUrl, _urlDictList, _pageParam='?page=%d'):
        self.collection = Db().getCollection('products')
        self.webSiteUrl = _webSiteUrl
        self.pageBaseUrl = _pageBaseUrl
        self.urlDictList = _urlDictList
        self.pageParam = _pageParam
        self.lenUrlList = len(self.urlDictList)
        self.tpool = threadpool.ThreadPool(num_workers=settings.nb_thread)
        '''
        Base class
        '''
        self.productGetter = None

    def updateAllProduct(self):
        for i in range(self.lenUrlList):
            url = self.pageBaseUrl % self.urlDictList[i]
            print(url)
            self._processCat(url)
        self.tpool.wait()

    def _processCat(self, url):
        getter = GetHtml()
        url_page1 = url + self.pageParam % 1
        print(url_page1)
        getter.set(url=url_page1)
        data = getter.get().decode('utf-8')

        sumPage = self._getSumPage(data)
        print(sumPage)
        for i in range(1, sumPage + 1):
            if(i != 1):
                url_page_i = url + self.pageParam % i
                print(url_page_i)
                getter.set(url=url_page_i)
                data = getter.get().decode('utf-8')
            list_product = self._getProductList(data)
            '''
            [(id,price,url),...]
            '''
            reqParams = []
            for j in list_product:
                pid, price, url_p = j
                reqParams.append(([pid, price, url_p], None))
            requests = threadpool.makeRequests(self._processOneProduct, reqParams)
            [self.tpool.putRequest(req) for req in requests]

    def _processOneProduct(self, pid, price, url):
        getProduct = self.collection.find_one(
            {'org_website': self.webSiteUrl, 'id': pid}, projection={'price': True})
        if(not getProduct):
            print('Add:', pid, 'Price:', price)
            self.productGetter.processProductWithUrl(url)
        else:
            if(getProduct['price'] != price):
                print('Update:', pid, 'Price:', price)
                self.collection.update_one(
                    {'org_website': self.webSiteUrl, 'id': pid}, {'$set': {'price': price}})

    @abstractmethod
    def _getSumPage(self, data):
        pass

    @abstractmethod
    def _getProductList(self, data):
        pass


class WebSiteProductManager_CWH(WebSiteProductManager):
    '''
    For https://www.chemistwarehouse.com.au
    '''

    def __init__(self):
        wurl = "https://www.chemistwarehouse.com.au"
        purl = "https://www.chemistwarehouse.com.au/Shop-Online/%d/%s"
        lurl = [
            (256, 'Health'),
            (257, 'Beauty'),
            (258, 'Medicines'),
            (259, 'Personal-Care'),
            (260, 'Medical-Aids'),
            (651, 'Veterinary')
        ]
        self.reSumPage = re.compile(r"<a class=\"last-page\" href=\".*?page=(\d*?)\">Last</a>")
        self.reProductList = re.compile(
            r"<td>.*?<input type=\"hidden\" class=\"PageGroupSKUs\" value=\"(.*?)\"/>.*?<a class=\"product-container\" href=\"(.*?)\" title=.*?<span class='Price' >\$(.*?) .*?</td>", re.S)
        super().__init__(wurl, purl, lurl)
        self.productGetter = ProductGetter_CWH()

    def _getSumPage(self, data):
        r = self.reSumPage.findall(data)
        if(len(r) == 0):
            r = 2
        else:
            r = r[0]
        return int(r)

    def _getProductList(self, data):
        '''
        [(id,price,url),...]
        '''
        l = self.reProductList.findall(data)
        res = []
        for i in l:
            pid, url, price = i
            res.append((int(pid), float(price), self.webSiteUrl + url))
        return res


if __name__ == '__main__':
    test = WebSiteProductManager_CWH()
    test.updateAllProduct()
