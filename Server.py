from flask import Flask, jsonify, request
import myToken
import mysql.connector
import json
import time
import os

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
    conn.execute(
        "SELECT IF((SELECT 1 FROM account where BINARY ID='" + ID +
        "' AND BINARY passwd='" + passwd + "') ,1,0)"
    )
    result_set = conn.fetchone()  # mysql return 1 or 0
    info = dict()
    if result_set[0] == 1:
        access_token = myToken.creat_jwt(ID)
        logining_time = time.asctime(
            time.localtime(time.time()))  # logining time
        time_limit = int(time.time()) + 3600  # token time limit 1hr
        conn.execute(
            "UPDATE token SET status='Login elsewhere' WHERE ID='" + ID + "'"
        )
        conn.execute(
            "INSERT INTO token values ('" + ID + "','" + access_token +
            "','" + logining_time + "','" + str(time_limit) + "','login')"
        )
        mydb.commit()
        info['access_token'] = access_token
        info['result'] = "1"

    return jsonify(info)  # login success return token


# register
@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.get_data())
    ID = data['ID']
    passwd = data['passwd']
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
            "','" + passwd + "')"
        )
        mydb.commit()
        info['result'] = "register success"

    return jsonify(info)


# logout
@app.route('/logout', methods=["POST"])
def logout():
    data = json.loads(request.get_data())
    ID = data['ID']
    access_token = data['access_token']
    now_time = int(time.time())
    conn.execute(
        "SELECT IF((SELECT 1 FROM token where BINARY ID= '" + ID + "' AND access_token= '" +
        access_token + "'AND time_limit >'" + str(now_time) + "'AND status='login'), 1, 0)"
    )
    result_set = conn.fetchone()
    info = dict()
    if result_set[0] == 1:
        conn.execute(
            "UPDATE token SET status='logout' WHERE access_token='" + access_token + "'"
        )
        mydb.commit()
        info['result'] = "logout success"
    else:
        info['result'] = "Logged out"

    return jsonify(info)


app.run('127.0.0.1', port=5000)
