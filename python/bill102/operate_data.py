import mysql.connector
import time

def insert_bill( mingxi, jine, user):
    now_date = time.strftime("%Y-%m-%d", time.localtime())
    conn = mysql.connector.connect(
        user="bill", password="bill_zzz", host="fushisanlang.cn", database="bill_102"
    )
    cursor = conn.cursor()
    sql_parm_1 = 'INSERT INTO `bill_102` ( `date`, `mingxi`,`jine`, `user`) VALUES ('
    sql_parm_2 = '\'' + now_date + '\'' + ',\'' + mingxi + '\',' + jine + ',\''  + user +  '\'' + ') ;'
    sql = sql_parm_1 + sql_parm_2
    print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return
