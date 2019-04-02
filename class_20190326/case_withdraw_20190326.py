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

cf = Config('con_20190326', 'CASE', 'case_id')
cases=DoExcel('Excelcase.xlsx','withdraw')
case_1=cases.read()
# print(*case_1)
leaveamount_Sql=Config('con_20190326', 'mysql', 'Sql').getother()['sql']

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
        case_id = case['case_id']
        method=case['Method']
        url=case['URL']
        param=read_re(case['Params'])
        expect=case['ExcepectedResult']
        db = Config('con_20190326', 'mysql', 'db_config').getother()

        if case['Sql'] is not None:
            sql=(eval(case['Sql']))['sql']
            before_amount=Mysql(db,sql).select()[0]  #此处请求前的余额数字类型为int

        resp=Http(url,method,eval(param),cookie=getattr(Getdata,'COOKIE')).http()

        if resp.cookies:
            setattr(Getdata,'COOKIE',resp.cookies)

        Loger().INFO('正在执行第{}条用例，参数是{}，结果是{}'.format(case_id, param, resp.json()))

        try:
           if case['Sql'] is not None:
               sql = (eval(case['Sql']))['sql']
              # '''此处请求后的余额数字类型为int'''
               after_amount = Mysql(db, sql).select()[0]#请求后的余额
               expect_amount = before_amount -int(eval(param)['amount'])#期望余额
               self.assertEqual(expect_amount,after_amount)
           if case['ExcepectedResult'].find( 'Money')!=-1:#如果在期望值里面找到money这个字符串
               expect=case['ExcepectedResult'].replace('Money',str(expect_amount ))#就替换为我计算出来的期望余额
           self.assertEqual(eval(expect), resp.json())
           res='pass'
        except Exception as e :
            Loger(msglevel='ERROR').ERROR('断言出错啦,错误是{}'.format(e))
            res='failed'
            raise e
        finally:
            cases.write(case_id+1,9,resp.text)
            cases.write(case_id + 1, 10, res)
            cases.write(case_id + 1, 11, str(Mysql(db, leaveamount_Sql).select()[0]))

