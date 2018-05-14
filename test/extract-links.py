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

# get the music links on the side bar
links = soup.select('#dismissable > a')
# get the musuc links on the side playlist
# result = soup.select('#wc-endpoint')
for link in links:
    print('https://www.youtube.com' + link.get('href'))
driver.quit()