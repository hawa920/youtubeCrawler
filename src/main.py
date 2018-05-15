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

def baseCrawler(baseURL, seen_url, url_queue):
    test = myCrawler(seedURL = baseURL, maxFetch = 1024)
    test.goCrawl(seen_url, url_queue)

if __name__ == "__main__":

    try:
        with open('../storage/save-seenPool', 'rb') as fp:
            seen_url = pickle.load(fp)
    except OSError:
        seen_url = {}

    try:
        with open('../storage/save-urlPool', 'rb') as fp:
            qlist = pickle.load(fp)
            url_queue = queue.Queue()
            for ele in qlist:
                url_queue.put(ele)
    except OSError:
        url_queue = queue.Queue()

    ulist = ['https://www.youtube.com/watch?v=r-d5HI-zC3I', 
             'https://www.youtube.com/watch?v=cIriwVhRPVA',
             'https://www.youtube.com/watch?v=tk36ovCMsU8',
             'https://www.youtube.com/watch?v=Mke9EHMQMYI',
             'https://www.youtube.com/watch?v=a7SouU3ECpU',
             'https://www.youtube.com/watch?v=EkHTsc9PU2A',
             'https://www.youtube.com/watch?v=hT_nvWreIhg',
             'https://www.youtube.com/watch?v=SXjXKT98esw',
             'https://www.youtube.com/watch?v=kjMNXpqmjb4',
             'https://www.youtube.com/watch?v=kVpv8-5XWOI'
            ]
    kthread = 6
    threadlist = []
    for i in range(kthread):
        t = threading.Thread(target=baseCrawler, args=(ulist[i], seen_url, url_queue))
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