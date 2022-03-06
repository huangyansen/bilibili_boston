# 生成txt文件 

import requests 
from bs4 import BeautifulSoup
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0", "Cookie": "_uuid=827B8494-A44C-31D0-9BD4-DFF80A5E0FEE82120infoc; buvid3=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; sid=adec7tca; bp_video_offset_398722478=497617492191521518; PVID=2; CURRENT_FNVAL=80; rpdid=|(um~kmlu|lR0J'ulmlY~~uJY; LIVE_BUVID=AUTO6815959410724974; CURRENT_QUALITY=80; blackside_state=1; fingerprint3=9705c866e2e5e695c6e38746c7a602b7; fingerprint=3ed5802aad09c12021d5aec79dff4604; fingerprint_s=ad649c5d9fd6fcfeb770fa2baf91990b; buivd_fp=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; buvid_fp_plain=6D98D0E6-B61B-4EF6-8419-5ACD0EF3710E95147infoc; buvid_fp=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; DedeUserID=398722478; DedeUserID__ckMd5=a7040f6f6a474e19; SESSDATA=49f91206%2C1626876204%2Cd3b97*11; bili_jct=ebc530ed75291ef66baf035af911fab7; bp_t_offset_398722478=489028433772728540"} 
comments = [] 
original_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=48624233&sort=0&pn="  
for page in range(1, 3): # 页码这里简单处理  258       oid为视频号 sort为0时按时间排序 为1时按热度排序 pn为页数
    url = original_url + str(page) 
    #print(url) 
    html = requests.get(url, headers=header) 
    data = html.json() 
    if data['data']['replies']: 
        for i in data['data']['replies']: 
#            comments.append(i['content']['message']) 
            with open('F:\\bili\\out\\bili.txt','a',encoding='utf-8') as fp:
                fp.write(i['member']['uname']+'\n') #用户名
                fp.write(i['content']['message']+'\n') #评论
                fp.write(str(i['like'])+'\n') #点赞数
                fp.write('\n')
     
           
'''
#评论数据是用动态js展示的，因此不能直接爬取                
import requests 
from bs4 import BeautifulSoup
import os

comments = [] 
original_url = "https://www.bilibili.com/video/BV1Av41167m6?p="  
fh=open('F:\\test.txt','w',encoding='utf-8')
for page in range(1, 3): # 页码这里简单处理         oid为视频号 sort为0时按时间排序 为1时按热度排序 pn为页数
    url = original_url + str(page) 
    urlhtml=requests.get(url)
    urlhtml.encoding='utf-8'
    soup=BeautifulSoup(urlhtml.text,'lxml')
    #print(url) 
    comment_list = soup.find_all('div',attrs = {'class': 'con'})
    print (comment_list)
    for comment in comment_list:
        #fh.write()
        print (comment)
'''     