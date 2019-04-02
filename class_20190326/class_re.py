import re
from class_20190326.getdata_20190326 import Getdata
def read_re(target):
    p='#(.*?)#'#匹配格式
    while re.search(p,target):#如果查找到匹配的字符串就进入循环
        m=re.search(p,target)#查找字符串里符合条件的字符串
        key=m.group(1)#去掉#号
        value=getattr(Getdata,key)#利用查找出来的key去寻找对应的值
        target=re.sub(p,value,target,count=1)#然后再把这个值替换到字符串中
    return target
if __name__ == '__main__':

    target='''{'mobilephone':'#phone#','pwd':'#pwd#'}'''
    print(read_re(target))
