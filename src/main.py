from myCrawl import myCrawler
import re
import json
import time
import queue
import pickle
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


lock = threading.Lock()


def baseCrawler(seen_url, url_queue):
    test = myCrawler(maxFetch = 1, minVideoLen = 120)
    test.goCrawl(seen_url, url_queue)
    lock.acquire()
    with open('../storage/records', 'a') as fp:
        for rec in test.bulkStream:
            fp.write(rec)
    test.bulkStream.clear()
    lock.release()

if __name__ == "__main__":
    

    try:
        with open('../storage/save-seenPool', 'rb') as fp:
            seen_url = pickle.load(fp)
    except OSError:
        seen_url = {}

    ulist = ['https://www.youtube.com/watch?v=r-d5HI-zC3I',
             'https://www.youtube.com/watch?v=cIriwVhRPVA',
             'https://www.youtube.com/watch?v=tk36ovCMsU8',
             'https://www.youtube.com/watch?v=Mke9EHMQMYI',
             'https://www.youtube.com/watch?v=a7SouU3ECpU',
             'https://www.youtube.com/watch?v=EkHTsc9PU2A',
             'https://www.youtube.com/watch?v=hT_nvWreIhg',
             'https://www.youtube.com/watch?v=SXjXKT98esw',
             'https://www.youtube.com/watch?v=kjMNXpqmjb4',
             'https://www.youtube.com/watch?v=kVpv8-5XWOI',
             'https://www.youtube.com/watch?v=3ChgRbqGi-E',
             'https://www.youtube.com/watch?v=DkeiKbqa02g',
             'https://www.youtube.com/watch?v=vDSF07Rhfzw',
             'https://www.youtube.com/watch?v=Vzo-EL_62fQ',
             'https://www.youtube.com/watch?v=ZSM3w1v-A_Y',
             'https://www.youtube.com/watch?v=cB5e0zHRzHc',
             'https://www.youtube.com/watch?v=kWBE0sQC5L8'
            ]

    try:
        with open('../storage/save-urlPool', 'rb') as fp:
            qlist = pickle.load(fp)
            url_queue = queue.Queue()
            if url_queue.empty():
                raise Exception
            for ele in qlist:
                url_queue.put(ele)
    except:
        url_queue = queue.Queue()
        for url in ulist:
            url_queue.put(url)


    kthread = 6
    threadlist = []
    for i in range(kthread):
        t = threading.Thread(target=baseCrawler, args=(seen_url, url_queue))
        t.daemon = True
        threadlist.append(t)
        t.start()
    for t in threadlist:
        t.join()

    # keep the seen url pool (which is a dict) in binary
    with open('../storage/save-seenPool', 'wb') as fp:
        pickle.dump(seen_url, fp, protocol=pickle.HIGHEST_PROTOCOL)

    # keep the url pool (those in queue) in binary
    # since queue.Queue() is for threading purposes, it will have problems with pickle
    with open('../storage/save-urlPool', 'wb') as fp:
        pickle.dump(list(url_queue.queue), fp)
