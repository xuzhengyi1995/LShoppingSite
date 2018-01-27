# For google translate
# XUZhengyi, 23/01/2018

import json
from GetHtml import GetHtml
import settings


class GoogleTranslator:
    '''
    GoogleTranslate class.
    translate(text,lang='zh-cn').
    '''

    def __init__(self):
        self.url_t = 'https://translation.googleapis.com/language/translate/v2/'
        self.url_g = 'https://translation.googleapis.com/language/translate/v2/languages?target=%s&key=%s'
        self.key = settings.googletranslate_key

    def _getJson(self, url, _postData=False):
        getter = GetHtml()
        getter.set(url, postData=_postData)
        data = getter.get(wait_time=103).decode('utf-8')
        return json.loads(data)

    def getLanguages(self, lang='zh-cn'):
        data = self._getJson(self.url_g % (lang, self.key))
        return data['data']['languages']

    def translate(self, text, target='zh', _format='html'):
        post_data = {'q': text, 'target': target, 'format': _format, 'key': self.key}
        data = self._getJson(url=self.url_t, _postData=post_data)
        return data['data']['translations'][0]


if __name__ == '__main__':
    test = GoogleTranslator()
    # print(test.getLanguages())
    print(test.translate(text='I love you more than I can say.'))
    print(test.translate(text='Optislim VLCD Meal Replacement Chocolate Shake 21 x 40g'))
