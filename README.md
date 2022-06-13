# sanhak_project_4
한양대_머신러닝_산학프로젝트_4조


### <div align=center>🛠skill</div>
- Language <img src="https://img.shields.io/badge/Python-3776AB?style=plastic&logo=Python&logoColor=white"> 

- OS <img src="https://img.shields.io/badge/Linux-FCC624?style=plastic&logo=Linux&logoColor=white"> <img src="https://img.shields.io/badge/CentOS-262577?style=plastic&logo=CentOS&logoColor=white">

- Environment <img src="https://img.shields.io/badge/Google Colab-F9AB00?style=plastic&logo=Google Colab&logoColor=white"> <img src="https://img.shields.io/badge/Jupyter-F37626?style=plastic&logo=Jupyter&logoColor=white"> <img src="https://img.shields.io/badge/NVIDIA-76B900?style=plastic&logo=NVIDIA&logoColor=white"> <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=plastic&logo=Visual Studio Code&logoColor=white"> <img src="https://img.shields.io/badge/Microsoft Azure-0078D4?style=plastic&logo=Microsoft Azure&logoColor=white"> <img src="https://img.shields.io/badge/VirtualBox-183A61?style=plastic&logo=VirtualBox&logoColor=white">

- Data Ecosystem <img src="https://img.shields.io/badge/Grafana-F46800?style=plastic&logo=Grafana&logoColor=white"> <img src="https://img.shields.io/badge/Prometheus-E6522C?style=plastic&logo=Prometheus&logoColor=white"> <img src="https://img.shields.io/badge/Elasticsearch-005571?style=plastic&logo=Elasticsearch&logoColor=white"> <img src="https://img.shields.io/badge/Logstash-005571?style=plastic&logo=Logstash&logoColor=white"> <img src="https://img.shields.io/badge/MariaDB-003545?style=plastic&logo=MariaDB&logoColor=white">

- Framework <img src="https://img.shields.io/badge/Keras-D00000?style=plastic&logo=Keras&logoColor=white"> <img src="https://img.shields.io/badge/Django-092E20?style=plastic&logo=Django&logoColor=white"> 

- Library <img src="https://img.shields.io/badge/scikit learn-F7931E?style=plastic&logo=scikit learn&logoColor=white">  <img src="https://img.shields.io/badge/Selenium-43B02A?style=plastic&logo=Selenium&logoColor=white"> <img src="https://img.shields.io/badge/NumPy-013243?style=plastic&logo=NumPy&logoColor=white"> <img src="https://img.shields.io/badge/pandas-150458?style=plastic&logo=pandas&logoColor=white"> <br/>

##### &nbsp; ➕ 자연어 처리 Package : Transformers(자연어처리 모델), PyKoSpacing(띄어쓰기 수정), py-hanspell(맞춤법 검사기), KoNLPy_Okt(형태소 분석기), Soynlp_normalizer(정규화) 
<br/>
<br/>


### 📋 프로젝트 개발 환경_prerequsite
&nbsp; : 프로젝트에 필요한 모듈, 라이브러리, 프레임워크 등 버전 정보

<br/>

### 📚 raw data(리뷰 개수_긍정 약 1만개, 부정 약 1만개, 총 약 2만개)  
&nbsp; : 침대, 장롱, 식탁, 거실장, 소파, 책상 총 6개 상품군에 대하여 크롤링 <br/>
&nbsp; : 기존 별점 4, 5점을 긍정(10,888개)으로, 기존 별점 1, 2, 3점을 부정(10,421개)으로 분류

<br/>

### 📚 data(리뷰 개수_raw data와 동일)
  - **total_final.csv** <br/>
&nbsp;columns: type(제품명), review(토큰화되지 않은 리뷰_BERT 학습용), star(기존별점), label(기존라벨), new_star(새로운 별점)
  - **total_final(tokenized).csv** <br/>
&nbsp;columns: type(제품명), reviews(토큰화된 리뷰_BERT 외 학습용), label(기존라벨), new_label(tofhdns 라벨), new_star(새로운 별점)
  - **total_tokenized_review.csv** <br/>
&nbsp;: 토큰화된 리뷰 모음 (seperator: ',')
  - **stopwords.txt** <br/>
&nbsp;: 불용어 사전
  - **sentiment_dictionary_total.json** <br/>
&nbsp;: 총별점 라벨링용 감성사전 JSON 파일
  - 📁 **카테고리별 감성사전(3,2,1-gram 별)** <br/>
&nbsp;  : '가격', '내구성', '디자인', '서비스' 카테고리로 세분화된 별점 예측용 1gram, 2gram, 3gram 감성사전 JSON 파일<br/>
&nbsp;&nbsp;- sentiment_dictionary_price_3gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_price_2gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_price_1gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_durability_3gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_durability_2gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_durability_1gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_design_3gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_design_2gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_design_1gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_service_3gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_service_2gram.json<br/>
&nbsp;&nbsp;- sentiment_dictionary_service_1gram.json<br/>
  - **Hancom Gothic Bold.ttf** <br/>
&nbsp;  : 워드클라우드 글씨체



<br/>

### 📚 test용 sample data(리뷰 개수_180개)
  - **test_data.csv** <br/>
&nbsp;columns: name(제품명), review(리뷰 원본), star(기존 별점), 긍(1)/부정(0)(predict용으로 조원 5인이 직접 읽은 후 합의 하에 부여한 라벨)
  - **test_data.xlsx** <br/>
&nbsp;: 위 csv 파일과 내용 동일   
   
<br/>

#### 📄 1. 크롤링.ipynb
&nbsp;   : 네이버 리뷰페이지 크롤링 코드(100페이지까지)
  
  
<br/>  

#### 📄 2. 패딩_근거.ipynb
&nbsp;   : 패딩 300자 이하로 정한 근거
  
  
<br/> 

#### 📄 3. 전처리1_공백제거_정규화_띄어쓰기_오탈자.ipynb
&nbsp;   : 공백제거, 정규화, 띄어쓰기, 오탈자 수정 코드
  
  
<br/>  

#### 📄 4. 전처리2_토큰화_불용어제거_워드클라우드.ipynb
&nbsp;   : 토큰화, 불용어제거 후 워드클라우드 생성 코드<br/>
  
  
<br/>  

#### 📁 5. 감성사전 구축 및 텍스트리뷰 수치화(총별점)
  - 감성사전_생성.ipynb<br/> 
&nbsp;: 감성사전 생성 코드 
  - 감성사전으로_텍스트리뷰_수치화(총별점).py<br/>
&nbsp;: 텍스트리뷰 점수측정 코드 

    
<br/>   

#### 📁 6. 감성분석 모델링
  - 📂 이진분류(긍부정)<br/>
&nbsp;  : BERT, KoBERT, CNN+BiLSTM+Attention, GRU+Attention, BiLSTM+Attetion 이진분류모델
  - 📂 다중분류(5점척도)<br/>
&nbsp;  : BERT, CNN+BiLSTM+Attention 다중분류모델<br/>
&nbsp;&nbsp;- BERT_trained.pt<br/> 
&nbsp;&nbsp;&nbsp;&nbsp;: 가중치 저장된 BERT 파일<br/>
&nbsp;&nbsp;- BERT_input(middle_test).ipynb<br/>
&nbsp;&nbsp;&nbsp;&nbsp;: 직접 data를 input해서 sample data로 사용할 수 있는 predict 파일<br/> 
&nbsp;&nbsp;- BERT_csv(middle_test).ipynb<br/> 
&nbsp;&nbsp;&nbsp;&nbsp;: csv파일 형식을 sample data로 사용할 수 있는 predict 파일 <br/>


<br/>

#### 📄 7. 세분화된_감성사전으로_텍스트리뷰_수치화(세분화된 별점).ipynb <br/> 
&nbsp;   : '가격', '내구성', '디자인', '서비스'로 세분화된 각 사전 기반 텍스트리뷰 수치화 코드
    

<br/>

#### 📁 8. 시각화_WordCloud, BarChart, PieChart <br/>
  - 📂 시각화 이미지 생성 코드 <br/>
&nbsp;  : WordCloud 생성 코드, Barchart 생성 코드, PieChart 생성 코드와 mask로 사용되는 bed, closet, desk, sofa, diningtable, livingtable 이미지 파일들 
  - 📂 시각화 이미지 전체 <br/>
&nbsp;  : bed, closet, desk, sofa, diningtable, livingtable의 긍/부정 워드클라우드, BarChart, PieChart


<br/>

#### 📄 9. 전과정(크롤링_전처리_별점부여_시각화_적재).py <br/>
&nbsp;  : 위의 전 과정(크롤링, 전처리, 별점 부여, 별점분포 시각화) 실행 후 Elasticsearch, MariaDB로 전송하는 코드
 
  
<br/>


#### 📁 10. Django project
  
<br/>

### 🌐 Elasticsearch_document_key
**- index**<br/>
&nbsp;  : bed / closet / desk / sofa / diningtable / livingtable
 
**- type**<br/>
&nbsp;  : document
  
**- id**<br/>
&nbsp;  : 1부터 순차적으로 부여

**- raw_review**<br/>
&nbsp;  : 리뷰 원본

**- spacing_spell_review**<br/>
&nbsp;  : 전처리1_띄어쓰기 및 오탈자 수정한 리뷰, 기존 별점, 새로운 별점
  
**- token_stopword_review**<br/>
&nbsp;  : 전처리2_토큰화 및 불용어처리한 리뷰
  
**- image**<br/>
&nbsp;  : 제품 사진 url
  
<br/>

### 🦈 MariaDB Table

**- name** <br/>
&nbsp;  columns: items(제품군), name(제품명)
   
**- contents**<br/>
&nbsp;  columns: name(제품명), image(제품 사진 링크), summary(리뷰 ), count(리뷰수)

**- star**<br/>
&nbsp;  columns: name(제품명), total(총별점), durability(내구성 별점), service(서비스 별점), design(디자인 별점),   price(가격 별점)

**- visualization**<br/>
&nbsp;  columns: name(제품명), wordcloud_negative(부정 워드클라우드), wordcloud_positive(긍정 워드클라우드), star_old(기존 별점 분포 BarChart), star_new(새로운 별점 분포 BarChart), star_new_pie(새로운 별점 분포 PieChart)

