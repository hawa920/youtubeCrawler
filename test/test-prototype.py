import re
import time
import queue
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# some constant settings
maxVlen = 4 * 60 + 30
secList = [1, 60, 3600, 86400]
numFetch = 0
maxFetch = 1024
gapFetch = 5
bulkSize = 32

# maintext file path
writePath = './test-records'

# initialize a file writer
fp = open(writePath, 'w')

# seed url
seed_url = 'https://www.youtube.com/watch?v=r-d5HI-zC3I'

# url queue
url_queue = queue.Queue()
url_queue.put(seed_url)

# seen db
seen_url = {}

# options for selenium chrome web driver
# uncomment the below codes if want to run browser in the background
"""
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
"""

# initialize web driver
driver = webdriver.Chrome(executable_path='../package/chromedriver')

# initialize a bulk outstreams
bulk = []

# Crawler Kernel
while not url_queue.empty() and numFetch < maxFetch:
    cur_url = url_queue.get()
    # see if the current url has been crawled
    if seen_url.get(cur_url) == True:
        print("Got some repeated url, return 'Escape'")
        continue

    # fetch the source code from given url
    driver.get(cur_url)
    # wait for js to load
    time.sleep(gapFetch)
    # get the source code
    srcode = driver.page_source
    # initialize bs4
    bsoup = BeautifulSoup(srcode, 'html.parser')
    
    # get video length
    vlen = bsoup.select('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div > span.ytp-time-duration')[0].text
    # filter out those album or self-remix long productions
    tsplit = re.findall('\d+\.?\d*', vlen)
    tsplit = [int(s) for s in tsplit]
    thisLen = 0
    for i in range(len(tsplit) - 1, -1, -1):
        thisLen = thisLen + tsplit[i] * secList[len(tsplit) - i - 1]
    if thisLen > maxVlen:
        print("current video length excceed the limitation, return 'Escape'.")
        continue

    # label crawled
    seen_url[cur_url] = True
    # counter adds by one
    numFetch = numFetch + 1
    print("[{0}]: {1}".format(numFetch, cur_url))
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
    bulk.append(outStream)

    if(len(bulk) == bulkSize):
        print("Write out {0} records!".format(bulkSize))
        for rec in bulk:
            fp.write(rec)
        bulk.clear()
    
    # code below is wrong
    """ 
    bulk.append(extract)
    if len(bulk) == bulkSize:
        for arec in bulk:
            fp.write(arec.printOut())
        bulk.clear()
    """

    # extract the music from sidebar not playlist
    all_url = bsoup.select('#dismissable > a')
    for new_url in all_url:
        url_queue.put('https://www.youtube.com' + new_url.get('href'))

driver.quit()

# write the rest of the records
for rec in bulk:
    fp.write(rec)
    bulk.clear()

fp.close()
"""
for i, j in seen_url.items():
    print(i, '\t\t:', j)
"""