from mysql import connector
from class_20190326.conf_20190326 import Config
from configparser import  ConfigParser

class Mysql():
    def __init__(self,db,sql,flag=1):
        self.db=db
        self.sql=sql
        self.flag=flag#等于1就默认返回一条数据
    def select(self):
        cnn=connector.connect(**self.db)#链接数据库
        cursor=cnn.cursor()#获取游标
        cursor.execute(self.sql)#执行sql
        if self.flag==1:
            res=cursor.fetchone()#返回一条
        else:
            res = cursor.fetchall()#返回全部
        return res

if __name__ == '__main__':
    db=Config('con_20190326','mysql','db_config').getother()
    sql={'sql':'select LeaveAmount from member where MobilePhone=13512365669'}
    print(type(eval(str(Mysql(db,sql['sql']).select()[0]))))