import requests
from Crypto.Cipher import AES
import time

def progressbar(now, total):
    prefix='progress:'
    print('\r' + prefix  + int(now/total*50)*'+' +int(50-now/total*50)*'-' , end='')

def bytesToHexString(bs):
    return ''.join(['%02X ' % b for b in bs])

def getpass(password):
    key = '-=1skf.|asdqwfls'
    vi = '=-,asmfF[]|mq313'
    data = pad(password)
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    data = bytesToHexString(encryptedbytes).replace(' ', '')
    return data

def login(useremail, password):
    #url = 'https://ecosys.china-inv.cn/api/auth/login'
    #head = {"Content-Type": "application/x-www-form-urlencoded", "Host": "ecosys.china-inv.cn",
    #        'User-Agent': "Mozilla/5.0 #(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
    #requestdata = 'email=' + useremail + ' &password=' + password
    #r = requests.post(url, data=requestdata, headers=head, timeout=5)
    #accessToken = r.json()['access_token']
    #refreshToken = r.json()['refresh_token']
    accessToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6ImF0K2p3dCJ9.eyJuYmYiOjE2NTk4ODk0NjYsImV4cCI6MTY1OTg5MzA2NiwiaXNzIjoiaHR0cHM6Ly9pZHMuY2hpbmEtaW52LmNuIiwiYXVkIjpbImVjb3N5cyIsImVjb3N5c3JjIiwic2VuZGNvZGUiLCJzdmMiXSwiY2xpZW50X2lkIjoiZWNvc3lzIiwic3ViIjoiemhhbmd5aW5AZS1uY2kuY29tIiwiYXV0aF90aW1lIjoxNjUzMDIwOTMyLCJpZHAiOiJsb2NhbCIsIm5hbWUiOiLlvKDlvJUiLCJlbWFpbCI6InpoYW5neWluQGUtbmNpLmNvbSIsImRlcGFydG1lbnQiOiLkuLTml7bpg6jpl6giLCJjb21wYW55Ijoi5paw5Y2O55S15ZWG5YWs5Y-4IiwiZGl2aXNpb24iOiIiLCJlbXBsb3llZWlkIjoiMzE4MTEyIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwianRpIjoiQzZGNTg1OEE2ODhDQjk0Mjk3NEI4NkVFRjBDNjk5RTkiLCJpYXQiOjE2NTMwMjA5MzIsInNjb3BlIjpbImVjb3N5cyIsImVjb3N5c3JjIiwib3BlbmlkIiwic2VuZGNvZGUiLCJzdmMiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsiRW1haWxQYXNzd29yZCJdfQ.cL5AJ9LYNtHaOiCrbTQ7577D9hXfcsbSmHnqE1ULZUAA3htb9LC515wcj101QrIGzXSgvD7wfchItkeLRfNXCFqX7vsiOmChbkRttdB10O0OYHDc_4iRBZm8AsVbH84MViwn-BuWOqKBev83X_6O4Cr4AJCQKOv5LjWBcT6PWai_0pauHI560-aACen9umaxLcUGoUUxG88EH3n57hMBAb62k3Y_9gLyPY9ZWelkLwyoagh8ODsrhCX4A8S5dgpMYuYCevHQVWGnevZiP3Eug0a_uXpic4xCjt51njtegn9fC3SrCURTBiQlhDyHzvaKxqGOnnrsaypuoBkKHlPHjw'
    refreshToken = '58059CD9F6925A55C885DCFFCE54E0119A50574A927EFDF4805C89D3E4E890D6'
    return accessToken, refreshToken

#推荐资讯
def getContentIdList1(pagenum ,maxContentPage, accessToken, refreshToken):
    contentIdList = []
   
    while pagenum <= maxContentPage:
        url = "https://ecosys.china-inv.cn/api/content/independent/intelligentRecommendation/page"
        requestdata = 'pageSize=10&type=1&unread=1&pageNum=' + str(pagenum)
        head = {"accessToken": accessToken,
                "refreshToken": refreshToken, "Content-Type": "application/x-www-form-urlencoded", "Host": "ecosys.china-inv.cn",  "Cache-Control": "no-cache", 'User-Agent': "Mozilla/5.0  #Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
        r = requests.post(url, headers=head, data=requestdata, timeout=5)
        datas = r.json()['data']['records']
        if datas == []:
            break
        for data in datas:
            contentIdList.append(data['contentId'])
        pagenum = pagenum + 1
    return contentIdList
#党建
def getContentIdList2(pagenum,maxContentPage, accessToken, refreshToken):
    contentIdList = []
   
    while pagenum <= maxContentPage:
        url = "https://ecosys.china-inv.cn/api/content/list?qtime=1649748306329&pageNum=" + str(pagenum) + "&pageSize=10&columnId=2&needAll=true&orgId="
        head = {"accessToken": accessToken,
                "refreshToken": refreshToken, "Content-Type": "application/x-www-form-urlencoded", "Host": "ecosys.china-inv.cn",  "Cache-Control": "no-cache", 'User-Agent': "Mozilla/5.0  #Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
        r = requests.get(url, headers=head, timeout=5)
        
        datas = r.json()['data']
        if datas == []:
            break
        for data in datas:
            contentIdList.append(data['contentId'])
        pagenum = pagenum + 1
    return contentIdList
#资讯
def getContentIdList3(pagenum,maxContentPage, accessToken, refreshToken):
    contentIdList = []
 
    while pagenum <= maxContentPage:
        url = "https://ecosys.china-inv.cn/api/content/list?qtime=1649748354412&needAll=true&pageNum="+ str(pagenum) +"&pageSize=10&columnId=ecosysNews" 
        head = {"accessToken": accessToken,
                "refreshToken": refreshToken, "Content-Type": "application/x-www-form-urlencoded", "Host": "ecosys.china-inv.cn",  "Cache-Control": "no-cache", 'User-Agent': "Mozilla/5.0  #Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
        r = requests.get(url, headers=head, timeout=5)
        
        datas = r.json()['data']
        if datas == []:
            break
        for data in datas:
            contentIdList.append(data['contentId'])
        pagenum = pagenum + 1
    return contentIdList
#研报
def getContentIdList4(pagenum,maxContentPage, accessToken, refreshToken):
    contentIdList = []
  
    while pagenum <= maxContentPage:
      
        url="https://ecosys.china-inv.cn/api/content/list?qtime=1649750229202&pageNum="+ str(pagenum) +"&pageSize=10&columnId=3&needAll=true&needExchange=false" 
        head = {"accessToken": accessToken,
                "refreshToken": refreshToken, "Content-Type": "application/x-www-form-urlencoded", "Host": "ecosys.china-inv.cn",  "Cache-Control": "no-cache", 'User-Agent': "Mozilla/5.0  #Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
        r = requests.get(url, headers=head, timeout=5)
        
        datas = r.json()['data']
        if datas == []:
            break
        for data in datas:
            contentIdList.append(data['contentId'])
        pagenum = pagenum + 1
    return contentIdList

def readAndStarAndMark(accessToken, refreshToken, contentIdList):
    contentIdListLen = len(contentIdList)
    i = 0
    for contentId in contentIdList:
        
        # 阅读
        contentUrl = 'https://ecosys.china-inv.cn/api/content?qtime=1649660333710&contentId=' + \
            str(contentId)
        head = {"accessToken": accessToken,
                "refreshToken": refreshToken, "Content-Type": "application/x-www-form-urlencoded", "Host": "ecosys.china-inv.cn",  "Cache-Control": "no-cache", 'User-Agent': "Mozilla/5.0  #Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
        try:
            r = requests.get(contentUrl, headers=head, timeout=5)
        except:
            time.sleep(1)
        
        # 点赞
        starUrl = "https://ecosys.china-inv.cn/api/content/independent/content/behavior"
        requestdata = 'userBehavior=PRAISE&resourceId=' + str(contentId)
        try:
            r = requests.post(starUrl, data=requestdata, headers=head, timeout=5)
        except:
            time.sleep(1)
        # 收藏
        markUrl = "https://ecosys.china-inv.cn/api/content/independent/content/behavior"
        requestdata = 'userBehavior=COLLECTION&resourceId=' + str(contentId)
        try:
            r = requests.post(markUrl, data=requestdata, headers=head, timeout=5)
        except:
            time.sleep(1)
        i = i+1
        progressbar(i,contentIdListLen)


BLOCK_SIZE = 16  # Bytes
def pad(s): return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
def unpad(s): return s[:-ord(s[len(s) - 1:])]

#页码，每页10篇文章
#起始文章列表页码
pageStartNum=1
#终止文章列表页码
pageStopNum =100


#用户和密码
useremail = 'zhangyin@e-nci.com'
password = 'abcd@1234'

#print("总篇数" + str(maxContentPage * 10) + ',任务开始')
#加密密码
passwordDecode = getpass(password)
#登录
accessToken, refreshToken = login(useremail, passwordDecode)
#获取文章列表
contentIdList1 = getContentIdList1(pageStartNum,pageStopNum, accessToken, refreshToken)
contentIdList2 = getContentIdList2(pageStartNum,pageStopNum, accessToken, refreshToken)
contentIdList3 = getContentIdList3(pageStartNum,pageStopNum, accessToken, refreshToken)
contentIdList4 = getContentIdList4(pageStartNum,pageStopNum, accessToken, refreshToken)
contentIdList = contentIdList1 + contentIdList2 + contentIdList3+ contentIdList4
contentIdList=list(set(contentIdList))
print("共读取到" + str(len(contentIdList)) + "篇文章，操作开始")
#文章操作
readAndStarAndMark(accessToken, refreshToken, contentIdList)
print("任务完成")
