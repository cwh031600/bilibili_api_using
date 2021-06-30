import requests
import urllib
from urllib import request
import urllib.parse
import urllib.request
import re
import sys
import json
import urllib as UrlUtils
from bs4 import BeautifulSoup 


def requests_GET(url,head): #GET请求封装模块
    join_in = requests.get(url,headers=head)
    #return_json = join_in.json()
    return join_in

def get_AV_data():
    '''
    获取指定信息，API直接使用
    '''
	# 请求头
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Host": "api.bilibili.com",
        "Referer": "https://www.bilibili.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }
	# 刚刚获取的api
    api_url = "https://api.bilibili.com/x/web-interface/online"
	# 开始请求
    res = requests.get(api_url, headers=headers)
    online_dic = res.json()
    print(online_dic)
    #print("最新投稿:%d" % online_dic['data']['all_count'])
    #print("在线人数:%d" % online_dic['data']['web_online'])

def followings(id):
    '''
    爬取关注up主，返回列表 0.up主uid 1.up主名字 2.up主简介 3.bilibili官方认证
    '''
    #global user
    #if id == 0:
    #    return
    following_up = []
    i = 0
    result = []
    ref_url = "https://space.bilibili.com/"+str(id)+"/#/fans/follow"
    head = {
        'Accept': '*/*',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'api.bilibili.com',
        'Pragma': 'no-cache',
        'Referer': ref_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    while 1:
        i += 1
        if i >= 6:
            break
        url = "https://api.bilibili.com/x/relation/followings?vmid=" + \
            str(id)+"&pn="+str(i) + \
            "&ps=20&order=desc&jsonp=jsonp&callback=__jp5"
        try:
            '''
            爬取关注up主信息，并正则表达式提取关键信息
            '''
            r = requests.get(url, headers=head, timeout=10)
            #r.encoding='utf-8'
            a = r.content
            r2=str(a,'utf-8')
            print("获取返回数据如下：")
            print(r2)
            #print(type(r2))
            #my_mid = re.split('mid', r2)
            pattern_mid = '"mid":(.*?),"'
            pattern_uname = '"uname":"(.*?)"'
            pattern_sign = '"sign":"(.*?)"'
            pattern_desc = '"desc":"(.*?)"'
            #my_mid = re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{4})',s)
            up_mid = re.findall(pattern_mid,r2)   #up主唯一标识
            up_uname = re.findall(pattern_uname,r2) #up主名字
            up_sign = re.findall(pattern_sign,r2) #up主简介
            up_desc = re.findall(pattern_desc,r2) #up主名牌
            #print(up_mid)
            #print(up_uname)
            #print(up_sign)
            #print(up_desc)
            '''
            处理每轮产生结果，生成字典，每一项存放一个up主
            '''  
            for H in range(0,len(up_mid)):
                up_list = []
                up_list.append(up_mid[H])
                up_list.append(up_uname[H])
                up_list.append(up_sign[H])
                up_list.append(up_desc[H])
                following_up.append(up_list)
        except Exception as e:
            print(e)
    if following_up != []:
        return following_up
        #save(result, id)
    None1 = []
    return None1

def like(id):
    '''
    查询up主的相关信息，关注数，粉丝数，播放数
    '''
    up_list = []
    ref_url = "https://space.bilibili.com/"+str(id)+"/"
    head = {
        'Accept': '*/*',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'api.bilibili.com',
        'Pragma': 'no-cache',
        'Origin': 'https://space.bilibili.com',
        'Referer': ref_url,
        'Cookie': '_uuid=95E34708-B13F-06BD-F15D-B9A7889F566A81055infoc; buvid3=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; sid=ctkdkd9j; fingerprint=86389dc6f0cfbcc788570e854adb58d7; buvid_fp=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; buvid_fp_plain=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; SESSDATA=2ff764bb%2C1634227219%2Ccbd32%2A41; bili_jct=71474888bc861e2b812f5b1c37be43af; DedeUserID=9212842; DedeUserID__ckMd5=9b3f2f28b80496cc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kYJR|~Yu||0J\'uYu)Y~Ylu); bp_video_offset_9212842=538707551688239083; bp_t_offset_9212842=538578260294428027; PVID=1; LIVE_BUVID=AUTO9216189331965043; CURRENT_QUALITY=120; fingerprint3=92ba3966bc055af7f2017403217146b5; fingerprint_s=d0253cd16b7410177c9b7f2f6cd1dcc6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    url = "https://api.bilibili.com/x/space/upstat?mid=" + str(id) + "&jsonp=jsonp"
    r = requests.get(url, headers=head, timeout=10)
    #r.encoding='utf-8'
    a = r.content
    r2=str(a,'utf-8')
    pattern_view = '"view":(.*?)},"article'
    pattern_readnum = '"view":(.*?),"l'
    pattern_like = '"likes":(.*?)}'
    pattern_readnum2 = '"view":(.*?)}'
    #print(r2)
    up_view = re.findall(pattern_view,r2)   #up播放量
    up_readnum = re.findall(pattern_readnum,r2) #up阅读量
    up_like = re.findall(pattern_like,r2) #up获赞数
    print(up_readnum[0])
    up_readnum2 = re.findall(pattern_readnum2,up_readnum[0])
    up_list.append(up_view[0])            #up播放量   
    up_list.append(up_readnum2[0])          #up阅读量
    up_list.append(up_like[0])             #up获赞数
    print(up_list)
    return up_list

def followingnum(id):
    '''
    获取up主粉丝数量
    '''
    ref_url = "https://space.bilibili.com/"+str(id)+"/dynamic"
    head = {
        'Accept': '*/*',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'api.bilibili.com',
        'Pragma': 'no-cache',
        'Origin': 'https://space.bilibili.com',
        'Referer': ref_url,
        #'Cookie': '_uuid=95E34708-B13F-06BD-F15D-B9A7889F566A81055infoc; buvid3=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; sid=ctkdkd9j; fingerprint=86389dc6f0cfbcc788570e854adb58d7; buvid_fp=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; buvid_fp_plain=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; SESSDATA=2ff764bb%2C1634227219%2Ccbd32%2A41; bili_jct=71474888bc861e2b812f5b1c37be43af; DedeUserID=9212842; DedeUserID__ckMd5=9b3f2f28b80496cc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kYJR|~Yu||0J\'uYu)Y~Ylu); bp_video_offset_9212842=538707551688239083; bp_t_offset_9212842=538578260294428027; PVID=1; LIVE_BUVID=AUTO9216189331965043; CURRENT_QUALITY=120; fingerprint3=92ba3966bc055af7f2017403217146b5; fingerprint_s=d0253cd16b7410177c9b7f2f6cd1dcc6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    url = "https://api.bilibili.com/x/relation/stat?vmid=" + str(id) + "&jsonp=jsonp"
    r = requests.get(url, headers=head, timeout=10)
    #r.encoding='utf-8'
    a = r.content
    r2=str(a,'utf-8')
    print(r2)
    pattern_followingnum1 = '"follower":(.*?)}'
    up_followingnum = re.findall(pattern_followingnum1,r2) #up获赞数
    print(up_followingnum)
    return up_followingnum[0]



def video(id):
    '''
    本函数用于抓取up主的视频的投稿数，由于投稿数在html中，所以与之前还是有一点区别的
    '''
    ref_url = "https://space.bilibili.com/"+str(id)
    head = {
        'Accept': '*/*',
        #'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'api.bilibili.com',
        'Pragma': 'no-cache',
        'Origin': 'https://space.bilibili.com',
        'Referer': ref_url,
        #'Cookie': '_uuid=95E34708-B13F-06BD-F15D-B9A7889F566A81055infoc; buvid3=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; sid=ctkdkd9j; fingerprint=86389dc6f0cfbcc788570e854adb58d7; buvid_fp=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; buvid_fp_plain=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; SESSDATA=2ff764bb%2C1634227219%2Ccbd32%2A41; bili_jct=71474888bc861e2b812f5b1c37be43af; DedeUserID=9212842; DedeUserID__ckMd5=9b3f2f28b80496cc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kYJR|~Yu||0J\'uYu)Y~Ylu); bp_video_offset_9212842=538707551688239083; bp_t_offset_9212842=538578260294428027; PVID=1; LIVE_BUVID=AUTO9216189331965043; CURRENT_QUALITY=120; fingerprint3=92ba3966bc055af7f2017403217146b5; fingerprint_s=d0253cd16b7410177c9b7f2f6cd1dcc6',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    url = "https://api.bilibili.com/x/space/navnum?mid="+str(id) + "&jsonp=jsonp&callback=__jp5"
    r = requests.get(url, headers=head, timeout=10)
    #r.encoding='utf-8'
    a = r.content
    r2=str(a,'utf-8')
    print(r2)
    pattern_followingnum1 = '"video":(.*?),"'
    up_followingnum = re.findall(pattern_followingnum1,r2) #up获赞数
    print(up_followingnum)
    return up_followingnum[0]



if __name__ == '__main__':
    #get_api()
    #print(followings(9212842))
    #like(394620890)
    #followingnum(394620890)
    video(448039667)

'''
GET /x/space/upstat?mid=394620890&jsonp=jsonp HTTP/2
Host: api.bilibili.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: https://space.bilibili.com/394620890/
Origin: https://space.bilibili.com
Connection: keep-alive
Cookie: _uuid=95E34708-B13F-06BD-F15D-B9A7889F566A81055infoc; buvid3=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; sid=ctkdkd9j; fingerprint=86389dc6f0cfbcc788570e854adb58d7; buvid_fp=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; buvid_fp_plain=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; SESSDATA=2ff764bb%2C1634227219%2Ccbd32%2A41; bili_jct=71474888bc861e2b812f5b1c37be43af; DedeUserID=9212842; DedeUserID__ckMd5=9b3f2f28b80496cc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kYJR|~Yu||0J'uYu)Y~Ylu); bp_video_offset_9212842=538707551688239083; bp_t_offset_9212842=538578260294428027; PVID=2; LIVE_BUVID=AUTO9216189331965043; CURRENT_QUALITY=120; fingerprint3=92ba3966bc055af7f2017403217146b5; fingerprint_s=d0253cd16b7410177c9b7f2f6cd1dcc6; bfe_id=1e33d9ad1cb29251013800c68af42315
Cache-Control: max-age=0
TE: Trailers
'''

'''
GET /x/relation/stat?vmid=429392011&jsonp=jsonp HTTP/2
Host: api.bilibili.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: https://space.bilibili.com/429392011/dynamic
Origin: https://space.bilibili.com
Connection: keep-alive
Cookie: _uuid=95E34708-B13F-06BD-F15D-B9A7889F566A81055infoc; buvid3=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; sid=ctkdkd9j; fingerprint=86389dc6f0cfbcc788570e854adb58d7; buvid_fp=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; buvid_fp_plain=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; SESSDATA=2ff764bb%2C1634227219%2Ccbd32%2A41; bili_jct=71474888bc861e2b812f5b1c37be43af; DedeUserID=9212842; DedeUserID__ckMd5=9b3f2f28b80496cc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kYJR|~Yu||0J'uYu)Y~Ylu); bp_video_offset_9212842=538707551688239083; bp_t_offset_9212842=538578260294428027; PVID=2; LIVE_BUVID=AUTO9216189331965043; CURRENT_QUALITY=120; fingerprint3=92ba3966bc055af7f2017403217146b5; fingerprint_s=d0253cd16b7410177c9b7f2f6cd1dcc6; bfe_id=fdfaf33a01b88dd4692ca80f00c2de7f
TE: Trailers
'''

'''
GET /x/space/navnum?mid=448039667&jsonp=jsonp&callback=__jp5 HTTP/2
Host: api.bilibili.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: https://space.bilibili.com/448039667
Connection: keep-alive
Cookie: _uuid=95E34708-B13F-06BD-F15D-B9A7889F566A81055infoc; buvid3=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; sid=ctkdkd9j; fingerprint=0848256832ca1f810ae25aa908e3fb89; buvid_fp=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; buvid_fp_plain=E0740887-CFFD-4C3B-879A-604FDDF8AC8B13426infoc; SESSDATA=2ff764bb%2C1634227219%2Ccbd32%2A41; bili_jct=71474888bc861e2b812f5b1c37be43af; DedeUserID=9212842; DedeUserID__ckMd5=9b3f2f28b80496cc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(kYJR|~Yu||0J'uYu)Y~Ylu); bp_video_offset_9212842=539900599119579057; bp_t_offset_9212842=539904709395983064; PVID=1; LIVE_BUVID=AUTO9216189331965043; CURRENT_QUALITY=120; fingerprint3=a466fad6a277e5aefdd8acbf3afe241e; fingerprint_s=9a586d2148e03458e70a8f8abad36520; bfe_id=fdfaf33a01b88dd4692ca80f00c2de7f
TE: Trailers
'''