from flask import render_template,abort,redirect, url_for,request,Flask
from operate_data import get_sum_all_data,insert_account_data,insert_bill
from decimal import Decimal

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/insertresult',methods=['POST','GET'])
def insertresult():
    if request.method == 'POST':
        noun1 = request.form.get('noun1')
        noun4 = request.form.get('noun4')
        noun5 = request.form.get('noun5')
        insert_bill(noun4,noun5,noun1)
        return render_template('poem.html')
    else:
        abort(404)


#pingzhang
@app.route('/account')
def account():
    return render_template('account.html')

#pingzhangzhuangtai
@app.route('/accountstatus',methods=['POST','GET'])
def accountstatus():
    if request.method == 'POST':
        #get all status
        bankcard = Decimal(request.form.get('bankcard'))
        zhifubao = Decimal(request.form.get('zhifubao'))
        weixin = Decimal(request.form.get('weixin'))
        ccbcredit = Decimal(request.form.get('ccbcredit'))
        bcmcredit = Decimal(request.form.get('bcmcredit'))
        cmbcredit = Decimal(request.form.get('cmbcredit'))
        zhongxincredit = Decimal(request.form.get('zhongxincredit'))
        cmbccredit = Decimal(request.form.get('cmbccredit'))
        huabei = Decimal(request.form.get('huabei'))
        baitiao = Decimal(request.form.get('baitiao'))
        jiebei = Decimal(request.form.get('jiebei'))
        account = Decimal(request.form.get('account'))
        get_list=[]
        # put all status in list
        get_list.extend([
            bankcard,zhifubao,weixin,ccbcredit,bcmcredit,cmbcredit,
            zhongxincredit,cmbccredit,huabei,baitiao,jiebei,account
        ])

        # get db now status
        result_tuple = get_sum_all_data()
        result_list = list(result_tuple)

        #operate date,get need insert data
        for i in range(len(result_list)):
            result_list[i] = float(Decimal(0) - (result_list[i]-get_list[i]))

        #insert date to db
        insert_account_data(result_list)
        return 'insert ok!'
    else:
        #get return 404
        abort(404)


if __name__ == '__main__':
    app.run()
