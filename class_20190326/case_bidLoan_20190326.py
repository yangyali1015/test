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

cases=DoExcel('Excelcase.xlsx','bidLoan')
case_1=cases.read()#读取表格
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

        case_id = case['case_id']
        method=case['Method']
        url=case['URL']

        param=read_re(case['Params'])
        expect=case['ExcepectedResult']
        db = Config('con_20190326', 'mysql', 'db_config').getother()

        if case['Sql'] is not None:
            sql=(eval(case['Sql']))['sql']
            loanid=Mysql(db,sql).select()[0]  #查询加完标后的标ID
            setattr(Getdata,'loanid',str(loanid))#将ID 设置到getdata属性里面，便于利用正则替换

        if case_id == 4:  # 如果这是一条投资的用例
            sql = (eval(case['Sql']))['sql']
            leaveamount = Mysql(db, sql).select()[0] - eval(param)['amount']  # 余额等于数据库查询到的余额减去投资金额
            cases.write(case_id + 1, 11, str(leaveamount))#将余额写入到表格

        resp=Http(url,method,eval(param),cookie=getattr(Getdata,'COOKIE')).http()

        if resp.cookies:
            setattr(Getdata,'COOKIE',resp.cookies)

        Loger().INFO('正在执行第{}条用例，参数是{}，结果是{}'.format(case_id, param, resp.json()))

        try:

            self.assertEqual(eval(expect), resp.json())
            res='pass'
        except Exception as e :
            Loger(msglevel='ERROR').ERROR('断言出错啦,错误是{}'.format(e))
            res='failed'
            raise e
        finally:
            cases.write(case_id+1,9,resp.text)
            cases.write(case_id + 1, 10, res)



