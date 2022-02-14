# -*- coding: utf-8 -*
# 封装参考:https://cloud.tencent.com/developer/article/1624558
# 实盘交易请注释 headers.update({"x-simulated-trading": "1"})
import datetime, requests, hmac, base64,json
from hashlib import sha256
from authorization import API_KEY, SECRET_KEY, PASSPHRASE
# 实盘交易地址
BASE_URL = "https://www.okx.com"
PUBLIC_URI = "wss://ws.okx.com:8443/ws/v5/public"
PRIVATE_URI = "wss://ws.okx.com:8443/ws/v5/private"

class RequestHandler:
    """通过底层request函数实现GET和POST方法、签名并添加请求头
    """
    def __init__(self):
        self.requests = requests
        self.secret_key = SECRET_KEY
        self.api_key = API_KEY
        self.passphrase = PASSPHRASE
    def visit(self,method,path,params=None,data=None,json=None,headers=None,**kwargs):
        """request请求
        """
        headers = self._get_header(method,path,body=json)
        url = "%s%s" % (BASE_URL,path)

        return self.requests.request(method,url,params=params,data=data,json=json,headers=headers,timeout=180,verify=True,**kwargs)
    def _get_header(self,method,path,body=''):
        """设置REST请求头
        """
        headers = {"Content-Type": "application/json","OK-ACCESS-KEY":self.api_key,"OK-ACCESS-PASSPHRASE":self.passphrase}
        # 时间戳
        ts = datetime.datetime.utcnow().isoformat("T", "milliseconds") + "Z"
        headers.update({"OK-ACCESS-TIMESTAMP":ts})
        # 签名
        if body is None:
            body = ''
        msg = str(ts) + str.upper(method) + path + body
        print("MESSAGE",msg)
        headers.update({"OK-ACCESS-SIGN":self._sign(msg)})
        print(self._sign(msg))
        # 模拟盘请求头
        headers.update({"x-simulated-trading": "1"}) # 实盘交易请注释
        return headers


    def _sign(self,msg): 
        """ 签名: 
            OK-ACCESS-SIGN请求头是对timestamp + method + requestPath + body字符串（+表示字符串连接），以及SecretKey，使用HMAC SHA256方法加密，通过Base-64编码输出而得到的
        """
        # 使用HMAC SHA256方法加密，通过Base-64编码输出
        signature = base64.b64encode(hmac.new(bytes(self.secret_key,encoding='utf-8'),bytes(msg,encoding='utf-8'),digestmod='sha256').digest())
        return signature
        
if __name__ == "__main__" :
    """测试封装 
    """
    req = RequestHandler()
    # 模拟盘请求头 !!! 请勿实盘测试
    headers = "{'x-simulated-trading': '1'}"
    # GET请求测试
    # get = req.visit("GET", "/api/v5/asset/currencies", headers=headers)
    # print(get.status_code)
    # print(get.text)
    # POST请求测试
    params = {
        "instId":"BTC-USDT",
        "tdMode":"cash",
        "clOrdId":"b15",
        "side":"buy",
        "ordType":"limit",
        "px":"2.15",
        "sz":"2"
    }
    post = req.visit("POST", "/api/v5/trade/order", json=json.dumps(params).replace(" ", ""), headers=headers)
    print(post.request.body)
    print(post.status_code)
    print(post.text)


    
