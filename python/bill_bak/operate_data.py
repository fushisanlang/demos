import mysql.connector
import time
#for get now status
def get_sum_all_data():
    conn = mysql.connector.connect(
        user="bill", password="bill_zzz", host="fushisanlang.cn", database="Bill"
    )
    cursor = conn.cursor()
    cursor.execute("select * from sumall;")
    result = cursor.fetchall()
    result_tuple = result[0]
    cursor.close()
    return result_tuple


# send a newest status to db
def insert_account_data(result_list):
    now_date = time.strftime("%Y-%m-%d", time.localtime())
    name_str='account'
    conn = mysql.connector.connect(
        user="bill", password="bill_zzz", host="fushisanlang.cn", database="Bill"
    )
    cursor = conn.cursor()
    sql1 = 'INSERT INTO bill (date, detail, bankcard, zhifubao, weixin, ccbcredit, bcmcredit,' \
           ' cmbcredit, zhongxincredit, cmbccredit, huabei, baitiao, jiebei, account) VALUES ( '
    sql2 = ' \'' + now_date + '\' ' + ' , ' + ' \'' + name_str + '\' ' + ' , '
    sql3 = str(result_list[0]) + ' , ' + str(result_list[1]) + ' , ' + str(result_list[2]) + \
           ' , ' + str(result_list[3]) + ' , ' + str(result_list[4]) + ' , ' + str(result_list[5]) + \
           ' , ' + str(result_list[6]) + ' , ' + str(result_list[7]) + ' , ' + str(result_list[8]) + \
           ' , ' + str(result_list[9]) + ' , ' + str(result_list[10]) + ' , ' + str(result_list[11]) + ');'
    sql = sql1 + sql2 + sql3

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return

def insert_bill( detail, jine, fform):
    now_date = time.strftime("%Y-%m-%d", time.localtime())
    conn = mysql.connector.connect(
        user="bill", password="bill_zzz", host="fushisanlang.cn", database="Bill"
    )
    cursor = conn.cursor()
    sql_parm_1 = 'INSERT INTO bill (date, detail, '
    sql_parm_2 = fform
    sql_parm_3 = ') VALUES ( \''
    sql_parm_4 = now_date + '\'' +',\'' + detail + '\',' + jine + ') ;'
    sql = sql_parm_1 + sql_parm_2 + sql_parm_3 + sql_parm_4
    print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return
