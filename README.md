環境

Python 3.9.2
pip install flaskmysql-connector

xampp
https://www.apachefriends.org/zh_tw/index.html

----------------------------------------------------------
server功能(POST JSON) 

/login
request {'ID' : ID , 'passwd' : passwd}
return info{'result' : "1" , 'access_token' : token} or return info{'result' : '0'}

/logout
request {'access_token' : access_token}
return 0

/register
request {'ID' : ID , 'passwd' : passwd}
return info{'result' : "ID already exists"} or info{'result' : "register success"}

/changePasswd
request {'ID' : ID , 'passwd' : passwd , 'access_token' : access_token}
return info{'result' : "change password success"} or info{'result' : "change password fail"}

----------------------------------------------------------
mysql table

account {ID , passwd}
token {ID , access_token , logining_time , time_limit , status}

----------------------------------------------------------
myToken.py

secret_key = 'mantou'
def creat_jwt(id) :
header = {“alg” : “HS256” , “typ” : “JWT”}
payload = {“user” : id , “login_time” : str(time.time())}

----------------------------------------------------------
待更新
顯示記錄檔
上傳記錄檔
下載記錄檔
密碼雜湊
伺服器訊息
