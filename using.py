import sqlite3
import requests
import time
import bilbliapi
import AGNES
import math


'''
此python文件是基于用户协同的推荐算法
'''

def using_database(id):
    '''
    用户协同主要针对1类up主，原因是大up主用户粘合度高，产出稳定，视频种类更加固定且丰富，适合用户协同
    算法流程：
    1.得到一个用户所关注的全部1类up主列表，根据up主mid查找所有关注的用户，进行统计
    2.计算相关度，相关度保持在50%以上，得出几个最高的用户，查找其关注的1类up主
    3.导出，对比输入，得到推荐列表结论
    '''
    conn = sqlite3.connect('data.db')
    user = {}
    for i in id:
        command1 = "SELECT relation.master from relation where relation.following =" + str(i) + " GROUP BY relation.master" #步骤一 通过up主反向查找数据库中关注了人数
        master_id = conn.execute(command1).fetchall()
        for i in master_id: #遍历对象
            if i[0] in user:
                user[i[0]] = user[i[0]] + 1
            else:
                user[i[0]] = 1
    user1 = sorted(user.items(), key = lambda kv:(kv[1], kv[0]))
    print("已经成功匹配数据库中所用用户，结果如下（mid，关注相同个数）：")
    print(user1)
    command2 = "SELECT user.mid,user.name,user.desc from user where user.mid in (SELECT relation.following FROM relation where relation.master == "+ str(user1[-1][0]) +" and EXISTS(SELECT datausing1.mid from datausing1 where datausing1.group_num ==1 and datausing1.mid = relation.following)) GROUP BY user.mid"
    up_data = conn.execute(command2).fetchall()
    tplt = "{0:{3}^10}\t{1:{3}^10}\t{2:^10}"
    print("使用基于用户协同算法匹配与您最接近的用户是：" + str(user1[-1][0]) + "根据该用户为您做如下推荐")
    print(tplt.format("up主mid", "up主id", "up获得头衔", chr(12288)))
    for i in up_data:
        if i[0] not in id: 
            print(tplt.format(i[0], i[1], i[2], chr(12288)))

if __name__ == "__main__":
    '''
    主函数
    '''
    id =[14583962,641591444,254463269,7788379,1868902080,401742377]
    using_database(id)
    