from flask import render_template, abort, redirect, url_for, request, Flask, jsonify, make_response
from operate_data import insert_operaction, select_operaction, update_operaction
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    str = select_operaction("e.env_name env_name,e.env_url env_url, e.remote_ip remote_ip, e.call_num call_num, "
                      "p.branch branch ,p.git_id git_id ,p.update_time p_update_time,s.git_id s_git_id , "
                      "s.branch s_branch ,s.version version , s.conf_file conf_file,s.update_time s_update_time",
                      "env e,page p,system s","e.id = p.env_id and e.id = s.env_id")
    print(str)
    return render_template('index.html',str=str)

@app.route('/add_env')
def add_env():
    return render_template('add_env.html')

@app.route('/add_env_over', methods=['POST', 'GET'] )
def add_env_over():
    if request.method == 'POST':
        #取值
        env_name = request.form.get('env_name')
        env_url = (request.form.get('env_url'))
        remote_ip = request.form.get('remote_ip')
        call_num = request.form.get('call_num')
        page_git_id = request.form.get('page_git_id')
        page_git_branch = request.form.get('page_git_branch')
        system_git_id = request.form.get('system_git_id')
        system_git_branc = request.form.get('system_git_branc')
        version = request.form.get('version')
        conf_file = request.form.get('conf_file')

        #验证是否存在
        select_str = "env_name" + " = \"" + env_name + "\""
        select_result = select_operaction("env_name","env",select_str)
        #环境存在 报告异常，退出
        if len(select_result) != 0:
            return render_template('add_env_error.html',env_name = env_name)

        #不存在填写env表
        env_key_str = "env_name,env_url,remote_ip,call_num"
        env_valuses_str = "\"" + env_name + "\",\"" + env_url + "\",\"" + remote_ip + "\",\"" + call_num + "\""
        insert_operaction("env",env_key_str,env_valuses_str)

        #获取envid
        select_str = "env_name" + " = \"" + env_name + "\""
        select_result = select_operaction("id", "env", select_str)
        env_id = select_result[0][0]

        #插入page表
        update_time = time.strftime("%Y-%m-%d", time.localtime())
        page_key_str = "env_id,git_id,branch,update_time"
        page_valuses_str = str(env_id) + ", \"" + page_git_id + "\",\"" + page_git_branch + "\",\"" + update_time + "\""
        insert_operaction("page", page_key_str, page_valuses_str)


        #插入system表
        update_time = time.strftime("%Y-%m-%d", time.localtime())
        system_key_str = "env_id,git_id,branch,version,conf_file,update_time"
        system_valuses_str = str(env_id) + ", \"" + system_git_id + "\",\"" + system_git_branc + "\",\""  + version + "\",\"" + conf_file + "\",\""  + update_time + "\""
        insert_operaction("system", system_key_str, system_valuses_str)

        return render_template('add_env_over.html', env_name=env_name)
    # ,env_name = env_name,env_url = env_url,remote_ip = remote_ip,call_num = call_num,page_git_id = page_git_id,
    # page_git_branch = page_git_branch,system_git_id = system_git_id,system_git_branc = system_git_branc,version = version,conf_file = conf_file
    else:
        abort(404)

#上线登记
@app.route('/update_register')
def update_register():
    #返回所有环境id和环境名称供前端选择
    env = select_operaction("id,env_name", "env")
    return render_template('update_register.html',env = env)

@app.route('/update_register_over', methods=['POST', 'GET'] )
def update_register_over():
    if request.method == 'POST':
        #赋值
        env_id = request.form.get('env_id')
        page_git_id = request.form.get('page_git_id')
        page_git_branch = request.form.get('page_git_branch')
        system_git_id = request.form.get('system_git_id')
        system_git_branch = request.form.get('system_git_branch')
        version = request.form.get('version')

        #更新page表
        update_time = time.strftime("%Y-%m-%d", time.localtime())
        page_update_str1 = "git_id = \"" + page_git_id + "\","
        page_update_str2 = "branch = \"" + page_git_branch + "\","
        page_update_str3 = "update_time = \"" + update_time + "\" "
        page_update_str = page_update_str1 + page_update_str2 + page_update_str3
        page_update_key_str = "env_id = " + env_id
        update_operaction("page",page_update_str,page_update_key_str)

        #写入pagelog表
        page_log_key_str = "env_id,git_id,branch,update_time"
        page_log_valuses_str = str(env_id) + ", \"" + page_git_id + "\",\"" + page_git_branch + "\",\"" + update_time + "\""
        insert_operaction("page_log", page_log_key_str, page_log_valuses_str)

        #更新system表
        system_update_str1 = "git_id = \"" + system_git_id + "\","
        system_update_str2 = "branch = \"" + system_git_branch + "\","
        system_update_str3 = "version = \"" + version + "\","
        system_update_str4 = "update_time = \"" + update_time + "\" "
        system_update_str = system_update_str1 + system_update_str2 + system_update_str3 + system_update_str4
        system_update_key_str = "env_id = " + env_id
        update_operaction("system",system_update_str,system_update_key_str)

        #写入systemlog表
        system_log_key_str = "env_id,git_id,branch,version,update_time"
        system_log_valuses_str = str(env_id) + ", \"" + system_git_id + "\",\"" + system_git_branch + "\",\""  + version + "\",\""  + update_time + "\""
        insert_operaction("system_log", system_log_key_str, system_log_valuses_str)

        return render_template('update_register_over.html',env_id = env_id)
    else:
        abort(404)
#前端更新记录
#后端更新记录
#环境配置调整 rewrite
if __name__ == '__main__':
    app.run()
