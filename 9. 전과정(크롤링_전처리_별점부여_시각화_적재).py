from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from time import sleep
import requests
import re
import pandas as pd
import numpy as np
import os
import socket
import json
import logging
from datetime import datetime
import sys
from pyvirtualdisplay import Display
from elasticsearch import Elasticsearch
import warnings
import pandas as pd
import numpy as np
import pandas as pd
from pykospacing import Spacing
from hanspell import spell_checker 
from soynlp.normalizer import * 
import konlpy
from konlpy.tag import Okt
from konlpy.utils import pprint
import json
import csv
from collections import Counter, defaultdict
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
from textrank import KeywordSummarizer, KeysentenceSummarizer
import numpy as np
import math
import torch
import pandas as pd
import numpy as np
from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from keras.preprocessing.sequence import pad_sequences
from matplotlib import font_manager
import matplotlib.pyplot as plt
import urllib.request
from sklearn.model_selection import train_test_split
import time
from wordcloud import WordCloud
from PIL import Image
import base64



warnings.filterwarnings('ignore')

chrome_options = Options()

display = Display(visible = False, size = (800,800))
display.start()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

# name=['보루네오하우스 윈트 루시 LED 평상수납형 침대 SS']
category=['별점']


#보루네오하우스 윈트 루시 LED 평상수납형 침대 SS 후기
ns_address="https://search.shopping.naver.com/catalog/21731079171?query=%EC%B9%A8%EB%8C%80&NaPm=ct%3Dl1ww1gpc%7Cci%3D013ed9ccb42d3e1a808b576c5507e2beb0b06039%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Dece9e2ef2e7898482808392a378ff56709f7936c"
#xpath
shoppingmall_review='//*[@id="snb"]/ul/li[3]/a'

header = {'User-Agent': ''}
d = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options) # webdriver = chrome
d.implicitly_wait(3)
d.get(ns_address)
req = requests.get(ns_address,verify=False)
html = req.text 
soup = BeautifulSoup(html, "html.parser")
sleep(2)

name = d.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[1]/h2').text    #  제품이름
items = d.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div[1]/div/div[1]/span[3]').text   # 제품군
count = d.find_element_by_xpath('//*[@id="section_review"]/div[2]/div[2]/ul/li[1]/a/em').text   # 리뷰수
image = d.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/img').get_attribute('src')  # 이미지
id_number =0
count = count.replace('(','').replace(')','')
if '침대' in name:
    items = 'bed'
    

elastic_data = {'name': name,
                'image': image,
                'index' : items}

maria_items_name = {'name': name,
                    'items': items}


'''------------------------------"items_name" socket  --->  MariaDB-------------------------------'''
print()
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.connect(('172.20.40.52',9605))
try: 
    sock1.sendall(json.dumps(maria_items_name).encode())
    print('items_name_success')
except:
    print('실패')
finally:
    sock1.close()
'''-----------------------------------------------------------------------------------------------'''


maria_items_contents = {'count': count,
                        'image': image,
                        'name': name,
                        }



def category_star(score):
    if score < -2:
        return('⭐')

    elif score < 0:
        return('⭐⭐')

    elif score < 1:
        return('⭐⭐⭐')

    elif score < 2:
        return('⭐⭐⭐⭐')

    else :
        return('⭐⭐⭐⭐⭐')


maria_items_star = {'name': name}

#쇼핑몰 리뷰 보기
d.find_element_by_xpath(shoppingmall_review).click()
sleep(2)

element=d.find_element_by_xpath(shoppingmall_review)
d.execute_script("arguments[0].click();", element)
sleep(2)


def add_dataframe(name,category,reviews,stars,cnt):  #데이터 프레임에 저장
    #데이터 프레임생성
    df1=pd.DataFrame(columns=['type','category','review','star'])
    n=1
    if (cnt>0):
        for i in range(0,cnt-1):
            df1.loc[n]=[name,category,reviews[i],stars[i]] #해당 행에 저장
            i+=1
            n+=1
    else:
        df1.loc[n]=[name,category,'null','null']
        n+=1    
    return df1


# 리뷰 가져오기
#d.find_element_by_xpath(shoppingmall_review).click() #스크롤 건드리면 안됨
name_=name[0]
category_=category[0]
reviews=[]
stars=[]
cnt=1   #리뷰index
page=1
result = []


while True:
    if page > 100:#페이지 변경
        break
    j=1
#     print ("페이지", page ,"\n") 
    sleep(2)
    while True: #한페이지에 20개의 리뷰, 마지막 리뷰에서 error발생
        try:                              
            star=d.find_element_by_xpath('//*[@id="section_review"]/ul/li['+str(j)+']/div[1]/span[1]').text
            stars.append(star.replace('평점',''))
            review=d.find_element_by_xpath('//*[@id="section_review"]/ul/li['+str(j)+']/div[2]/div[1]/p').text
            #'//*[@id="section_review"]/ul/li[1]/div[2]/div[1]/p'
            reviews.append(review)           
            if j%2==0: #화면에 2개씩 보이도록 스크롤
                ELEMENT = d.find_element_by_xpath('//*[@id="section_review"]/ul/li['+str(j)+']/div[2]/div[1]')
                d.execute_script("arguments[0].scrollIntoView(true);", ELEMENT)       
            j+=1
            
            result.append(review)
            print(cnt, review ,star.replace('평점',''), "/ \n")
            cnt+=1 
        except: break
            
    sleep(2)
    
    if page<11:#page10
        try: #리뷰의 마지막 페이지에서 error발생
            page +=1
            next_page=d.find_element_by_xpath('//*[@id="section_review"]/div[3]/a['+str(page)+']').click() 
        except: break #리뷰의 마지막 페이지에서 process 종료
        
    else :
        try: #page11부터
            if page%10==0:
                if page >19:
                    next_page=d.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[12]').click()
                else:
                    next_page=d.find_element_by_xpath('//*[@id="section_review"]/div[3]/a[11]').click()
            else : 
                next_page=d.find_element_by_xpath('//*[@id="section_review"]/div[3]/a['+str(page%10+2)+']').click()
            page+=1
        except: break
id_number += 1            
c = 0
for i in result:
    result[c] = i.replace('\n','')
    c += 1

elastic_data['raw_review'] = result
elastic_data['star'] = stars
elastic_data['test_id'] = str(id_number)


data = result
# data = data.split(sep='/')
data = pd.DataFrame(data)

def data_preprocessing(data):
    
    # 제목과 중복되는 내용 제거
    data.drop_duplicates(subset = [0], inplace=True) # 중복 제거
    review_sum =data[0]
    

    i = 0
    for review in review_sum:
        review_space = review.replace(' ','')
        start = review_space.find('\n')
        review_enter = review_space.replace('\n','')

        if start != -1:
            title = review_enter[:start-3]
            text1 = review_enter[start:(start)*2-3]


            if title == text1:
                data[0].iloc[i] = review_enter[start:]

            else:
                pass
        i += 1
    
    
    # 한글,공백 남겨두고 띄어쓰기, 정규화 작업
    space = Spacing()
    i=0
    for review in review_sum:
        a = only_hangle(review).replace(' ','')  # 한글과 공백을 제외하고 모두 제거
        b = space(a)  # 띄어쓰기
        c = repeat_normalize(b, num_repeats=2)   # ㅋㅋㅋㅋㅋㅋ,ㅎㅎㅎㅎ 등 정규화
        data[0].iloc[i] = c
        i += 1
        
    # 공백인 행은 지우고 인덱스 초기화    
    data = data.loc[data[0] != '']
    data.reset_index(drop=True,inplace=True)
    
    # 300 이상인 리뷰 제거
    data_copy = data[0].copy()
    n = 0
    for i in data_copy:
        if len(i) >= 300:
            data.drop(n,axis=0,inplace=True)
        
        n += 1
    
    data.reset_index(drop=True,inplace=True)
   
    # 맞춤범 검사
    review_sum =data[0]
    i=0
    for review in review_sum:
        spelled_sent = spell_checker.check(review)
        data[0].iloc[i] = spelled_sent.checked
        i += 1
        
    return data

sentences = data_preprocessing(data)


preprocessing_1 = []
for re in sentences[0]:
    preprocessing_1.append(re)
print('띄어쓰기_오탈자_완료 ')


# 토큰화
f = open('stopwords.txt', 'r',encoding = 'cp949')

#불용어 리스트 만들기
stopword  = []
for word in f:
    word = word.replace('\n','')
    stopword.append(word)

#토큰화 okt
okt = Okt()
# print(preprocessing_1)

preprocessing_2 = []
temp_2 = []
for re in preprocessing_1:
    temp = okt.morphs(re,stem=True)
    # 불용어처리 

    temp_2 = []
    for word in temp:
        if word not in stopword:
            temp_2.append(word)
    
    preprocessing_2.append(' '.join(temp_2))
print('토큰화_불용어처리 완료')

elastic_data['token_stopword_review'] = preprocessing_2


class KnuSL():

    def data_list(wordname):
        # 감성 사전 불러온 후 읽기
        with open(q,encoding='utf-8', mode='r') as f:
            data = json.load(f)
        result = [0,0]
        j= 0
        포함여부 = 0
        # 3-gram
        for i in range(0, len(data)):
            if (data[i]['word_root'] in wordname):
                result.pop()
                result.pop()
                result.append(data[i]['word_root'])
                result.append(data[i]['polarity'])	
                포함여부 += 1
                j += 1
                break
            else:
                j += 1
        try:
            r_word = result[0]
            s_word = result[1]	
        except:
            pass
        return s_word, 포함여부


'''---------------------------------------가격 사전------------------------------------------'''

q = 'sentiment_dictionary_price_3gram.json'
n = 0

ksl = KnuSL   
포함여부리스트_3 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

rdr = preprocessing_2

점수리스트_3 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:],word[2:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 3-gram 만들기
            three_gram_word = ' '.join(j)
            a = ksl.data_list(three_gram_word)[0]
            b = ksl.data_list(three_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    # print(score)
    # print(b)
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('3-gram 점수 : {}'.format(score))
    # print('3-gram 포함여부 : {}'. format(p))
    점수리스트_3.append(score)
    포함여부리스트_3.append(p)


q = 'sentiment_dictionary_price_2gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_2 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

점수리스트_2 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 2-gram 만들기
            two_gram_word = ' '.join(j)
            a = ksl.data_list(two_gram_word)[0]
            b = ksl.data_list(two_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('2-gram 점수 : {}'.format(score))
    # print('2-gram 포함여부 : {}'. format(p))
    점수리스트_2.append(score)
    포함여부리스트_2.append(p)


q = 'sentiment_dictionary_price_1gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_1 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)
점수리스트_1 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    a = ksl.data_list(word)
    A =list(a)
    try:
        score += A[0]
        p += A[1]
    except:
        pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('1-gram 점수 : {}'.format(score))
    # print('1-gram 포함여부 : {}'. format(p))
    점수리스트_1.append(score)
    포함여부리스트_1.append(p)

# 사전 돌려서 나온 총 점수
total_sum = [x + y + z for x,y,z in zip(점수리스트_3, 점수리스트_2, 점수리스트_1)]

# 사전에 포함된 단어 빈도수 총 합계 
total_count = [x + y + z for x,y,z in zip(포함여부리스트_3, 포함여부리스트_2, 포함여부리스트_1)]

# 사전 단어가 한번도 등장하지 않은 리뷰 개수
count_none = total_count.count(0)

# 평균 구할때 사용되는 최종 리뷰 개수
count_sum = len(total_count) - count_none


# 단어 등장 빈도 수에 따라 나눠 평균 내주기
n = 0
total_average = []
for i in total_sum:
  try:
    score_average = i/total_count[n]
    n += 1
    total_average.append(score_average)
  except ZeroDivisionError:
    total_average.append(i)
    n += 1
    pass

# 단어가 4번 이상 등장한 리뷰에 가중치 주기
a = 0
for i in total_count:
  if i >=4 :
    if total_average[a] > 0:
      total_average[a] = total_average[a] + 1
      a += 1
    else :
      total_average[a] = total_average[a] - 1
      a += 1

  else :
    a += 1    

value_sum = sum(total_average)
######## 세분화 이름을 바꿔주세요 ######## 
try: 
    price_score = value_sum / count_sum
except:
    price_score = 0

'''-------------------------------------------내구성 사전--------------------------------------'''

q = 'sentiment_dictionary_durability_3gram.json'
n = 0

ksl = KnuSL   
포함여부리스트_3 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

rdr = preprocessing_2

점수리스트_3 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:],word[2:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 3-gram 만들기
            three_gram_word = ' '.join(j)
            a = ksl.data_list(three_gram_word)[0]
            b = ksl.data_list(three_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    # print(score)
    # print(b)
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('3-gram 점수 : {}'.format(score))
    # print('3-gram 포함여부 : {}'. format(p))
    점수리스트_3.append(score)
    포함여부리스트_3.append(p)


q = 'sentiment_dictionary_durability_2gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_2 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

점수리스트_2 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 2-gram 만들기
            two_gram_word = ' '.join(j)
            a = ksl.data_list(two_gram_word)[0]
            b = ksl.data_list(two_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('2-gram 점수 : {}'.format(score))
    # print('2-gram 포함여부 : {}'. format(p))
    점수리스트_2.append(score)
    포함여부리스트_2.append(p)


q = 'sentiment_dictionary_durability_1gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_1 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)
점수리스트_1 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    a = ksl.data_list(word)
    A =list(a)
    try:
        score += A[0]
        p += A[1]
    except:
        pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('1-gram 점수 : {}'.format(score))
    # print('1-gram 포함여부 : {}'. format(p))
    점수리스트_1.append(score)
    포함여부리스트_1.append(p)

# 사전 돌려서 나온 총 점수
total_sum = [x + y + z for x,y,z in zip(점수리스트_3, 점수리스트_2, 점수리스트_1)]

# 사전에 포함된 단어 빈도수 총 합계 
total_count = [x + y + z for x,y,z in zip(포함여부리스트_3, 포함여부리스트_2, 포함여부리스트_1)]

# 사전 단어가 한번도 등장하지 않은 리뷰 개수
count_none = total_count.count(0)

# 평균 구할때 사용되는 최종 리뷰 개수
count_sum = len(total_count) - count_none


# 단어 등장 빈도 수에 따라 나눠 평균 내주기
n = 0
total_average = []
for i in total_sum:
  try:
    score_average = i/total_count[n]
    n += 1
    total_average.append(score_average)
  except ZeroDivisionError:
    total_average.append(i)
    n += 1
    pass

# 단어가 4번 이상 등장한 리뷰에 가중치 주기
a = 0
for i in total_count:
  if i >=4 :
    if total_average[a] > 0:
      total_average[a] = total_average[a] + 1
      a += 1
    else :
      total_average[a] = total_average[a] - 1
      a += 1

  else :
    a += 1

value_sum = sum(total_average)
######## 세분화 이름을 바꿔주세요 ######## 
try:
    durability_score = value_sum / count_sum
except:
    durability_score = 0

'''-------------------------------------------디자인 사전--------------------------------------'''

q = 'sentiment_dictionary_design_3gram.json'
n = 0

ksl = KnuSL   
포함여부리스트_3 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

rdr = preprocessing_2

점수리스트_3 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:],word[2:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 3-gram 만들기
            three_gram_word = ' '.join(j)
            a = ksl.data_list(three_gram_word)[0]
            b = ksl.data_list(three_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    # print(score)
    # print(b)
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('3-gram 점수 : {}'.format(score))
    # print('3-gram 포함여부 : {}'. format(p))
    점수리스트_3.append(score)
    포함여부리스트_3.append(p)


q = 'sentiment_dictionary_design_2gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_2 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

점수리스트_2 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 2-gram 만들기
            two_gram_word = ' '.join(j)
            a = ksl.data_list(two_gram_word)[0]
            b = ksl.data_list(two_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('2-gram 점수 : {}'.format(score))
    # print('2-gram 포함여부 : {}'. format(p))
    점수리스트_2.append(score)
    포함여부리스트_2.append(p)


q = 'sentiment_dictionary_design_1gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_1 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)
점수리스트_1 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    a = ksl.data_list(word)
    A =list(a)
    try:
        score += A[0]
        p += A[1]
    except:
        pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('1-gram 점수 : {}'.format(score))
    # print('1-gram 포함여부 : {}'. format(p))
    점수리스트_1.append(score)
    포함여부리스트_1.append(p)

# 사전 돌려서 나온 총 점수
total_sum = [x + y + z for x,y,z in zip(점수리스트_3, 점수리스트_2, 점수리스트_1)]

# 사전에 포함된 단어 빈도수 총 합계 
total_count = [x + y + z for x,y,z in zip(포함여부리스트_3, 포함여부리스트_2, 포함여부리스트_1)]

# 사전 단어가 한번도 등장하지 않은 리뷰 개수
count_none = total_count.count(0)

# 평균 구할때 사용되는 최종 리뷰 개수
count_sum = len(total_count) - count_none


# 단어 등장 빈도 수에 따라 나눠 평균 내주기
n = 0
total_average = []
for i in total_sum:
  try:
    score_average = i/total_count[n]
    n += 1
    total_average.append(score_average)
  except ZeroDivisionError:
    total_average.append(i)
    n += 1
    pass

# 단어가 4번 이상 등장한 리뷰에 가중치 주기
a = 0
for i in total_count:
  if i >=4 :
    if total_average[a] > 0:
      total_average[a] = total_average[a] + 1
      a += 1
    else :
      total_average[a] = total_average[a] - 1
      a += 1

  else :
    a += 1

value_sum = sum(total_average)
######## 세분화 이름을 바꿔주세요 ######## 
try:
    design_score = value_sum / count_sum
except:
    design_score = 0


'''-------------------------------------------서비스 사전--------------------------------------'''

q = 'sentiment_dictionary_service_3gram.json'
n = 0

ksl = KnuSL   
포함여부리스트_3 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

rdr = preprocessing_2

점수리스트_3 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:],word[2:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 3-gram 만들기
            three_gram_word = ' '.join(j)
            a = ksl.data_list(three_gram_word)[0]
            b = ksl.data_list(three_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    # print(score)
    # print(b)
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('3-gram 점수 : {}'.format(score))
    # print('3-gram 포함여부 : {}'. format(p))
    점수리스트_3.append(score)
    포함여부리스트_3.append(p)


q = 'sentiment_dictionary_service_2gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_2 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)

점수리스트_2 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    z = zip(word,word[1:])
    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            # 2-gram 만들기
            two_gram_word = ' '.join(j)
            a = ksl.data_list(two_gram_word)[0]
            b = ksl.data_list(two_gram_word)[1]
            try:
                score += int(a)
                p += int(b)
                c = score/p
            except:
                pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('2-gram 점수 : {}'.format(score))
    # print('2-gram 포함여부 : {}'. format(p))
    점수리스트_2.append(score)
    포함여부리스트_2.append(p)


q = 'sentiment_dictionary_service_1gram.json'
n = 0

# ksl = KnuSL   
포함여부리스트_1 = []
# f = open('/content/total_불용어제거_0428.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)
점수리스트_1 = []
for i in rdr:
    score = 0
    p = 0
    # r = ','.join(i).replace(',',' ')
    word = i.split()
    a = ksl.data_list(word)
    A =list(a)
    try:
        score += A[0]
        p += A[1]
    except:
        pass
    n +=1   
    # print('---------------------------------------------------------------------')
    # print(n)
    # print('1-gram 점수 : {}'.format(score))
    # print('1-gram 포함여부 : {}'. format(p))
    점수리스트_1.append(score)
    포함여부리스트_1.append(p)

# 사전 돌려서 나온 총 점수
total_sum = [x + y + z for x,y,z in zip(점수리스트_3, 점수리스트_2, 점수리스트_1)]

# 사전에 포함된 단어 빈도수 총 합계 
total_count = [x + y + z for x,y,z in zip(포함여부리스트_3, 포함여부리스트_2, 포함여부리스트_1)]

# 사전 단어가 한번도 등장하지 않은 리뷰 개수
count_none = total_count.count(0)

# 평균 구할때 사용되는 최종 리뷰 개수
count_sum = len(total_count) - count_none


# 단어 등장 빈도 수에 따라 나눠 평균 내주기
n = 0
total_average = []
for i in total_sum:
  try:
    score_average = i/total_count[n]
    n += 1
    total_average.append(score_average)
  except ZeroDivisionError:
    total_average.append(i)
    n += 1
    pass

# 단어가 4번 이상 등장한 리뷰에 가중치 주기
a = 0
for i in total_count:
  if i >=4 :
    if total_average[a] > 0:
      total_average[a] = total_average[a] + 1
      a += 1
    else :
      total_average[a] = total_average[a] - 1
      a += 1

  else :
    a += 1        


# 총 점수 

value_sum = sum(total_average)
######## 세분화 이름을 바꿔주세요 ######## 
try:
    service_score = value_sum / count_sum
except:
    service_score = 0


maria_items_star['design'] = category_star(design_score)
maria_items_star['service'] = category_star(service_score)
maria_items_star['durability'] = category_star(durability_score)
maria_items_star['price'] = category_star(price_score)



tokenizer = BertTokenizer.from_pretrained('klue/bert-base', do_lower_case=False)
model2 =  BertForSequenceClassification.from_pretrained("klue/bert-base", num_labels=5)
# model2.load_state_dict(torch.load('bert_model_ver2_st_0505.pt'))
model2.load_state_dict(torch.load('BERT_trained.pt',map_location=torch.device('cpu')))
device = torch.device("cpu")
model2.to(device)
def convert_input_data(sentences):
    # BERT의 토크나이저로 문장을 토큰으로 분리
    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]
    # 입력 토큰의 최대 시퀀스 길이
    MAX_LEN = 128
    # 토큰을 숫자 인덱스로 변환
    input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]
    # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움
    input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")
    # 어텐션 마스크 초기화
    attention_masks = []
    # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
    # 패딩 부분은 BERT 모델에서 어텐션을 수행하지 않아 속도 향상
    for seq in input_ids:
        seq_mask = [float(i>0) for i in seq]
        attention_masks.append(seq_mask)
    # 데이터를 파이토치의 텐서로 변환
    inputs = torch.tensor(input_ids)
    masks = torch.tensor(attention_masks)
    return inputs, masks
# 문장 테스트
def test_sentences(sentences):
    # 평가모드로 변경
    model2.eval()
    # 문장을 입력 데이터로 변환
    inputs, masks = convert_input_data(sentences)
    # 데이터를 GPU에 넣음
    b_input_ids = inputs.to(device)
    b_input_mask = masks.to(device)
    # 그래디언트 계산 안함
    with torch.no_grad():
        # Forward 수행
        outputs = model2(b_input_ids,
                        token_type_ids=None,
                        attention_mask=b_input_mask)
    # 로스 구함
    logits = outputs[0]
    # CPU로 데이터 이동
    logits = logits.detach().cpu().numpy()
    return logits
sentences_re = []
predict_star_list = []   # elastic에 추가

# while True:
    # print('리뷰를 입력해 주세요. : ')
for re in preprocessing_1:
    # review = preprocessing_1 
    # for re in review:
    logits = test_sentences([re])
    # print(logits)
    # print(np.argmax(logits))
    if np.argmax(logits) == 0 :
        # print(review)
        print("⭐")
        print('-----------------------------------------------------------------------------------------------')
        sentences_re.append(1)
        predict_star_list.append("⭐")
    elif np.argmax(logits) == 1 :
        # print(i)
        print("⭐⭐")
        print('-----------------------------------------------------------------------------------------------')
        sentences_re.append(2)
        predict_star_list.append("⭐⭐")
    elif np.argmax(logits) == 2 :
        # print(i)
        print("⭐⭐⭐")
        print('-----------------------------------------------------------------------------------------------')
        sentences_re.append(3)
        predict_star_list.append("⭐⭐⭐")
    elif np.argmax(logits) == 3 :
        # print(i)
        print("⭐⭐⭐⭐")
        print('-----------------------------------------------------------------------------------------------')
        sentences_re.append(4)
        predict_star_list.append("⭐⭐⭐⭐")
    else :
        # print(i)
        print("⭐⭐⭐⭐⭐")
        print('-----------------------------------------------------------------------------------------------')
        sentences_re.append(5)
        predict_star_list.append("⭐⭐⭐⭐⭐")    

old_star = []
# print(stars)
for i in range(len(stars)):
    if stars[i] == '1':
        old_star.append("⭐")
    elif stars[i] == '2':
        old_star.append("⭐⭐")
    elif stars[i] == '3':
        old_star.append("⭐⭐⭐")
    elif stars[i] == '4':
        old_star.append("⭐⭐⭐⭐")
    else:
        old_star.append("⭐⭐⭐⭐⭐")

tm2 = []
for c in range(len(preprocessing_1)):
    tm1 = []
    
    tm1.append(preprocessing_1[c])
    tm1.append(old_star[c])
    tm1.append(predict_star_list[c])
    tm2.append(tm1)
elastic_data['spacing_spell_review'] = tm2 #list(map(list.__add__, preprocessing_1, [predict_star_list])) 
'''------------------------------elastic --->  reviews socket-------------------------------'''
# sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock3.connect(('172.20.40.52',9602))
# try: 
#     sock3.sendall(json.dumps(elastic_data).encode())
#     print('elasticsearch_success')
#     print(elastic_data)
# except Exception as e:
#     print('실패',e)
# finally:
#     sock3.close()

'''-------------------------------------------총별점------------------------------------------'''
total_star = round(sum(sentences_re)/len(sentences_re), 3)
maria_items_star['total'] = total_star

print("starting to send data to MariaDB")

sock4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock4.connect(('172.20.40.52',9603))
message = []
try:
    sock4.sendall(json.dumps(maria_items_star).encode())
    print("Sent")
except socket.error as e:
    sys.stderr.write(str(e))
finally:
    sock4.close()
print('MariaDB의 star 테이블로 데이터 전송 완료 ')

'''-------------------------------------------------------------------------------------'''
'''-------------------------------------------긍부정 분류------------------------------------------'''
# a = [('부정1','⭐'),('부정2','⭐⭐'),('중립','⭐⭐⭐'),('긍정1','⭐⭐⭐⭐'),('긍정2','⭐⭐⭐⭐⭐')]

positive = []
negative = []
for i in elastic_data['spacing_spell_review']:
  if i[2] == '⭐' or  i[2] == '⭐⭐':
    negative.append(i[0])
  elif  i[2] == '⭐⭐⭐⭐' or  i[2] == '⭐⭐⭐⭐⭐':
    positive.append(i[0])
'''-----------------------------------------------------------------------------------------------'''


'''-------------------------------------------textrank_요약----------------------------------------'''
# min_count 최소 빈도수
def scan_vocabulary(sents, tokenize, min_count=2):
    counter = Counter(w for sent in sents for w in tokenize(sent))
    counter = {w:c for w,c in counter.items() if c >= min_count}
    idx_to_vocab = [w for w, _ in sorted(counter.items(), key=lambda x:-x[1])]
    vocab_to_idx = {vocab:idx for idx, vocab in enumerate(idx_to_vocab)}
    return idx_to_vocab, vocab_to_idx



# 두 단어간 유사도 정의
# window 단어들 간격 설정 가능
def cooccurrence(tokens, vocab_to_idx, window=2, min_cooccurrence=2):
    counter = defaultdict(int)
    for s, tokens_i in enumerate(tokens):
        vocabs = [vocab_to_idx[w] for w in tokens_i if w in vocab_to_idx]
        n = len(vocabs)
        for i, v in enumerate(vocabs):
            if window <= 0:
                b, e = 0, n
            else:
                b = max(0, i - window)
                e = min(i + window, n)
            for j in range(b, e):
                if i == j:
                    continue
                counter[(v, vocabs[j])] += 1
                counter[(vocabs[j], v)] += 1
    counter = {k:v for k,v in counter.items() if v >= min_cooccurrence}
    n_vocabs = len(vocab_to_idx)
    return dict_to_mat(counter, n_vocabs, n_vocabs)



#dictionary 형식의 그래프를 sparse matrix(희소 행렬)로 변환
def dict_to_mat(d, n_rows, n_cols):
    rows, cols, data = [], [], []
    for (i, j), v in d.items():
        rows.append(i)
        cols.append(j)
        data.append(v)
    return csr_matrix((data, (rows, cols)), shape=(n_rows, n_cols))



#명사, 동사, 형용사와 같은 단어들만 return
def word_graph(sents, tokenize=None, min_count=2, window=2, min_cooccurrence=2):
    idx_to_vocab, vocab_to_idx = scan_vocabulary(sents, tokenize, min_count)
    tokens = [tokenize(sent) for sent in sents]
    g = cooccurrence(tokens, vocab_to_idx, window, min_cooccurrence, verbose)
    return g, idx_to_vocab



# pagerank 학습
def pagerank(x, df=0.85, max_iter=30):
    assert 0 < df < 1

    # initialize
    A = normalize(x, axis=0, norm='l1')
    R = np.ones(A.shape[0]).reshape(-1,1)
    bias = (1 - df) * np.ones(A.shape[0]).reshape(-1,1)

    # iteration
    for _ in range(max_iter):
        R = df * (A * R) + bias

    return R




def textrank_keyword(sents, tokenize, min_count, window, min_cooccurrence, df=0.85, max_iter=30, topk=30):
    g, idx_to_vocab = word_graph(sents, tokenize, min_count, window, min_cooccurrence)
    R = pagerank(g, df, max_iter).reshape(-1)
    idxs = R.argsort()[-topk:]
    keywords = [(idx_to_vocab[idx], R[idx]) for idx in reversed(idxs)]
    return keywords




#핵심 문장 추출을 위한 그래프 생성 함수
def sent_graph(sents, tokenize, similarity, min_count=2, min_sim=0.3):
    _, vocab_to_idx = scan_vocabulary(sents, tokenize, min_count)

    tokens = [[w for w in tokenize(sent) if w in vocab_to_idx] for sent in sents]
    rows, cols, data = [], [], []
    n_sents = len(tokens)
    for i, tokens_i in enumerate(tokens):
        for j, tokens_j in enumerate(tokens):
            if i >= j:
                continue
            sim = similarity(tokens_i, tokens_j)
            if sim < min_sim:
                continue
            rows.append(i)
            cols.append(j)
            data.append(sim)
    return csr_matrix((data, (rows, cols)), shape=(n_sents, n_sents))


#문장간 유사도를 textrank로 구하는 함수
def textrank_sent_sim(s1, s2):
    n1 = len(s1)
    n2 = len(s2)
    if (n1 <= 1) or (n2 <= 1):
        return 0
    common = len(set(s1).intersection(set(s2)))
    base = math.log(n1) + math.log(n2)
    return common / base



#문장간 유사도를 cosine으로 구하는 함수
def cosine_sent_sim(s1, s2):
    if (not s1) or (not s2):
        return 0

    s1 = Counter(s1)
    s2 = Counter(s2)
    norm1 = math.sqrt(sum(v ** 2 for v in s1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in s2.values()))
    prod = 0
    for k, v in s1.items():
        prod += v * s2.get(k, 0)
    return prod / (norm1 * norm2)



#핵심 문장 추출 함수
def textrank_keysentence(sents, tokenize, min_count, similarity, df=0.85, max_iter=30, topk=5):
    g = sent_graph(sents, tokenize, min_count, min_sim, similarity)
    R = pagerank(g, df, max_iter).reshape(-1)
    idxs = R.argsort()[-topk:]
    keysents = [(idx, R[idx], sents[idx]) for idx in reversed(idxs)]
    return keysents



#okt로 토큰화
okt = Okt()
def okt_tokenize(sent):
    words = okt.phrases(sent)
    return words


sents_p = positive
sents_n = negative
summarizer = KeysentenceSummarizer(tokenize = okt_tokenize, min_sim = 0.3)  # min_sim=0.3은 similarity가 0.3 이상이라는 의미
keysents_p = summarizer.summarize(sents_p, topk=1) # topk는 출력 문장 개수
keysents_n = summarizer.summarize(sents_n, topk=1)


maria_items_contents['summary_positive'] = keysents_p[0][2]
maria_items_contents['summary_negative'] = keysents_n[0][2]

'''------------------------------maria2 --->  item_contents socket-------------------------------'''

sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2.connect(('172.20.40.52', 9604))
try: 
    sock2.sendall(json.dumps(maria_items_contents).encode())
    print('items_contents_success')
except:
    print('실패')
finally:
    sock2.close()


'''------------------------------wordcloud-------------------------------'''
positive = positive
negative = negative
okt = Okt()
result_negative = []
result_positive = []
maria_items_visualization = {'name': name}

def WordCloud_bed_negative(df):
    for i in negative:
        words = okt.nouns(i)
        for word in words:
            result_negative.append(word)

    words = Counter(result_negative)
    tags = words.most_common(200)

    c = dict(tags)

    img = Image.open('bed.png')
    mask = np.array(img)

    wc = WordCloud(font_path = 'malgunbd.ttf', width = 400, height = 400, max_font_size=100, background_color = 'white', mask = mask, colormap = 'gist_heat')
    wc_g = wc.generate_from_frequencies(c)


    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(wc_g)
    # plt.show()
    plt.savefig('WordCloud_bed_negative.png',bbox_inches='tight')
    plt.close()


def WordCloud_bed_positive(df):
    for i in positive:
        words = okt.nouns(i)
        for word in words:
            result_positive.append(word)

    words = Counter(result_positive)
    tags = words.most_common(200)

    c = dict(tags)

    img = Image.open('bed.png')
    mask = np.array(img)

    wc = WordCloud(font_path = 'malgunbd.ttf', width = 400, height = 400, max_font_size=100, background_color = 'white', mask = mask, colormap = 'winter')
    wc_g = wc.generate_from_frequencies(c)


    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(wc_g)
    # plt.show()
    plt.savefig('WordCloud_bed_positive.png',bbox_inches='tight')
    plt.close()    



WordCloud_bed_negative(negative)
WordCloud_bed_positive(positive)

with open("WordCloud_bed_negative.png", "rb") as image_file:
	negative_image = image_file.read()
# Base64로 인코딩
negative_image = base64.b64encode(negative_image)
# UTF-8로 디코딩
negative_image = negative_image.decode('UTF-8')

with open("WordCloud_bed_positive.png", "rb") as image_file:
	positive_image = image_file.read()
# Base64로 인코딩
positive_image = base64.b64encode(positive_image)
# UTF-8로 디코딩
positive_image = positive_image.decode('UTF-8')

# sql = "INSERT INTO visualization (image, date, time) VALUES(%s,%s,%s)"
# curs.execute(sql, (binary_image, date, time))
# _conn.commit()
# _conn.close()

maria_items_visualization['wordcloud_negative'] =  negative_image #Image.open('WordCloud_bed_negative.png')#WordCloud_bed_negative(negative)
maria_items_visualization['wordcloud_positive'] =  positive_image #Image.open('WordCloud_bed_positive.png')#WordCloud_bed_positive(positive)


'''-------------------------------------------old star vs new star---------------------------------------------------'''

#우리별점

# def searchAPI():
#     es = Elasticsearch('http://172.20.40.189:9200')
#     res = es.search(
#         index='bed',
#         body={ "query":
#             {"match_all":  {   }}})
#     return res
# elastic = searchAPI()
# stars = elastic['hits']['hits'][0]['_source']['spacing_spell_review']  # 보고 싶은 키값 ex) spacing_spell_review

star = []
for i in tm2:
  a = len(i[2])
  star.append(a)

a = star.count(1)
b = star.count(2)
c = star.count(3)
d = star.count(4)
e = star.count(5)
values = [a,b,c,d,e]

score = [1,2,3,4,5]
colors = ['#62F062', '#12BE12', '#0E970E', '#085408', '#042A04']

def add_value_label(x_list,y_list):
    for i in range(1, len(x_list)+1):
        plt.text(i,y_list[i-1],y_list[i-1], fontsize=15)
        
plt.rcParams["figure.figsize"] = (12, 8)
plt.bar(score,values, color=colors,alpha = 0.6)
add_value_label(score,values)
plt.title("New Star", fontsize=20)
plt.xlabel("Star Score")
plt.ylabel("Count")

plt.savefig('star_bed_new.png',bbox_inches='tight')
plt.close()

#기존별점
# def searchAPI():
#     es = Elasticsearch('http://172.20.40.189:9200')
#     res = es.search(
#         index='bed',
#         body={ "query":
#             {"match_all":  {   }}})
#     return res
# elastic = searchAPI()
# stars = elastic['hits']['hits'][0]['_source']['star']  # 보고 싶은 키값 ex) spacing_spell_review

stars = list(map(int,stars))

a = stars.count(1)
b = stars.count(2)
c = stars.count(3)
d = stars.count(4)
e = stars.count(5)
values = [a,b,c,d,e]

score = [1,2,3,4,5]
colors = ['#FAB8C8', '#DB8AB6', '#C061A6', '#923A83', '#8A0F86']

def add_value_label(x_list,y_list):
    for i in range(1, len(x_list)+1):
        plt.text(i,y_list[i-1],y_list[i-1], fontsize=15)
        
plt.rcParams["figure.figsize"] = (12, 8)
plt.bar(score,values, color=colors,alpha = 0.6)
add_value_label(score,values)
plt.title("Old Star", fontsize=20)
plt.xlabel("Star Score")
plt.ylabel("Count")

plt.savefig('star_bed_old.png',bbox_inches='tight')
plt.close()

with open("star_bed_new.png", "rb") as image_file:
	new_image = image_file.read()
# Base64로 인코딩
new_image = base64.b64encode(new_image)
# UTF-8로 디코딩
new_image = new_image.decode('UTF-8')

with open("star_bed_old.png", "rb") as image_file:
	old_image = image_file.read()
# Base64로 인코딩
old_image = base64.b64encode(old_image)
# UTF-8로 디코딩
old_image = old_image.decode('UTF-8')

maria_items_visualization['star_old'] = old_image
maria_items_visualization['star_new'] = new_image


'''---------------------------------------------new star_pie------------------------------------------------'''

#우리별점

# def searchAPI():
#     es = Elasticsearch('http://172.20.40.189:9200')
#     res = es.search(
#         index='bed',
#         body={ "query":
#             {"match_all":  {   }}})
#     return res
# elastic = searchAPI()
# stars = elastic['hits']['hits'][0]['_source']['spacing_spell_review']  # 보고 싶은 키값 ex) spacing_spell_review

star = []
for i in tm2:
  a = len(i[2])
  star.append(a)

a = star.count(1)
b = star.count(2)
c = star.count(3)
d = star.count(4)
e = star.count(5)
values = [a,b,c,d,e]

v_sum = sum(values)
v_a = []
for i in values:
    q = round(i/v_sum*100, 1)
    v_a.append(q)

score = ['1 Star   Unit : %','2 Star','3 Star','4 Star','5 Star']
colors = ['#EFA2A1', '#E0BAAA', '#C9D8B5', '#BAEBBA', '#B3F5BE']

width_num = 0.4
count = [v_sum]
fig, ax = plt.subplots()
ax.axis('equal')
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 23

pie_outside, _ = ax.pie(v_a,radius=1.3,labeldistance=0.8,colors = colors, pctdistance=0.85,labels=v_a)
plt.setp(pie_outside,width=width_num, edgecolor='white')
pie_inside, plt_labels, junk = ax.pie(count, radius=(1.3 - width_num),labeldistance=0.75,autopct='                            Total count \n                           {}'.format(count[0]),colors=['white'])
plt.setp(pie_inside,width=width_num, edgecolor='white') 
plt.title("New Star \n ", fontsize=30)
plt.legend(score,loc='lower center', bbox_to_anchor=(0.35, -0.3, 0.3, 1),ncol=3)
plt.savefig('star_bed_new_pie.png',bbox_inches='tight')
plt.close()

with open("star_bed_new_pie.png", "rb") as image_file:
	new_image = image_file.read()
# Base64로 인코딩
new_image = base64.b64encode(new_image)
# UTF-8로 디코딩
new_image = new_image.decode('UTF-8')

maria_items_visualization['star_new_pie'] = new_image



'''---------------------------------------------new star_pie------------------------------------------------'''

sock5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock5.connect(('172.20.40.52', 9606))
try: 
    sock5.sendall(json.dumps(maria_items_visualization).encode())
    print('items_visualization로 wordcloud 전송 완료')
except:
    print('실패')
finally:
    sock5.close()