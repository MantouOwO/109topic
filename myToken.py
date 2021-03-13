import time
import base64
import hmac
import hashlib 
import binascii

#參考資料:https://medium.com/mr-efacani-teatime/%E6%B7%BA%E8%AB%87jwt%E7%9A%84%E5%AE%89%E5%85%A8%E6%80%A7%E8%88%87%E9%81%A9%E7%94%A8%E6%83%85%E5%A2%83-301b5491b60e
secret_key = 'mantou'

def toBytes(string):
	return bytes(string,'utf-8')

def encodeBase64(text):
	return base64.urlsafe_b64encode(text).replace(b'=',b'')

def creat_jwt(id):
    header	= '{"alg":"HS256","typ":"JWT"}'
    payload = '{"user":' + id +',"login_time":' + str(time.time()) +'}'

    #jwt = header.payload 
    jwt = encodeBase64(toBytes(header)) + toBytes('.') + encodeBase64(toBytes(payload))
    hs256 = hmac.new(toBytes(secret_key), jwt).digest()
    
    return encodeBase64(hs256).decode("utf-8")

