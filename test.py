from flask import Flask, jsonify, request
import mysql.connector
import json
import time
import os

app = Flask(__name__)
app.config["DEBUG"] = True

# login
@app.route('/login', methods=['GET'])
def login():
    info = dict()
    info['result'] = "1"
    return jsonify(info)

app.run('127.0.0.1', port=5000,ssl_context=('server.crt','server.key'))
