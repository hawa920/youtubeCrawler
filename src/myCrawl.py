import re
import json
import time
import queue
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class myCrawler:

    def __init__(self, seedURL, maxVideoLen = 60 * 4 + 30, minVideoLen = 30, maxFetch = 128, timeGap = 5, bulkSize = 64):
        
        self.maxVideoLen = maxVideoLen
        self.minVideoLen = minVideoLen
        self.maxFetch = maxFetch
        self.timeGap = timeGap
        self.bulkSize = bulkSize
        self.seed_url = seedURL
    
    def lenInSec(self, vlen):

        secList = [1, 1 * 60, 1 * 60 * 60, 1 * 24 * 60 * 60]
        tsplit = re.findall('\d+\.?\d*', vlen)
        tsplit = [int(s) for s in tsplit]
        thisLen = 0
        for i in range(len(tsplit) - 1, -1, -1):
            thisLen = thisLen + tsplit[i] * secList[len(tsplit) - i - 1]
        return True if thisLen < self.maxVideoLen and thisLen > self.minVideoLen else False
    
    def goCrawl(self, seen_url, url_queue):
        
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Chrome(executable_path='../package/chromedriver', chrome_options=chrome_options)

        driver = webdriver.Chrome(executable_path = '../package/chromedriver')
        # push seed url into url_queue
        url_queue.put(self.seed_url)

        numOfFetch = 0
        bulkStream = []

        while not url_queue.empty() and numOfFetch < self.maxFetch:
            cur_url = url_queue.get()
            if cur_url in seen_url:
                print("Got some repeated url, return 'escape'.")
                continue
            # fetching
            driver.get(cur_url)
            # wait
            time.sleep(self.timeGap)
            # extract source code
            srcode = driver.page_source
            # init bs4
            bsoup = BeautifulSoup(srcode, 'html.parser')
            # get length of video
            vlen = bsoup.select('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div > span.ytp-time-duration')[0].text
            if not self.lenInSec(vlen):
                print("Current video length doesn't fit the limitation, return 'escape'.")
                continue
            numOfFetch += 1
            # label current url crawled
            seen_url[cur_url] = True
            print("[{0}]: {1}".format(numOfFetch, cur_url))
            # get video title
            title = bsoup.select('#container > h1 > yt-formatted-string')[0].text
            # get count of views
            cview = bsoup.select('#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer')[0].text
            # get number of likes and hates
            clike = bsoup.select('#text')[1].text
            chate = bsoup.select('#text')[2].text
            # get publish date
            pubtime = bsoup.select('#upload-info > span')[0].text
            # get owner of the video
            owner = bsoup.select('#owner-name > a')[0].text
            # get number of subscribe
            subscribe = bsoup.select('#subscribe-button')[1].text
            outStream = '@url:' + cur_url + '\n' + \
                    '@@title:' + title + '\n' + \
                    '@vlen:' + vlen + '\n' + \
                    '@cview:' + cview + '\n' + \
                    '@clike:' + clike + '\n' + \
                    '@chate:' + chate + '\n' + \
                    '@owner:' + owner + '\n' + \
                    '@pubtime:' + pubtime + '\n' + \
                    '@subscribe:' + subscribe + '\n\n'

            bulkStream.append(outStream)
            if(len(bulkStream) is self.bulkSize):
                with open('../storage/records', 'a') as fp:
                    for rec in bulkStream:
                        fp.write(rec)
                bulkStream.clear()
            
            # extract links
            all_url = bsoup.select('#dismissable > a')
            for new_url in all_url:
                url_queue.put('https://www.youtube.com' + new_url.get('href'))
                
        # write off the last batch
        with open('../storage/records', 'a') as fp:
            for rec in bulkStream:
                fp.write(rec)
        bulkStream.clear()
        driver.quit()

if __name__ == "__main__":

    # seen_url = {}
    # url_queue = queue.Queue()
    try:
        with open('../storage/save-seenPool', 'rb') as fp:
            seen_url = pickle.load(fp)
    # OSError | FileNotFoundError | No specification
    except OSError:
        seen_url = {}
    
    try:
        with open('../storage/save-urlPool', 'rb') as fp:
            qlist = pickle.load(fp)
            url_queue = queue.Queue()
            for ele in qlist:
                url_queue.put(ele)
    # OSError | FileNotFoundError | No specification
    except OSError:
        url_queue = queue.Queue()
    
    test = myCrawler(seedURL = 'https://www.youtube.com/watch?v=gsGn1dzITD0')
    test.goCrawl(seen_url, url_queue)

    """
    for i, j in seen_url.items():
        print(i,' -> ', j)

    for i in list(url_queue.queue):
        print(i)
    """
    # keep the seen pool in human language
    """
    with open('../storage/save-seenPool.json', 'w') as fp:
        fp.write(json.dumps(seen_url))
    """
    # keep the seen url pool (which is a dict) in binary
    with open('../storage/save-seenPool', 'wb') as fp:
        pickle.dump(seen_url, fp, protocol=pickle.HIGHEST_PROTOCOL)
    # keep the url pool (those in queue) in binary
    # since queue.Queue() is for threading purposes, it will have problems with pickle
    with open('../storage/save-urlPool', 'wb') as fp:
        pickle.dump(list(url_queue.queue), fp)