import requests
import sys
import json
 

def getMd5Str(name):
    prefix=sys.prefix
    url="https://tools.fushisanlang.cn/api/getMd5Str"
    dataStr={"str":name+ prefix}
    data=json.dumps(dataStr)
    r=requests.post(url,data= data,headers={ 'Content-Type': 'application/json;charset=utf-8'})
    return r.text
#md5Str = getMd5Str("123")
def setProgress(name,progressNum,status,progressId):
    url ="https://tools.fushisanlang.cn/api/progress"
    dataStr= {"name":name,"progressNum":progressNum,"status":status,"progressId":progressId}
    data=json.dumps(dataStr)
    r=requests.post(url,data= data,headers={ 'Content-Type': 'application/json;charset=utf-8'})
    print(r.json())
#setProgress("123",15,"running",md5Str)