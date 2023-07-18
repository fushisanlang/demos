from flask import render_template,abort,redirect, url_for,request,Flask
from operate_data import insert_bill
from decimal import Decimal

app = Flask(__name__)

@app.route('/')
def index():
     #ip = request.headers.request.Remote-Host
     ip = request
     print(type(ip))
     return render_template('index.html', user_ip=ip)

@app.route('/insertresult',methods=['POST','GET'])
def insertresult():
    if request.method == 'POST':
        mingxi = request.form.get('mingxi')
        jine = request.form.get('jine')
        user = request.form.get('user')
        insert_bill(mingxi,jine,user)
        return render_template('poem.html')
    else:
        abort(404)



if __name__ == '__main__':
    app.run()
