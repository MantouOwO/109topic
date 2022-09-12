from flask import Flask, jsonify, request
import myToken
import mysql.connector
import json
import time
import hashlib


mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    db="server"
)

conn = mydb.cursor()  # db connect

app = Flask(__name__)
app.config["DEBUG"] = True

# login


@app.route('/login', methods=['POST'])
def login():
    
    data = json.loads(request.get_data())
    ID = data['ID']
    passwd = data['passwd']

    passwd_md5 = hashlib.md5()  # 密碼雜湊
    passwd_md5.update(passwd.encode("utf-8"))

    conn.execute(
        "SELECT IF((SELECT 1 FROM account where BINARY ID='" + ID +
        "' AND BINARY passwd='" + passwd_md5.hexdigest() + "') ,1,0)"
    )
    result_set = conn.fetchone()  # mysql return 1 or 0

    info = dict()
    if result_set[0] == 1:
        access_token = myToken.creat_jwt(ID)  # 生成token
        access_token_md5 = hashlib.md5()  # token雜湊
        access_token_md5.update(access_token.encode("utf-8"))

        logining_time = time.asctime(
            time.localtime(time.time()))  # logining time
        time_limit = int(time.time()) + 3600  # token time limit 1hr

        conn.execute(
            "UPDATE token SET status='Login elsewhere' WHERE ID='" + ID + "'"
        )
        conn.execute(
            "INSERT INTO token values ('" + ID + "','" + access_token_md5.hexdigest() +
            "','" + logining_time + "','" + str(time_limit) + "','login')"
        )
        mydb.commit()
        info['access_token'] = access_token
        info['result'] = "1"
    else:
        info['result'] = "0"

    return jsonify(info)  # login success return token


# register
@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.get_data())
    ID = data['ID']
    passwd = data['passwd']
    passwd_md5 = hashlib.md5()  # 密碼雜湊
    passwd_md5.update(passwd.encode("utf-8"))
    conn.execute(
        "SELECT IF((SELECT 1 FROM account where BINARY ID='" + ID + "'), 1, 0)"
    )
    result_set = conn.fetchone()
    info = dict()
    if result_set[0] == 1:
        info['result'] = "ID already exists"
    else:
        passwd = data['passwd']
        conn.execute(
            "INSERT INTO account values ('" + ID +
            "','" + passwd_md5.hexdigest() + "')"
        )
        mydb.commit()
        info['result'] = "register success"

    return jsonify(info)


# logout  #修改須確認
@app.route('/logout', methods=["POST"])
def logout():
    data = json.loads(request.get_data())
    access_token = data['access_token']
    now_time = int(time.time())
    conn.execute(
       "SELECT IF((SELECT 1 FROM token where access_token= '" +
       access_token + "'AND time_limit >'" + str(now_time) + "'AND status='login'), 1, 0)"
     )
    result_set = conn.fetchone()
    #info = dict()
    if result_set[0] == 1:
        conn.execute(
            "UPDATE token SET status='logout' WHERE access_token='" + access_token + "'"
        )
        mydb.commit()

    return

# changePasswd
@app.route('/changePasswd', methods=["POST"])
def changePasswd():
    data = json.loads(request.get_data())
    ID = data['ID']
    newPasswd = data['newPasswd']
    newPasswd_md5 = hashlib.md5()
    newPasswd_md5.update(newPasswd.encode("utf-8"))

    access_token = data['access_token']
    access_token_md5 = hashlib.md5()  # token雜湊
    access_token_md5.update(access_token.encode("utf-8"))

    now_time = int(time.time())
    conn.execute(
        "SELECT IF((SELECT 1 FROM token where access_token= '" +
        access_token_md5.hexdigest() + "'AND time_limit >'" +
        str(now_time) + "'AND status='login'), 1, 0)"
    )
    result_set = conn.fetchone()
    info = dict()
    if result_set[0] == 1:
        conn.execute(
            "UPDATE account SET passwd = '" + newPasswd_md5.hexdigest() + "'WHERE ID='" + ID + "'"
        )
        mydb.commit()
        info['result'] = "change password success"
    else:
        info['result'] = "change password fail"

    return jsonify(info)


app.run('127.0.0.1', port=5000)
