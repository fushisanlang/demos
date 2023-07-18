import time
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://weibo.com/u/3591355593?is_all=1'

chrome_options = Options()
# 定义无窗口运行，否则在服务器环境会报错
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.set_window_size(1080,1920)
browser.get(url)
while 1:
 browser.refresh()
 time.sleep(10) 

 browser.save_screenshot('/home/python/sprider/wyf/pic/'+ str(time.time()) + '.png') 
browser.quit()
