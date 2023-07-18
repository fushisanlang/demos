import requests
import json

def signin():
    url = "https://farm-server.fushisanlang.cn/user/signin"
    datastr = {"UserName": "符十三郎", "Password": "yierer333"}
    datajson = json.dumps(datastr)
    r = requests.post(url, data=datajson)
    return "gfsessionid=" + str(r.cookies).split("=", -1)[1].split(' ', -1)[0]

def auto(sessionid):
    url = "https://farm-server.fushisanlang.cn/field/auto"
    requests.get(url=url,  headers={
        'Content-Type': 'application/json;charset=utf-8', 'Cookie': sessionid})
    return

def getfieldinfo(sessionid):
    url = "https://farm-server.fushisanlang.cn/field/info/1"
    r = requests.get(url=url,  headers={
        'Content-Type': 'application/json;charset=utf-8', 'Cookie': sessionid})
    return r.json()["Status"]

def getbaginfo(sessionid):
    url = "https://farm-server.fushisanlang.cn/bag/info"
    r = requests.get(url=url,  headers={
        'Content-Type': 'application/json;charset=utf-8', 'Cookie': sessionid})
    count = 0
    for i in r.json():
        if i["PlantId"] == 42:
            count = i["Count"]
    return count

def buyplant(sessionid, count):
    url = "https://farm-server.fushisanlang.cn/store/buy"
    datastr = {"plantId": 42, "buyCount": 18-count}
    datajson = json.dumps(datastr)

    
    r = requests.post(url=url, data=datajson, headers={
        'Content-Type': 'application/json;charset=utf-8', 'Cookie': sessionid})
    datajson = json.dumps(datastr)
    print(r.json())
   
    return r.status_code

def plant(sessionid):
    url = "https://farm-server.fushisanlang.cn/field/plantall"
    datastr = {"plantId": 42}
    datajson = json.dumps(datastr)
    r=requests.post(url=url, data=datajson, headers={
        'Content-Type': 'application/json;charset=utf-8', 'Cookie': sessionid})
    print(r.json())
    return

sessionid = signin()
auto(sessionid)
if getfieldinfo(sessionid) == 1:
    count = getbaginfo(sessionid)
    buyplant(sessionid, count)
    plant(sessionid)
