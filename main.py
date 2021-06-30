import sqlite3
import requests
import time
import bilbliapi
import AGNES
import math
import useraner
import using


def useraner_data_F(mid):
    '''
    项协同的推荐算法,主要入口
    '''
    for i in mid:
        useraner.take_database(i)

def using_data_F(mid):
    '''
    用户协同的推荐算法,程序入口
    '''
    using.using_database(mid)
    

def using_agnes_data():
    '''
    基于聚类算法的推荐入口
    算法流程：
    1.查找数据库，查找出全部一类up主
    2.根据mid查找up主相关信息，输出up主相关信息
    '''
    conn = sqlite3.connect('data.db')
    data = conn.execute("SELECT user.mid,user.name,user.desc from user,datausing1 WHERE datausing1.group_num == 1 and datausing1.mid = user.mid GROUP BY user.mid").fetchall()
    tplt = "{0:{3}^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("up主mid", "up主id", "up获得头衔", chr(12288)))
    for i in data:
        print(tplt.format(i[0], i[1], i[2], chr(12288)))
    return

def initialization(uid): #推荐uid
    '''
    初始化函数主要为后续两种算法处理数据
    '''
    
    A = bilbliapi.followings(uid)
    O = ['63231', '116683', '122879', '208259', '375375', '466272', '546195', '562197', '730732', '777536', '883968', '1420982', '1532165', '1577804', '2200736', '2206456', '2374194', '2920960', '3345720', '3353026', '4162287', '4474705', '5294454', '5870268', '5970160', '6574487', '7788379', '8047632', '9008159', '9617619', '9824766', '10558098', 
'11688464', '13354765', '14110780', '14583962', '14804670', '17409016', '18202105', '19577966', '20165629', '26366366', '27756469', '29329085', '32786875', '35789774', '37090048', '37663924', '44688866', '51896064', '62540916', 
'67141499', '89847338', '90361813', '99157282', '113362335', '161775300', '163637592', '174501086', '176037767', '196356191', '212535360', '233114659', '250858633', '254463269', '280793434', '290526283', '319341196', '321173469', '326499679', '339680732', '353539995', '393166851', '401742377', '414336759', '419738808', '437316738', '455876411', '456664753', '472747194', '474702359', '517327498', '519872016', '587618113', '591856754', '598464467', '605544858', '641591444', '642389251', '1202762767', '1868902080', '2026561407']
    up_mid = []
    for i in A:
        up_mid.append(i[0])
    useraner_data = [] #项协同
    using_data = [] #用户协同
    for i in up_mid:
        if any(i in j for j in O):
            using_data.append(i)
        else:
            useraner_data.append(i)
    useraner_data_F(useraner_data)
    using_data_F(using_data)
2

def muen():
    '''
    主菜单界面，模式选择等功能
    '''
    while True:
        print("欢迎来的到bilibili推荐热门up系统 ----by ljzjsc")
        print("本程序提供两种推荐方式，一种是基于聚类算法的up热门推荐，适用于新来b站的朋友")
        print("一种是基于用户协同的推荐方式")
        print("1.聚类算法推荐")
        print("2.用户协同算法推荐")
        num = input("请输入你的选择：")
        if(int(num) == 1):
            using_agnes_data()
        elif(int(num) == 2):
            uid = input("请输入uid：")
            initialization(uid)
            #print("2")
        else:
            continue

if __name__ == "__main__":
    #initialization(1384117815)
    #muen()
    '''
    P = []
    conn = sqlite3.connect('data.db')
    command1 = "SELECT datausing1.mid from datausing1 where datausing1.group_num ==1 GROUP BY datausing1.mid"
    up = conn.execute(command1).fetchall()
    for i in up:
        P.append(i[0])
    print(P)'''
    muen()
