from class_20190326.conf_20190326 import Config
from configparser import ConfigParser
class Getdata():
    COOKIE=None
    Leaveamount=0#余额
    loanid=0#标id
    phone=Config('con_20190326','mysql','normal_phone').getstr()#要替换的正常手机号
    pwd=Config('con_20190326','mysql','normal_pwd').getstr()#要替换的正常密码
    MId=Config('con_20190326','mysql','MId').getstr()
#要替换的正常成员id
# print(Getdata.MId)