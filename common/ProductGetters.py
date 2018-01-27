# Get product from website
# XUZhengyi, 22/01/2018

from abc import ABCMeta, abstractmethod
import re
import json

from GetHtml import GetHtml
from Db import Db
from GoogleTranslator import GoogleTranslator


class ProductGetter:
    __metaclass__ = ABCMeta
    '''
    ProductGetter abstract based class.
    '''

    def __init__(self, baseUrl):
        self.collection = Db().getCollection('products')
        self.baseUrl = baseUrl
        self.translator = GoogleTranslator()

    def processProductWithUrl(self, url):
        htmlGetter = GetHtml()
        htmlGetter.set(url=url)
        data = htmlGetter.get().decode('utf-8')

        _id = self._findId(data)
        _name_en = self._findName(data)
        _name_cn = self._translate(_name_en)
        _description = self._findDescription(data)
        _rate = self._findRate(data)
        _categories = self._findCategories(data)
        _price = self._findPrice(data)
        _images = self._findImages(data)

        insert_data = {
            'id': _id,
            'name_en': _name_en,
            'name_cn': _name_cn,
            'description': _description,
            'review': [],
            'rate': _rate,
            'categories': _categories,
            'org_website': self.baseUrl,
            'org_url': url,
            'price': _price,
            'images': _images
        }

        self.collection.insert_one(insert_data)

    def _translate(self, name_en):
        return self.translator.translate(name_en)['translatedText']

    @abstractmethod
    def _findName(self, data):
        pass

    @abstractmethod
    def _findDescription(self, data):
        pass

    @abstractmethod
    def _findRate(self, data):
        pass

    @abstractmethod
    def _findCategories(self, data):
        pass

    @abstractmethod
    def _findPrice(self, data):
        pass

    @abstractmethod
    def _findImages(self, data):
        pass

    @abstractmethod
    def _findId(self, data):
        pass


class ProductGetter_CWH(ProductGetter):
    '''
    For https://www.chemistwarehouse.com.au
    '''

    def __init__(self):
        super().__init__('https://www.chemistwarehouse.com.au')
        self.reNameAndId = re.compile(r"<script>dataLayer = \[(.*?)\]")
        self.rePrice = re.compile(r"<div class=\"Price\" itemprop=\"price\">\$(.*?)</div>")
        self.reRate = re.compile(
            r"<span class=\"bvseo-ratingValue\" itemprop=\"ratingValue\">(.*?)</span>")
        self.reImage = re.compile(
            r"<a class=\"image_enlarger\" title=\"\" style=\"text-decoration: none; outline-style: none;\" href=\"(.*?)\" data-title=\"Product Name\" data-lightbox=\"preview\">")
        self.reCat_1 = re.compile(
            r"<div class=\"breadcrumbs\"> <a href='/home' > Home </a> / (.*?)</div>", re.S)
        self.reCat_2 = re.compile(r">([^/]*)<")
        self.reDes = re.compile(
            r"<div class=\"product-info-container\" style=\"display:block\" >.*</section>.*?</div>", re.S)

    def _findName(self, data):
        dict_data = json.loads(self.reNameAndId.findall(data)[0])
        return dict_data['sectionName']

    def _findId(self, data):
        dict_data = json.loads(self.reNameAndId.findall(data)[0])
        return int(dict_data['ecomm_prodid'])

    def _findPrice(self, data):
        return float(self.rePrice.findall(data)[0])

    def _findRate(self, data):
        rate = self.reRate.findall(data)
        if(len(rate) == 0):
            rate = [0]
        return float(rate[0])

    def _findImages(self, data):
        return self.reImage.findall(data)

    def _findCategories(self, data):
        return self.reCat_2.findall(self.reCat_1.findall(data)[0])

    def _findDescription(self, data):
        des = self.reDes.findall(data)
        if(len(des) == 0):
            return "<div class=\"product-info-container\" style=\"display:block\"><h1>暂无描述</h1></div>"
        else:
            return des[0]


if __name__ == '__main__':
    test = ProductGetter_CWH()
    test.processProductWithUrl(
        'https://www.chemistwarehouse.com.au/buy/81818/Pediasure-Ready-To-Drink-Vanilla-200ml')
