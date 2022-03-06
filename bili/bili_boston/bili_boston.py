# 生成表格文件
import requests
import pandas as pd
from collections import defaultdict
import jieba
 
#生成stopword表，需要去除一些否定词和程度词汇
stopwords = set()
fr = open('F:\\bili\\bili_boston\\停用词.txt','r',encoding='utf-8')
for word in fr:
	stopwords.add(word.strip())#Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
#读取否定词文件
not_word_file = open('F:\\bili\\bili_boston\\否定词.txt','r+',encoding='utf-8')
not_word_list = not_word_file.readlines()
not_word_list = [w.strip() for w in not_word_list]
#读取程度副词文件
degree_file = open('F:\\bili\\bili_boston\\程度副词.txt','r+',encoding='utf-8')
degree_list = degree_file.readlines()
degree_list = [item.split(',')[0] for item in degree_list]
#生成新的停用词表			
with open('F:\\bili\\bili_boston\\stopwords.txt','w',encoding='utf-8') as f:
	for word in stopwords:
		if(word not in not_word_list) and (word not in degree_list):
			f.write(word+'\n')
 
 
#jieba分词后去除停用词
def seg_word(sentence):
	seg_list = jieba.cut(sentence)
	seg_result = []
	for i in seg_list:
		seg_result.append(i)
	stopwords = set()
	with open('F:\\bili\\bili_boston\\stopwords.txt','r',encoding='utf-8') as fr:
		for i in fr:
			stopwords.add(i.strip())
	return list(filter(lambda x :x not in stopwords,seg_result))		
 
 
 
#找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
	#读取情感词典文件
	sen_file = open('F:\\bili\\bili_boston\\BosonNLP_sentiment_score.txt','r+',encoding='utf-8')
	#获取词典文件内容
	sen_list = sen_file.readlines()
	#创建情感字典
	sen_dict = defaultdict()
	#读取词典每一行的内容，将其转换成字典对象，key为情感词，value为其对应的权重
	for i in sen_list:
		if len(i.split(' '))==2:
			sen_dict[i.split(' ')[0]] = i.split(' ')[1]
 
	#读取否定词文件
	not_word_file = open('F:\\bili\\bili_boston\\否定词.txt','r+',encoding='utf-8')
	not_word_list = not_word_file.readlines()
	#读取程度副词文件
	degree_file = open('F:\\bili\\bili_boston\\程度副词.txt','r+',encoding='utf-8')
	degree_list = degree_file.readlines()
	degree_dict = defaultdict()
	for i in degree_list:
		degree_dict[i.split(',')[0]] = i.split(',')[1]
 
	sen_word = dict()
	not_word = dict()
	degree_word = dict()
	#分类
	for i in range(len(word_list)):
		word = word_list[i]
		if word in sen_dict.keys() and word not in not_word_list and word not in degree_dict.keys():
			# 找出分词结果中在情感字典中的词
			sen_word[i] = sen_dict[word]
		elif word in not_word_list and word not in degree_dict.keys():
			# 分词结果中在否定词列表中的词
			not_word[i] = -1
		elif word in degree_dict.keys():
			# 分词结果中在程度副词中的词
			degree_word[i]  = degree_dict[word]
 
 
	#关闭打开的文件
	sen_file.close()
	not_word_file.close()
	degree_file.close()
	#返回分类结果
	return sen_word,not_word,degree_word
 
#计算情感词的分数
def score_sentiment(sen_word,not_word,degree_word,seg_result):
	#权重初始化为1
	W = 1
	score = 0
	#情感词下标初始化
	sentiment_index = -1
	#情感词的位置下标集合
	sentiment_index_list = list(sen_word.keys())
	#遍历分词结果
	for i in range(0,len(seg_result)):
		#如果是情感词
		if i in sen_word.keys():
			#权重*情感词得分
			score += W*float(sen_word[i])
			#情感词下标加一，获取下一个情感词的位置
			sentiment_index += 1
			if sentiment_index < len(sentiment_index_list)-1:
				#判断当前的情感词与下一个情感词之间是否有程度副词或否定词
				for j in range(sentiment_index_list[sentiment_index],sentiment_index_list[sentiment_index+1]):
					#更新权重，如果有否定词，权重取反
					if j in not_word.keys():
						W *= -1
					elif j in degree_word.keys():
						W *= float(degree_word[j])	
		#定位到下一个情感词
		if sentiment_index < len(sentiment_index_list)-1:
			i = sentiment_index_list[sentiment_index+1]
	return score
 
 
#计算得分
def sentiment_score(sentence):
	#1.对文档分词
	seg_list = seg_word(sentence)
	#2.将分词结果转换成字典，找出情感词、否定词和程度副词
	sen_word,not_word,degree_word = classify_words(seg_list)
	#3.计算得分
	score = score_sentiment(sen_word,not_word,degree_word,seg_list)
	return score

#请求数据
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0", "Cookie": "_uuid=827B8494-A44C-31D0-9BD4-DFF80A5E0FEE82120infoc; buvid3=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; sid=adec7tca; bp_video_offset_398722478=497617492191521518; PVID=2; CURRENT_FNVAL=80; rpdid=|(um~kmlu|lR0J'ulmlY~~uJY; LIVE_BUVID=AUTO6815959410724974; CURRENT_QUALITY=80; blackside_state=1; fingerprint3=9705c866e2e5e695c6e38746c7a602b7; fingerprint=3ed5802aad09c12021d5aec79dff4604; fingerprint_s=ad649c5d9fd6fcfeb770fa2baf91990b; buivd_fp=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; buvid_fp_plain=6D98D0E6-B61B-4EF6-8419-5ACD0EF3710E95147infoc; buvid_fp=9F4694D1-B9D6-4004-8D82-7B2B8A788B27143098infoc; DedeUserID=398722478; DedeUserID__ckMd5=a7040f6f6a474e19; SESSDATA=49f91206%2C1626876204%2Cd3b97*11; bili_jct=ebc530ed75291ef66baf035af911fab7; bp_t_offset_398722478=489028433772728540"} 
comments,users,likes,rates = [],[],[],[]
# 示例url "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=48624233&sort=0&pn=" 高数
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=33&oid=4132&sort=0&_=1617613130901&pn=" 考研政治
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=29971113&sort=0&_=1617613830551&pn=" 线代
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=87631035&sort=0&_=1617613611881&pn=" 英语单词
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=79633193&sort=0&_=1617615894965&pn=" 英语听力
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=70211798&sort=0&_=1618808663183&pn=" 计算机组成原理 41页
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=70156862&sort=0&_=1618808844107&pn=" 操作系统 36页
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=92191094&sort=0&_=1618808963480&pn=" 数据结构 48页
# "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=70228743&sort=0&_=1618809136543&pn=" 计算机网络 45页
original_url = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&oid=70228743&sort=0&_=1618809136543&pn="
for page in range(1,45): #可以修改评论页数  oid为视频号 sort为0时按时间排序 为1时按热度排序 pn为页数
    url = original_url + str(page)
    print(url)
    try:
        html = requests.get(url, headers=headers)
        data = html.json()
        if data['data']['replies']:
            for i in data['data']['replies']:
                comments.append(i['content']['message'])   
                likes.append(i['like'])
                users.append(i['member']['uname'])
                result = sentiment_score(i['content']['message']) #情感评分
                rates.append(str(result)) #加入表格
    except Exception as err:
        print(url)
        print(err)

#写入表格        
data = pd.DataFrame({"用户":users,"评论":comments,"情感评分":rates,"点赞":likes})
data.to_excel("F:\\bili\\out\\bili_jw.xlsx")

data = pd.read_excel(r"F:\\bili\\out\\bili_jw.xlsx")
data.head()
data.describe() #数据描述
data.dropna() #删除空置
data.drop_duplicates() #删除重复值



