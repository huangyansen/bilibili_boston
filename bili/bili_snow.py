# 生成表格文件
import requests
import pandas as pd
from snownlp import SnowNLP
#from bs4 import BeautifulSoup
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0", "Cookie": "_uuid=827B8494-A44C-31D0-9BD4-DFF80A5E0FEE82120infoc; buvid3=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; sid=adec7tca; bp_video_offset_398722478=497617492191521518; PVID=2; CURRENT_FNVAL=80; rpdid=|(um~kmlu|lR0J'ulmlY~~uJY; LIVE_BUVID=AUTO6815959410724974; CURRENT_QUALITY=80; blackside_state=1; fingerprint3=9705c866e2e5e695c6e38746c7a602b7; fingerprint=3ed5802aad09c12021d5aec79dff4604; fingerprint_s=ad649c5d9fd6fcfeb770fa2baf91990b; buivd_fp=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; buvid_fp_plain=6D98D0E6-B61B-4EF6-8419-5ACD0EF3710E95147infoc; buvid_fp=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; DedeUserID=398722478; DedeUserID__ckMd5=a7040f6f6a474e19; SESSDATA=49f91206%2C1626876204%2Cd3b97*11; bili_jct=ebc530ed75291ef66baf035af911fab7; bp_t_offset_398722478=489028433772728540"} 
comments,users,likes,rates = [],[],[],[]
original_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=48624233&sort=0&pn="
for page in range(1,258): #可以修改评论页数 最大258  oid为视频号 sort为0时按时间排序 为1时按热度排序 pn为页数
    url = original_url + str(page)
    print(url)
    html = requests.get(url, headers=headers)
    data = html.json()
    if data['data']['replies']:
        for i in data['data']['replies']:
            comments.append(i['content']['message'])   
            likes.append(i['like'])
            users.append(i['member']['uname'])
            #print(i['content']['message'])
            result = SnowNLP(i['content']['message']) #情感评分
            #print(result.sentiments)
            rates.append(str(result.sentiments)) #加入表格
        
data = pd.DataFrame({"用户":users,"评论":comments,"情感评分":rates,"点赞":likes})
data.to_excel("F:\\bili\\out\\bili_s.xlsx")

data = pd.read_excel(r"F:\\bili\\out\\bili_s.xlsx")
data.head()
data.describe() #数据描述
data.dropna() #删除空置
data.drop_duplicates() #删除重复值
