from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
# data = pd.DataFrame.from_records(res)import mariadb
import sys
import pandas as pd
import mariadb

from elasticsearch import Elasticsearch
from elasticsearch import helpers

import torch
import pandas as pd
import numpy as np

import requests
from io import BytesIO
from PIL import Image
import time
import base64


from transformers import BertTokenizer
from transformers import BertForSequenceClassification, AdamW, BertConfig
from keras.preprocessing.sequence import pad_sequences

import gc


def convert_input_data(sentences):

      # BERT의 토크나이저로 문장을 토큰으로 분리
      tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]

      # 입력 토큰의 최대 시퀀스 길이
      MAX_LEN = 128

      # 토큰을 숫자 인덱스로 변환
      input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_stexts]
      
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



gc.collect()
torch.cuda.empty_cache()


tokenizer = BertTokenizer.from_pretrained('klue/bert-base', do_lower_case=False)

model2 =  BertForSequenceClassification.from_pretrained("klue/bert-base", num_labels=5)
# model2.load_state_dict(torch.load('bert_model_ver2_st_0505.pt'))
model2.load_state_dict(torch.load('/home/temp/post/bert_model_ver2(77)_st_0505.pt',map_location=torch.device('cpu')))

device = torch.device("cpu")
model2.to(device)
global name
name = ''
global res
res = ' '
global res2
res2 = ' '
global res3
res3 = ' '
global res4
res4 = ' '
global index
index = ' '
global name_use_review
name_use_review = ' '
global sentence
sentence = ' '
try:
    conn = mariadb.connect(
        user="root",
        password="password",
        # host="172.20.40.52",
        host="172.20.40.108",
        port=3306,
        database="test"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)



def searchAPI(ind):
    # es = Elasticsearch('http://172.20.40.52:9200')
    es = Elasticsearch('http://172.20.40.108:9200')
   
    res = es.search(index=ind,body={ "query":
            {"match_all":  {   }}})
    return res

# Create your views here.
def index(request):
  #코드 구현
  cur = conn.cursor()
  cur.execute('select * from contents')
  res = cur.fetchall()   # contents
  
  cur2 = conn.cursor()
  cur2.execute('select * from name')
  res2= cur2.fetchall()   # name

  

  name_list = []
  image_list = []
  item_list = []
  for i in range(len(res)):
      name_list.append(res[i][0])
  for i in range(len(res)):
      image_list.append(res[i][1])
  for i in range(len(res2)):
      item_list.append(res2[i][0])


  context = {'name':name_list, 'image':image_list, 'item':item_list}
  return render(request, "index.html",context)

def detail(request):
    global res
    global res2
    global res3
    global name
    
    '''-----------------------------------------------------------------------모델 함수 정의---------------------------------------------------------'''
    # 모델 함수 정의------------------------------------------------------------------------------------------------------------------------------
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

            #   '''--------------------------------------------------------------------모델 함수 정의 끝 ----------------------------------------------------------------------------'''

          # ------------------------------------------------------------------------------------------------------------------------------------------
          #   print(res)
  # Image.open(BytesIO(res.content))
    if bool(request.GET.get('name')) != 0:
        name = request.GET.get('name')
        name = '%' + name +'%'
        print(name)
    else:
        print('0')
    # print(name)
    # try:
    #     conn = mariadb.connect(
    #     user="root",
    #     password="password",
    #     host="172.20.40.189",
    #     port=3306,
    #     database="test"
    # )
    # except mariadb.Error as e:
    #     print(f"Error connecting to MariaDB Platform: {e}")
    #     sys.exit(1)


    # '''해당 제품의 제목과 사진 요약 가져오기'''

   
    cur = conn.cursor()
    #   cur.execute('select * from contents')
    cur.execute("select * from contents where name like (?)" ,(name,))
    res = cur.fetchall()   # contents
    print(name)
   # '''해당 제품의 별점 가져오기'''
    cur2 = conn.cursor()
    cur2.execute("select * from star where name like (?)" ,(name,))
    res2 = cur2.fetchall()   # star
    
    # 그래프 가져오기------------------------------------------------------------------------------------------
    cur3 = conn.cursor()
    # cur3.execute("select * from visualization where name like (?)" ,(name,))
    cur3.execute("select * from visualization where name like (?)",(name,))
    res3 = cur3.fetchall()   # visualization
     

    wordcloud_n = res3[0][1].decode() 
    wordcloud_p = res3[0][2].decode()
    pie = res3[0][5].decode()

    review_n = res[0][2]
    review_p = res[0][3]

    if len(res[0][2]) > len(res[0][3]):
        length = len(res[0][2]) - len(res[0][3])
        review_p = review_p + ' ' + ('\n' * length)
        
    else:
        length = len(res[0][3]) - len(res[0][2])
        review_n = review_n + ' ' + ('\n' * length)

    

    # print(review_n)
    # print(review_p)
    global sentence
    if bool(request.GET.get('sentence')):
      sentence = request.GET.get('sentence')
      print(sentence)
      print(type(sentence))
      #'''--------------------------------------------------------------------------모델 예측 부분---------------------------------------------------------------------------------'''
      logits = test_sentences([request.GET.get('sentence')])
      print(logits)
      # print(logits)
      # print(np.argmax(logits))
      if np.argmax(logits) == 0 :
      # print(review)
        # print("⭐")
        # print('-----------------------------------------------------------------------------------------------')
        predict_star = "⭐"
        print(predict_star)
        #   return render(request,'predict.html',context2)
        # sentences_re.append(1)
      elif np.argmax(logits) == 1 :
        # print(i)
        # print("⭐⭐")
        # print('-----------------------------------------------------------------------------------------------')
        predict_star = "⭐⭐"
        print(predict_star)
        #   return render(request,'predict.html',context2)
        # sentences_re.append(2)
      elif np.argmax(logits) == 2 :
        # print(i)
        print("⭐⭐⭐")
        print('-----------------------------------------------------------------------------------------------')
        predict_star = '⭐⭐⭐'
        #   return render(request,'predict.html',context2)
        # sentences_re.append(3)
      elif np.argmax(logits) == 3 :
        # print(i)
        # print("⭐⭐⭐⭐")
        # print('-----------------------------------------------------------------------------------------------')
        predict_star = '⭐⭐⭐⭐'
        print(predict_star)
        #   return render(request,'predict.html',context2)
        # sentences_re.append(4)
      else :
        # print(i)
        # print("⭐⭐⭐⭐⭐")
        # print('-----------------------------------------------------------------------------------------------')
        predict_star = "⭐⭐⭐⭐⭐"
        print(predict_star)
        #   return render(request,'predict.html',context2)
        # sentences_re.append(5)
    try:
      print(predict_star)
    except:
      print('not star')
    '''  ------------------------------------------------------------------------------------------------------------------------------------------------------------            '''
    try:
        context = { 'image' : res[0][1] ,'name': res[0][0],'star':round(float(res2[0][1]),2),'design':res2[0][2],'service':res2[0][5],
        'durability':res2[0][3],'price':res2[0][4],'predict': [sentence,predict_star],'review':review_n,'review_p':review_p,'count':res[0][3],'wordcloud_n':wordcloud_n,'wordcloud_p':wordcloud_p,'pie':pie}#,'spacing':spacing_review} 
    except:
        context = { 'image' : res[0][1] ,'name': res[0][0],'star':round(float(res2[0][1]),2),'design':res2[0][2],'service':res2[0][5],
        'durability':res2[0][3],'price':res2[0][4],'review':review_n,'review_p':review_p,'count':res[0][3],'wordcloud_n':wordcloud_n,'wordcloud_p':wordcloud_p,'pie':pie}#,'spacing':spacing_review} 
        pass
    return render(request,'tem.html',context)

def reviews(request):

  global name_use_review
  global res4
  
  if bool(request.GET.get('name1')) != 0:
    name_t = request.GET.get('name1')
    #   index = elastic.body['hits']['hits'][0]['_source']['raw_review']
    name_use_review = '%' + name_t +'%'

    cur4 = conn.cursor()
    cur4.execute("select * from visualization where name like (?)",(name_use_review,))
    res4 = cur4.fetchall()   # visualization
    
    print(1)
    print(name_use_review)
    
  else:
    #   elastic = searchAPI(request.GET.get(index))
    print(0)
    
  star_old = res4[0][3].decode() 
  star_new = res4[0][4].decode()

  global index
  index_t = request.GET.get('item')
#   print(request.GET.get('item'))
#   elastic = searchAPI(request.GET.get('item'))
  if bool(request.GET.get('item')) != 0:
      
      elastic = searchAPI(request.GET.get('item'))
    #   index = elastic.body['hits']['hits'][0]['_source']['raw_review']
      index = elastic.body['hits']['hits'][0]['_source']['spacing_spell_review']
      print(1)
    #   print(index)
  else:
    #   elastic = searchAPI(request.GET.get(index))
      print(0)
    #   print(index)


  # mariaDB 접속 후 그래프 가져오기    

#   try:
#     # spacing_review = elastic.body['hits']['hits'][0]['_source']['spacing_spell_review']
#     spacing_review = elastic.body['hits']['hits'][0]['_source']['raw_review']
#   except:
#       pass
  review_list = []
  star_list = []
#   for i in range(len(spacing_review)):
#       review_list.append(spacing_review[i][0])
#   for i in range(len(spacing_review)):
#       star_list.append(spacing_review[i][1])
  page = request.GET.get('page','1')
  paginator = Paginator(index,10)
  page_obj = paginator.get_page(page)
  context2 = { 'review_list':page_obj ,'star_old':star_old,'star_new':star_new}#, 'star_list':star_list}
  return render(request,'review.html',context2)

# def predict(request):


#   def convert_input_data(sentences):

#       # BERT의 토크나이저로 문장을 토큰으로 분리
#       tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]

#       # 입력 토큰의 최대 시퀀스 길이
#       MAX_LEN = 128

#       # 토큰을 숫자 인덱스로 변환
#       input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_stexts]
      
#       # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움
#       input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

#       # 어텐션 마스크 초기화
#       attention_masks = []

#       # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
#       # 패딩 부분은 BERT 모델에서 어텐션을 수행하지 않아 속도 향상
#       for seq in input_ids:
#           seq_mask = [float(i>0) for i in seq]
#           attention_masks.append(seq_mask)

#       # 데이터를 파이토치의 텐서로 변환
#       inputs = torch.tensor(input_ids)
#       masks = torch.tensor(attention_masks)

#       return inputs, masks

#   # 문장 테스트
#   def test_sentences(sentences):

#       # 평가모드로 변경
#       model2.eval()

#       # 문장을 입력 데이터로 변환
#       inputs, masks = convert_input_data(sentences)

#       # 데이터를 GPU에 넣음
#       b_input_ids = inputs.to(device)
#       b_input_mask = masks.to(device)
              
#       # 그래디언트 계산 안함
#       with torch.no_grad():     
#           # Forward 수행
#           outputs = model2(b_input_ids, 
#                           token_type_ids=None, 
#                           attention_mask=b_input_mask)

#       # 로스 구함
#       logits = outputs[0]

#       # CPU로 데이터 이동
#       logits = logits.detach().cpu().numpy()

#       return logits
#   # sentences_re = []
 
#   # print('리뷰를 입력해 주세요. : ')
#   # review = input()
#   # print('---------------------')
#   logits = test_sentences([request.GET.get('re')])
#   # print(logits)
#   # print(np.argmax(logits))
#   if np.argmax(logits) == 0 :
#       # print(review)
#       # print("⭐")
#       # print('-----------------------------------------------------------------------------------------------')
#       context2 = {'star':"⭐"}
#       return render(request,'predict.html',context2)
#       # sentences_re.append(1)
#   elif np.argmax(logits) == 1 :
#       # print(i)
#       # print("⭐⭐")
#       # print('-----------------------------------------------------------------------------------------------')
#       context2 = {'star':"⭐⭐"}
#       return render(request,'predict.html',context2)
#       # sentences_re.append(2)
#   elif np.argmax(logits) == 2 :
#       # print(i)
#       print("⭐⭐⭐")
#       print('-----------------------------------------------------------------------------------------------')
#       context2 = {'star':"⭐⭐⭐"}
#       return render(request,'predict.html',context2)
#       # sentences_re.append(3)
#   elif np.argmax(logits) == 3 :
#       # print(i)
#       # print("⭐⭐⭐⭐")
#       # print('-----------------------------------------------------------------------------------------------')
#       context2 = {'star':"⭐⭐⭐⭐"}
#       return render(request,'predict.html',context2)
#       # sentences_re.append(4)
#   else :
#       # print(i)
#       # print("⭐⭐⭐⭐⭐")
#       # print('-----------------------------------------------------------------------------------------------')
#       context2 = {'star':"⭐⭐⭐⭐⭐"}
#       return render(request,'predict.html',context2)
#       # sentences_re.append(5)


# def test(request):
#     return render(request,'tem.html')