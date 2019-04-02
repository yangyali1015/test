from configparser import ConfigParser
class Config:
    def __init__(self,filename,section,option):
        self.filename=filename#配置文件名称
        self.section=section#片段名
        self.option=option#选项名
        self.cf=ConfigParser()#配置文件的对象
    def getint(self):#获取数字
        self.cf.read(self.filename,encoding='utf-8')
        result=self.cf.getint(self.section,self.option)
        return result
    def getboolean(self):#获取布尔值
        self.cf.read(self.filename,encoding='utf-8')
        result =self.cf.getboolean(self.section,self.option)
        return result
    def getfloat(self):#获取浮点
        self.cf.read(self.filename, encoding='utf-8')
        result =self.cf.getfloat(self.section, self.option)
        return result
    def getstr(self):#获取字符串
        self.cf.read(self.filename, encoding='utf-8')
        result =self.cf.get(self.section, self.option)
        return  result
    def getother(self):#获取其他类型
        self.cf.read(self.filename, encoding='utf-8')
        result =self.cf.get(self.section, self.option)
        return eval(result)

if __name__ == '__main__':
    cf=Config('con_20190326','excel_read','button')
    print(cf.getstr())