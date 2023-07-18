from flask import render_template, abort, redirect, url_for, request, Flask, jsonify, make_response
from operate_data import insert_operaction, select_operaction
from decimal import Decimal
import datetime
import time
app = Flask(__name__)

@app.route('/')
def hello_world():

    now_date = time.strftime("%Y-%m-%d", time.localtime())

    result_list = select_operaction('dateid,lyt,zy,jine','battle','date = "'+ now_date + '"')
    idlist=[]
    liulist=[]
    zhanglist=[]
    jinelist=[]
    for i in range(len(result_list)):
        idlist.append(result_list[i][0])
        liulist.append(result_list[i][1])
        zhanglist.append(result_list[i][2])
        jinelist.append(result_list[i][3])
    sum_list = select_operaction('date,sum(jine)','battle','date >=DATE_SUB(curdate(),INTERVAL 7 DAY) GROUP BY date')
    datelist=[]
    sumjinelist_liu=[]
    sumjinelist_zhang=[]
    for j in range(len(sum_list)):
        datelist.append(sum_list[j][0])
        sumjinelist_liu.append(sum_list[j][1])
        sumjinelist_zhang.append(0-sum_list[j][1])
    return render_template('index.html',idlist=idlist,liulist=liulist,zhanglist=zhanglist,jinelist=jinelist,sumjinelist_liu=sumjinelist_liu,sumjinelist_zhang=sumjinelist_zhang,datelist=datelist)


#记账
@app.route('/insertresult', methods=['POST', 'GET'])
def insertresult():
    now_date = time.strftime("%Y-%m-%d", time.localtime())
    now_id = select_operaction('count(1)+1','battle','date = "'+ now_date + '"')
     
    try :
        kill = int(request.form.get('kill'))
    except BaseException:
        kill = 0
    liu = int(request.form.get('liu'))
    zhang = int(request.form.get('zhang'))
    jine = ( liu - zhang ) * 5 + kill

    if liu == 1:
        jine = jine - 20
    if zhang == 1:
        jine = jine + 20
    jine = 0 - jine       
    now_id = now_id[0][0]
    insert_operaction('battle','date,dateid,lyt,`kill`,zy,jine','"' + str(now_date) + '",' + str(now_id) + ',' + str(liu) + ',' + str(kill) + ',' + str(zhang) + ',' + str(jine)  )
    return redirect('/')


if __name__ == '__main__':
    app.run()