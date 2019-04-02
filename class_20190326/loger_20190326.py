import logging
from class_20190326 .conf_20190326 import Config
from configparser import ConfigParser


class Loger():
    def __init__(self,format=Config('con_20190326','loger','format').getstr(),logername='py14',filename='py14日志收集器',msglevel='DEBUG',logerlevel='DEBUG',filelevel='DEBUG',handlerlevel='DEBUG',):
        self.logername=logername#日志收集器名称
        self.logerlevel=logerlevel#收集器级别
        self.filename=filename#文件输出渠道名称
        self.filelevel=filelevel#文件输出渠道级别
        self.handlerlevel=handlerlevel#控制台输出级别
        self.format=format#日志格式
        self.msglevel=msglevel#要打印的日志的级别
    def loger(self,msg):
        loger=logging.getLogger(self.logername)#设置收集器
        loger.setLevel(self.logerlevel)#设置级别

        fomater=logging.Formatter(self.format)#格式
        ch=logging.StreamHandler()#输出渠道为控制台
        ch.setLevel(self.handlerlevel)#设置控制台级别
        ch.setFormatter(fomater)#设置输出格式

        fh=logging.FileHandler(self.filename,encoding='utf-8')#设置文件输出渠道
        fh.setLevel(self.filelevel)
        fh.setFormatter(fomater)

        loger.addHandler(ch)#连接收集器和输出渠道
        loger.addHandler(fh)

        if self.msglevel.upper()=='INFO':
            loger.info(msg)
        if self.msglevel.upper() == 'DEBUG':
                loger.debug(msg)
        if self.msglevel.upper() == 'WARNNING':
            loger.warning(msg)
        if self.msglevel.upper()=='ERROR':
            loger.error(msg)
        if self.msglevel.upper()=='CRITICAL':
            loger.critical(msg)

        loger.removeFilter(fh)#移除输出渠道
        loger.removeFilter(ch)

    def DEBUG(self,msg):
        Loger().loger(msg)
    def INFO(self,msg):
        Loger().loger(msg)
    def WARNING(self,msg):
        Loger().loger(msg)
    def ERROR(self,msg):
        Loger().loger(msg)
    def CRITICAL(self,msg):
        Loger().loger(msg)

if __name__ == '__main__':
    # format=Config('con_20190326','loger','format').getstr()
    Loger().DEBUG('测试日志')
