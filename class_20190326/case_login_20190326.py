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

cf = Config('con_20190326', 'CASE', 'case_id')
cases=DoExcel('Excelcase.xlsx','login')
case_1=cases.read()
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
        #参数如下
        case_id = case['case_id']
        method=case['Method']
        url=case['URL']
        param=read_re(case['Params'])
        expect=case['ExcepectedResult']
       #发起请求
        resp=Http(url,method,eval(param)).http()

        if resp.cookies:#判断cookies是否为空
            setattr(Getdata,'COOKIE',resp.cookies)

        Loger().INFO('正在执行第{}条用例，参数是{}，结果是{}'.format(case_id, param, resp.json()))

        try:
           self.assertEqual(eval(expect),resp.json())#断言结果
           res='pass'
        except Exception as e :
            Loger(msglevel='ERROR').ERROR('断言出错啦,错误是{}'.format(e))
            res='failed'
            raise e
        finally:
            cases.write(case_id+1,9,resp.text)
            cases.write(case_id + 1, 10, res)


