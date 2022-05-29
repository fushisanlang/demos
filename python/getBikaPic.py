import requests
import json
import time


def sendmessage(messagestr):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=bcfbfda3-5114-4694-8360-9289f6a0854d'
    messagejson = {"msgtype": "text", "text": {"content": messagestr}}
    messagejsondumps = json.dumps(messagejson)
    requests.post(url, messagejsondumps, headers={
                  'Content-Type': 'application/json;charset=utf-8'})
    return

import re ,os
j = 0
with open('2') as file_obj:
   for line in file_obj:

        line = line.strip('\n')
        if re.match('https', line) == None:
            s=line

            try:
                os.mkdir("./pics/" + line)
            except:
                print(line)
        else:


            head = {"Host":"i0.wp.com",'User-Agent': "Mozilla/5.0 #(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"}
            try:
                r = requests.get(url=line,headers=head)
            except:


                sendmessage("err at " + s + " "  +str(j))
            if r.status_code == 200:

                with open("./pics/" + s+ "/" + str(j)+".jpg",'wb') as f:

                    try:
                        f.write(r.content)
                    except:
                        f.close()

                    else:
                        f.close()

        j = j + 1

sendmessage("ok")
