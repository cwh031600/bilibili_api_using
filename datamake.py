import sqlite3
import requests
import time
import bilbliapi
import AGNES
import math

data = []
D = []
last_data = []
def dataout():
    '''
    此函数用于导出相关数据，输入up主的mid，导出关注，阅读等信息,返回元组数据
    '''
    global data
    conn = sqlite3.connect('data.db')    #连接数据库 
    data = conn.execute("select * from data").fetchall() #返回现在已有的全部数据
    print(data)
    return 0

def testdata2out():
    '''
    此函数用于导出相关数据，输入up主的mid，导出关注，阅读等信息,返回元组数据
    '''
    global data
    conn = sqlite3.connect('data.db')    #连接数据库 
    data = conn.execute("select * from testdata2").fetchall() #返回现在已有的全部数据
    print(data)
    return 0

def makedatabase():
    '''
    此方法为演示使用的适用方法
    1.处理数据，数据主要为：关注数，点赞数，阅读量+播放量
    **主要目的：将数据处理为二维坐标的形式，为后续AGNES算法做准备，(阅读量+播放量)/关注数 ; 点赞数/关注数
    2.数据入库，方便下次选用
    数据库分为三个选项，分别是主键up的mid，用户黏度，与喜爱程度,取整
    '''
    global data
    conn = sqlite3.connect('data.db')
    conn.execute("""
                create table if not exists datatest(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                stickiness int DEFAULT NULL,
                like int DEFAULT NULL)""")
    conn.commit()
    dataout() #获取表项
    command1 = "insert into datatest \
             (mid,stickiness,like) values (?,?,?);"
    for i in data: #i为每一项的键值，(id,mid,view,readnum,like,follow)
        temporary = []
        stickiness = int((i[2]+i[3])/i[5]) #stickiness
        like = int(i[4]/i[5])
        temporary.append(i[1])
        temporary.append(int(math.sqrt(stickiness)))
        temporary.append(like)
        try:
            conn.execute(command1, temporary)
            conn.commit()
        except Exception as e:
            print(e)
            print("insert error!")
            conn.rollback()
    return 0

def makedatabase2():
    '''
    此方法为演示使用的适用方法
    1.处理数据，数据主要为：关注数，点赞数，阅读量+播放量
    **主要目的：将数据处理为二维坐标的形式，为后续AGNES算法做准备，关注*（点赞/播放）;（点赞/稿件）*关注
    2.数据入库，方便下次选用
    数据库分为三个选项，分别是主键up的mid，用户黏度，与喜爱程度,取整
    '''
    global data
    conn = sqlite3.connect('data.db')
    conn.execute("""
                create table if not exists datatest(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                stickiness int DEFAULT NULL,
                like int DEFAULT NULL)""")
    conn.commit()
    testdata2out() #获取表项
    command1 = "insert into datatest2 \
             (mid,stickiness,like) values (?,?,?);"
    for i in data: #i为每一项的键值，(id,mid,view,readnum,like,follow，video)
        temporary = []
        stickiness = int((i[4]/(i[3]+i[2]))*i[5]) #stickiness
        like = int(i[5]*(i[4]/i[6]))
        temporary.append(i[1])
        temporary.append(math.pow(stickiness,0.25))
        temporary.append(math.pow(like,0.25))
        try:
            conn.execute(command1, temporary)
            conn.commit()
        except Exception as e:
            print(e)
            print("insert error!")
            conn.rollback()
    return 0

def AGNESmake():
    conn = sqlite3.connect('data.db')    #连接数据库 
    data = conn.execute("select stickiness,like from datatest3").fetchall() #返回现在已有的全部数据
    print(data)
    C = AGNES.AGNES(data,AGNES.dist_avg,4)
    print(C)
    AGNES.draw(C)
    return



#############################################################################################
def create_AGNES():
    '''
    此函数用来存放AGNES聚完类后的数据存放，方便读取使用
    '''
    conn = sqlite3.connect('data.db')
    conn.execute("""
                create table if not exists datausing(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                group int DEFAULT NULL)""")
    conn.commit()   
    return         

def AGNESmake_last():
    '''
    聚类算法
    '''
    global D
    conn = sqlite3.connect('data.db')    #连接数据库 
    data = conn.execute("select stickiness,like from ADGNE_last").fetchall() #返回现在已有的全部数据
    print(data)
    E = AGNES.AGNES(data,AGNES.dist_avg,4)
    print("start!")
    D = sorted(E,key = lambda b : b[0][1],reverse=True)
    print("done!")
    #AGNES.draw(C)
    return

def ADGNEdataout():
    '''
    此函数用于导出相关数据，输入up主的mid，导出关注，阅读等信息,返回元组数据
    '''
    global last_data
    conn = sqlite3.connect('data.db')    #连接数据库 
    last_data = conn.execute("select * from lastdatabase").fetchall() #返回现在已有的全部数据
    #print(data)
    return 0

def ADGNE_last_make():
    '''
    运行算法计算必要数据，生成数据库ADGNE_last
    '''
    '''
    此方法为演示使用的适用方法
    1.处理数据，数据主要为：关注数，点赞数，阅读量+播放量
    **主要目的：将数据处理为二维坐标的形式，为后续AGNES算法做准备，关注*（点赞/播放）;（点赞/稿件）*关注
    2.数据入库，方便下次选用
    数据库分为三个选项，分别是主键up的mid，用户黏度，与喜爱程度,取整
    '''
    global last_data
    conn = sqlite3.connect('data.db')
    conn.execute("""
                create table if not exists ADGNE_last(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                stickiness int DEFAULT NULL,
                like int DEFAULT NULL)""")
    conn.commit()
    ADGNEdataout() #获取表项
    command1 = "insert into ADGNE_last \
             (mid,stickiness,like) values (?,?,?);"
    for i in last_data: #i为每一项的键值，(id,mid,view,readnum,like,follow，video)
        temporary = []
        i_2 = int(i[2])+1 #防止垃圾up主的出现，出现0的情况
        i_3 = int(i[3])+1
        i_4 = int(i[4])+1
        i_5 = int(i[5])+1
        i_6 = int(i[6])+1
        stickiness = int((i_4/(i_3+i_2))*i_5) #stickiness
        like = int(i_5*(i_4/i_6))
        temporary.append(i[1])
        temporary.append(math.pow(stickiness,0.25))
        temporary.append(math.pow(like,0.25))
        try:
            conn.execute(command1, temporary)
            conn.commit()
        except Exception as e:
            print(e)
            print("insert error!")
            conn.rollback()
    return 0

def data_using_database_make():
    '''
    创建聚类后的数据库表，方便无参考推荐选用
    '''
    global D
    conn = sqlite3.connect('data.db')
    create_AGNES()#创建数据库
    command1 = "insert into datausing \
             (mid,group) values (?,?);" #存入数据库
    H = sorted(D,key = lambda b : b[0][1],reverse=True) #为处理完的数组进行降序排列 第一组定义为0
    for i in range(0,4):
        for j in H[i]:  #j为一个列表
            for x in j: #x为一个点阵
                mid = x[0]
                group = i
                list_data = []
                list_data.append(mid)
                list_data.append(group)
                try:
                    conn.execute(command1, list_data)
                    conn.commit()
                except Exception as e:
                    print(e)
                    print("insert error!")
                    conn.rollback() 
    return 0

if __name__ == "__main__":
    #ADGNE_last_make()\
    AGNESmake_last()
    data_using_database_make()