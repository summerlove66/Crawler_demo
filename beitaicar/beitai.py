import requests
import pymongo
import time
import json
import random
from multiprocessing.dummy import Pool
import socket
socket.setdefaulttimeout(10)

conn = pymongo.MongoClient()  # 连接Mongodb
tdb = conn.Car1  # 数据库
post_info = tdb.beitaicar  # 表


download_num = 0
miss_urls=[]
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}

# redo>1 时 若下载失败时 将再次下载
def get_car(page_num, redo=2):
    global download_num
    download_num += 1
    if download_num % 100 == 0:
        time.sleep(5 * random.random())


    try:
        t = str(time.time()).replace('.', '')[:13]
        res = requests.get('http://www.btjf.com/business/car/list?r=t&pageSize=20&currentPage={}'.format(page_num),
                         headers=headers )
        html = res.text
        hd = json.loads(html)
        for ele in hd['object']:
            del ele['publishTime']
            ele['firstRegDate'] = time.strftime('%Y-%m-%d', time.localtime(ele['firstRegDate'] / 1000))
            post_info.insert(ele)

    except Exception as e:
        print(page_num)
        print(e)

        time.sleep(6*random.random())
        if redo > 1:
            redo -= 1
            get_car(page_num, redo)
        else:
            miss_urls.append(page_num)  
            print('错过，{}'.format(page_num))

            return


if __name__ == '__main__':
    pool =Pool(6)
    pool.map(get_car,range(1,1560))
    a =input('追捕遗漏的url? y/n')
    if a =='y':
        print(miss_urls)
        map(get_car,miss_urls)
    else:
        print(miss_urls)
