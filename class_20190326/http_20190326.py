import requests
class Http():
    ''''''
    def __init__(self,url,method,param,cookie=None):
        self.url=url#请求地址
        self.method=method#请求方法get或者post
        self.param=param#请求参数
        self.cookie=cookie#请求cookie
    def http(self):
        if self.method.upper()=='GET':
            res=requests.get(self.url,params=self.param,cookies=self.cookie)#发起get请求
        elif self.method.upper()=='POST':
            res = requests.post(self.url, data=self.param, cookies=self.cookie)#发起post请求
        else:
            print('请求方法出错。')
            res=None
        return res
