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
    test = myCrawler(maxFetch = 512, minVideoLen = 120)
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

    ulist = [ 'https://www.youtube.com/watch?v=pD-2VsWaJo0']

    try:
        with open('../storage/save-urlPool', 'rb') as fp:
            qlist = pickle.load(fp)
            url_queue = queue.Queue()
            if len(qlist) is 0:
                raise Exception
            for ele in qlist:
                url_queue.put(ele)
    except:
        url_queue = queue.Queue()
        for url in ulist:
            url_queue.put(url)


    kthread = 2
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
