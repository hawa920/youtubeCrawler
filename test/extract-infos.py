import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# seed url
url = 'https://www.youtube.com/watch?v=CZlfbep2LdU'

# uncomment the below if want to run browser in background
"""
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='../package/chromedriver', chrome_options=chrome_options)
"""

driver = webdriver.Chrome(executable_path='../package/chromedriver')
# fetch the url
driver.get(url)
# wait for webdriver to load
time.sleep(5)
# get source of the page
src = driver.page_source

# init bs4
soup = BeautifulSoup(src, 'html.parser')

# extract the infos (vlen, title, cview, clike, chate, pubtime, subscribe, owner) No description so far
# sometimes the CSS selector will fail to work in Selenium

# get length of video
result = soup.select('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > div > span.ytp-time-duration')
vlen = result[0].text

# get title of the video
result = soup.select('#container > h1 > yt-formatted-string')
title = result[0].text

# get view count
result = soup.select('#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer')
cview = result[0].text

# get number of hates and likes
result = soup.select('#text')
clike = result[1].text
chate = result[2].text

# get publish time
result = soup.select('#upload-info > span')
pubtime = result[0].text

# get owner of the video
result = soup.select('#owner-name > a')
owner = result[0].text

# get number of subscribe
result = soup.select('#subscribe-button')
subscribe = result[1].text
outStream = '@url:' + url + '\n' + \
                    '@@title:' + title + '\n' + \
                    '@vlen:' + vlen + '\n' + \
                    '@cview:' + cview + '\n' + \
                    '@clike:' + clike + '\n' + \
                    '@chate:' + chate + '\n' + \
                    '@owner:' + owner + '\n' + \
                    '@pubtime:' + pubtime + '\n' + \
                    '@subscribe:' + subscribe

print(outStream)
driver.quit()