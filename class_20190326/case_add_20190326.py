from ddt import ddt,data,unpack
import openpyxl
import unittest
from configparser import ConfigParser
import logging
import requests
import re
import json
from class_20190326 import loger_20190326
from class_20190326.excel_20190326 import DoExcel
from class_20190326.conf_20190326 import Config
from class_20190326.http_20190326 import Http
from class_20190326.loger_20190326 import Loger
from class_20190326.mysql_20190326 import Mysql
from class_20190326.getdata_20190326 import Getdata
from class_20190326.class_re import read_re
from mysql import connector
from class_20190326 import mysql_20190326


cases=DoExcel('Excelcase.xlsx','add')
case_1=cases.read()
leaveamount_Sql=Config('con_20190326', 'mysql', 'Sql').getother()['sql']
# print(*case_1)


@ddt
class Test_case(unittest.TestCase):
    def setUp(self):
       print('======开始执行测试啦======')
    def tearDown(self):
        print('======用例执行完毕啦======')
    @data(*case_1)
    def test_cases(self,case):
        global res
        global before_amount
        global expect_amount
        case_id = case['case_id']#用例编号
        method=case['Method']#请求方法
        url=case['URL']#请求地址

        param=read_re(case['Params'])#利用正则表达式查找并替换请求参数里面的电话号，密码，id,等等
        expect=case['ExcepectedResult']#期望值
        db = Config('con_20190326', 'mysql', 'db_config').getother()#数据库连接信息

        if case['Sql'] is not None:#如果表格里面sql栏不为空
            sql=(eval(case['Sql']))['sql']#就取出数据库查询的sql
            loanid=Mysql(db,sql).select()[0]  #查询加完标后的标ID
            setattr(Getdata,'loanid',str(loanid))#将ID 设置到getdata属性里面，便于利用正则替换

        resp=Http(url,method,eval(param),cookie=getattr(Getdata,'COOKIE')).http()#发起请求

        if resp.cookies:#如果请求完存在cookies
            setattr(Getdata,'COOKIE',resp.cookies)#就将cookies的值设置到geedata这个反射类里面去

        Loger().INFO('正在执行第{}条用例，参数是{}，结果是{}'.format(case_id, param, resp.json()))

        try:
           self.assertEqual(eval(expect), resp.json())#判断实际值与期望值是否相等
           res='pass'#相等就返回pass
        except Exception as e :
            Loger(msglevel='ERROR').ERROR('断言出错啦,错误是{}'.format(e))
            res='failed'
            raise e
        finally:
            cases.write(case_id+1,9,resp.text)#最后将请求返回结果写入到表格
            cases.write(case_id + 1, 10, res)#这是对比的结果
            cases.write(case_id + 1, 11, str(Mysql(db, leaveamount_Sql).select()[0]))#查询数据库余额写入到表格

