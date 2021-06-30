import sqlite3
import requests
import time
import bilbliapi

user = [] #保证收录的up信息只出现一次

def create():
    '''
    创建数据库
    id 主键值用户唯一id
    mid 关注up的id
    uname up主的名字
    sign up主的简介
    desc up主的官方认证
    '''
    global conn
    conn = sqlite3.connect('data.db')
    print("Opened database successfully")
    conn.execute("""
                create table if not exists user(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                name varchar DEFAULT NULL,
                sign varchar DEFAULT NULL,
                desc varchar DEFAULT NULL)""")
    conn.execute("""
                create table if not exists relation(
                id INTEGER PRIMARY KEY ,
                master int,
                following int 
                )""")
    conn.commit()

    print("Table created successfully")
    conn.commit()

def save(id,result):
    '''
    添加数据进入数据库
    '''
    # 将数据保存至本地
    global conn
    command1 = "insert into user \
             (mid,name,sign,desc) values (?,?,?,?);"
    command2 = "insert into relation\
             (master,following)values(?,?)"
    if result == []:
        return
    for row in result:
        try:
            temp = (id, row[0])
            if row[0] not in user:
                user.append(row[0])
                conn.execute(command1, row)
                conn.execute(command2, temp)
            else:
                conn.execute(command2, temp)
        except Exception as e:
            print(e)
            print("insert error!")
            conn.rollback()
    conn.commit()
    return 

def use_database():
    '''
    使用爬虫信息备用，创建数据库
    9208637
    9150264
    '''
    num = 100000
    now_num = 9208637
    create()
    for i in range(0,num):
        uid = now_num - i
        data = bilbliapi.followings(uid)
        if data != []:    
            save(uid ,data)
        print("\r已爬取uid为{0}的用户".format(uid))
    conn.close()

def create_analyze_data():
    '''
    创建分析数据
    id 主键值用户唯一id
    mid 关注up的id
    view up主的总播放数
    readnum up主的总阅读数
    like up主的获赞数
    following up主的关注数
    '''
    global conn
    conn = sqlite3.connect('data.db')
    print("Opened database successfully")
    conn.execute("""
                create table if not exists data(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                view int DEFAULT NULL,
                readnum int DEFAULT NULL,
                like int DEFAULT NULL,
                following int DEFAULT NULL)""")
    conn.commit()
    print("Table created successfully")
    conn.commit()

def user_database_analyzedata():
    '''
    获取up数据库，并且新建表项
    '''
    conn = sqlite3.connect('data.db')
    create_analyze_data()
    #user = {}
    command1 = "insert into data \
             (view,readnum,like,following,mid) values (?,?,?,?,?);"
    for i in conn.execute("select mid,name from user where not EXISTS (select mid from data where user.mid == data.mid) order by id").fetchall():
        '''
        在user表中查询mid和name
        '''
        try:
            #up=[i[0]]
            up = bilbliapi.like(i[0])
            followingnum = bilbliapi.followingnum(i[0])
            up.append(followingnum)
            up.append(i[0])
            print(up)
            conn.execute(command1, up)
            conn.commit()
            time.sleep(1)
        except Exception as e:
            print(e)
            print("insert error!")
            conn.rollback()
    conn.commit()
    return
        #user[i[0]] = i[1]
    #print(len(user))

def create_test_data():
    '''
    创建分析数据
    id 主键值用户唯一id
    mid 关注up的id
    view up主的总播放数
    readnum up主的总阅读数
    like up主的获赞数
    following up主的关注数
    '''
    global conn
    conn = sqlite3.connect('data.db')
    print("Opened database successfully")
    conn.execute("""
                create table if not exists testdata3(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                view int DEFAULT NULL,
                readnum int DEFAULT NULL,
                like int DEFAULT NULL,
                following int DEFAULT NULL,
                video int DEFAULT NULL)""")
    conn.commit()
    print("Table created successfully")
    conn.commit()



def user_database_analyzetestdata(id):
    '''
    获取up数据库，并且新建表项
    '''
    conn = sqlite3.connect('data.db')
    create_test_data()
    #user = {}
    command1 = "insert into testdata3 \
             (view,readnum,like,following,video,mid) values (?,?,?,?,?,?);"
    #for i in conn.execute("select mid,name from user where not EXISTS (select mid from data where user.mid == data.mid) order by id").fetchall():
    '''
    在user表中查询mid和name
    '''
    try:
        #up=[i[0]]
        up = bilbliapi.like(id)
        followingnum = bilbliapi.followingnum(id)
        video  = bilbliapi.video(id)
        up.append(followingnum)
        up.append(video)
        up.append(id)
        print(up)
        conn.execute(command1, up)
        conn.commit()
        time.sleep(1)
    except Exception as e:
        print(e)
        print("insert error!")
        conn.rollback()
    conn.commit()
    return

def create_last_data(): #最终总表数据
    '''
    创建分析数据
    id 主键值用户唯一id
    mid 关注up的id
    view up主的总播放数
    readnum up主的总阅读数
    like up主的获赞数
    following up主的关注数
    '''
    global conn
    conn = sqlite3.connect('data.db')
    print("Opened database successfully")
    conn.execute("""
                create table if not exists lastdatabase(
                id INTEGER PRIMARY KEY ,
                mid int DEFAULT NULL,
                view int DEFAULT NULL,
                readnum int DEFAULT NULL,
                like int DEFAULT NULL,
                following int DEFAULT NULL,
                video int DEFAULT NULL)""")
    conn.commit()
    print("Table created successfully")
    conn.commit()

def user_database_analyzetestdata(id): #最后汇总函数
    '''
    获取up数据库，并且新建表项
    '''
    conn = sqlite3.connect('data.db')
    
    #user = {}
    command1 = "insert into lastdatabase \
             (view,readnum,like,following,video,mid) values (?,?,?,?,?,?);"
    #for i in conn.execute("select mid,name from user where not EXISTS (select mid from data where user.mid == data.mid) order by id").fetchall():
    '''
    在user表中查询mid和name
    '''
    try:
        #up=[i[0]]
        up = bilbliapi.like(id)
        followingnum = bilbliapi.followingnum(id)
        video  = bilbliapi.video(id)
        up.append(followingnum)
        up.append(video)
        up.append(id)
        print(up)
        conn.execute(command1, up)
        conn.commit()
        time.sleep(1)
    except Exception as e:
        print(e)
        print("insert error!")
        conn.rollback()
    conn.commit()
    return

def lastmakedata():
    '''
    进行提取up主的mid，加入断点续写能力
    '''
    conn = sqlite3.connect('data.db')
    create_last_data()
    for i in conn.execute("select mid,name from user where not EXISTS (select mid from lastdatabase where user.mid == lastdatabase.mid) order by id").fetchall():
        up = i[0]
        user_database_analyzetestdata(up)




if __name__ == "__main__":
    #use_database()
    '''
    1.怕上火暴王老菊 渗透之C君 泠鸢yousa 老番茄 上海滩许Van强 敖厂长 逗比的雀巢 中国BOY超级大猩猩 神奇的老皮VFX 凉风Kaze 木鱼水心
    2.正点原子 宋浩老师官方 一只大哈鱼 空耳狂魔 
    3.周扒片 -LKs- 观察者网 沈逸老师 米梦杰 怒九笑 Warma 夏布去 Crazy_Bucket
    4.牢记自己是菜 fe1w0
    '''
    
    '''
    聚类后的结果1
    1.老番茄 凉风Kaze 逗比的雀巢 敖厂长 渗透之C君
    2.-LKs- 观察者网 沈逸老师 怒九笑 Warma Crazy_Bucket 空耳狂魔 一只大哈鱼 宋浩老师官方 怕上火暴王老菊 泠鸢yousa 上海滩许Van强 中国BOY超级大猩猩 木鱼水心
    3.米梦杰 周扒片 夏布去
    4.正点原子官方 牢记自己是菜 fe1w0
    '''
    '''
    聚类后的结果2
    1.老番茄 凉风Kaze
    2.观察者网 逗比的雀巢 敖厂长 渗透之C君 沈逸老师 泠鸢yousa 上海滩许Van强 中国BOY超级大猩猩 木鱼水心 Warma
    3.米梦杰 周扒片 夏布去 怕上火暴王老菊 怒九笑 Crazy_Bucket -LKs- 一只大哈鱼 宋浩老师官方 空耳狂魔
    4.正点原子官方 牢记自己是菜 fe1w0
    '''
    '''
    #测试使用数据集
    A =[10330740,394620890,454958604,66607740,23604445,53456,353902138,3127528,14751040,1985025,66606350,301717426,5294454,624757844,648113003,125526,423895,4162287,927587,282994,546195,3380239,14110780,122879,562197]
    B = [9212842]
    for i in B:
        user_database_analyzetestdata(i)
    '''
    lastmakedata()