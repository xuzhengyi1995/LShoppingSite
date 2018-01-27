# Temp code
# XUZhengyi, 25/01/2018

from GoogleTranslator import GoogleTranslator
from Db import Db
import threadpool
import time

c = Db().getCollection("products")
t = GoogleTranslator()


def tra(p, s):
    tran = t.translate(p['description'])['translatedText']
    c.update_one({'_id': i['_id']}, {'$set': {'description_cn': tran}})
    print('[TRANS]Finished:', s)
    # time.sleep(100)


x = c.find({}, projection={'description': True, 'description_cn': True})
s = 0
# tpool = threadpool.ThreadPool(num_workers=40)
# reqParams = []
for i in x:
    if(not i.get('description_cn')):
        s += 1
        tra(i, s)
        #time.sleep(3)
        '''
        reqParams.append(([i, s], None))
        print('[Request build]Finished:', s)
        '''
'''
requests = threadpool.makeRequests(tra, reqParams)
[tpool.putRequest(req) for req in requests]
tpool.wait()
'''
