import time
 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://cs.newchinalife.com/service-center/service/invoice/invoice-index'

chrome_options = Options()
# 定义无窗口运行，否则在服务器环境会报错
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.set_window_size(1080,1920)
browser.get(url)
time.sleep(1)
print(browser.title)
browser.quit()
