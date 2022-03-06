# 生成词云  simsun.ttc为字体型号 cy.jpg为词云图片，保存在out文件夹下
from wordcloud import WordCloud
import jieba
import pandas as pd
from tkinter import _flatten
from matplotlib.pyplot import imread
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

data = pd.read_excel(r"F:\\bili\\out\\bili_b.xlsx")
with open('F:\\bili\\bili_boston\\stopwords.txt', 'r', encoding='utf-8') as f:
    stopWords = f.read()
with open('F:\\bili\\bili_boston\\停用词.txt','r',encoding='utf-8') as t:
    stopWord = t.read()
    
total = stopWord.split() + stopWords.split()
def my_word_cloud(data=None, stopWords=None):
    dataCut = data.apply(jieba.lcut)  # 分词
    dataAfter = dataCut.apply(lambda x: [i for i in x if i not in stopWords])  # 去除停用词
    wordFre = pd.Series(_flatten(list(dataAfter))).value_counts()  # 统计词频
    plt.figure(figsize=(20,20))
    wc  = WordCloud(scale=10,font_path='simsun.ttc',background_color="white",)
    wc.fit_words(wordFre)
    plt.axis("off")
    plt.imshow(wc)
    wc.to_file("F:\\bili\\out\\cy.jpg")
    
my_word_cloud(data=data["评论"],stopWords=stopWords)
