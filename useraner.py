import sqlite3
import requests
import time
import bilbliapi
import AGNES
import math

'''
此python文件是基于项协同的推荐算法
'''

def take_database(id): #up主mid
    '''
    提取数据库数据,主要用于2类up主的推荐，原因是第2，3，4类up主的画像相对比较固定，接受人群比较单一  
    算法流程：
    1.搜索当期up主在数据库中被关注的人员，生成列表list1
    2.根据list1中的mid正向搜索up主，进行up主数目统计，选取除第一个剩余的up主,计算比率
    3.比率大于30%即可将up主推荐给用户，否则返回当前数据库项目不匹配
    '''
    conn = sqlite3.connect('data.db')
    command1 = "SELECT relation.master from relation where relation.following =" + str(id) + " GROUP BY relation.master" #算法步骤一，正向查找人群
    master_id = conn.execute(command1).fetchall()
    #print(master_id)
    up = {}
    sum = len(master_id)*0.60
    for i in master_id: #遍历对象
        command2 = "SELECT relation.following from relation WHERE relation.master = " +str(i[0])+" and not EXISTS(SELECT datausing1.mid from datausing1 where datausing1.group_num ==1 and datausing1.mid = relation.following) GROUP BY relation.following"
        up_id = conn.execute(command2).fetchall()
        for j in up_id:
            if j[0] in up:
                up[j[0]] = up[j[0]] + 1 
            else:
                up[j[0]] = 1
    #list_num = []
    flag = 1
    for key,value in up.items():
        if value > sum:
            #list_num.append(key)
    #print(list_num)
            if key != id:
                command3 = "SELECT user.mid,user.name,user.desc from user WHERE user.mid == " + str(key) +" GROUP BY user.mid" #查询相关up主信息
                up_text = conn.execute(command3).fetchall()
                tplt = "{0:{3}^10}\t{1:{3}^10}\t{2:^10}"
                print("使用基于项协同算法根据up主：" + str(id) + "为您推荐")
                print(tplt.format("up主mid", "up主id", "up获得头衔", chr(12288)))
                print(tplt.format(up_text[0][0], up_text[0][1], up_text[0][2], chr(12288)))
                flag = 0
    if flag:
        print("由于数据库不足，根据up主：" + str(id) + "无法为您生成有效推荐")

if __name__ == "__main__":
    #test 2040144589 11534088 295788293 507102012 17561219 359328879
    #take_database(22017969)
    conn = sqlite3.connect('data.db')
    command1 = "SELECT datausing1.mid from datausing1 where datausing1.group_num !=1" #算法步骤一，正向查找人群
    up = conn.execute(command1).fetchall()
    for i in up:
        take_database(i[0])