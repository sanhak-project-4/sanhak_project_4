# sanhak_project_4
한양대_머신러닝_산학프로젝트_4조

https://yoon990.tistory.com/38



### 1. 크롤링.ipynb
  : 네이버 리뷰페이지 크롤링 코드(100페이지까지)
  
  
  
### 2. 패딩 근거.ipynb
  : 패딩 300자 이하로 정한 근거
  
  
  
### 3. 전처리1_공백제거_정규화_띄어쓰기_오탈자
  : 공백제거, 정규화, 띄어쓰기, 오탈자 수정 코드
  
  
  
### 4. 전처리2_토큰화_불용어제거_워드클라우드
  : 토큰화, 불용어제거 후 워드클라우드 생성 코드
  
  
  
### 5. 감성사전 구축 및 텍스트리뷰 수치화(총별점)
  - 감성사전 생성 코드 *감성사전생성_0425.ipynb
  - 감성사전 JSON 파일 *감성사전_ver_최종2022-04-25_않다 불포함.json
  - 텍스트리뷰 수치화 코드 *감성사전으로_점수측정_총점.txt

    
    
### 6. 감성분석 모델링
  - 이진분류(긍부정)
   : BERT, KoBERT, CNN+BiLSTM+Attention, GRU+Attention, BiLSTM+Attetion 이진분류모델
  - 다중분류(5점척도)
   : BERT, KoBERT, CNN+BiLSTM+Attention, GRU+Attention, BiLSTM+Attetion 다중분류모델
    + 가중치 저장된 BERT 파일[BERT_trained.pt]    
    + 직접 data를 input해서 sample data로 사용할 수 있는 predict 파일[BERT_input(middle_test).ipynb]
    + csv파일 형식을 sample data로 사용할 수 있는 predict 파일[BERT_csv(middle_test).ipynb] 



### 7. 감성사전 구축 및 텍스트리뷰 수치화(세분화된 별점)
  - 카테고리별 감성사전(3,2,1-gram별)
    : '가격', '내구성', '디자인', '서비스' 카테고리별로 1gram, 2gram, 3gram 감성사전 JSON 파일
     *가격사전_1gram.JSON, 가격사전_2gram.JSON, 가격사전_3gram.JSON, 내구성사전_1gram.JSON, 내구성사전_2gram.JSON, 내구성사전_3gram.JSON, 디자인사전_1gram.JSON, 디자인사전_2gram.JSON, 디자인사전_3gram.JSON, 서비스사전_1gram.JSON, 서비스사전_2gram.JSON, 서비스사전_3gram.JSON*
  2) 텍스트리뷰 수치화 코드
     *세분화된 감성사전으로 점수측정.ipynb*



### 8. 시각화_WordCloud, BarChart, PieChart
  1) 시각화 이미지 생성 코드
    : WordCloud 생성 코드, Barchart 생성 코드, PieChart 생성 코드와 mask로 사용되는 bed, closet, desk, sofa, diningtable, livingtable 이미지 파일들 
  2) 시각화 이미지 전체
    : bed, closet, desk, sofa, diningtable, livingtable의 긍/부정 워드클라우드, BarChart, PieChart



### 9. 위의 전 과정 실행 후 Elasticsearch, MariaDB로 저장하는 코드
  [크롤링, 전처리, 별점부여, 시각화 후 Elasticsearch, MariaDB로 저장 전체 코드.py]

### Elasticsearch_document_key
 #### index
  : bed / closet / desk / sofa / diningtable / livingtable
 #### type
  : document
 #### id
  : 1부터 순차적으로 부여
 #### spacing_spell_review
  : 전처리1_띄어쓰기, 오탈자 수정한 리뷰, 기존 별점, 새로운 별점
 #### token_stopword_review
  : 전처리2_토큰화, 불용어처리한 리뷰
 ### image
  : 제품 사진 url

### MariaDB Table
  #### name 
   - columns: items(제품군), name(제품명)
  #### contents
   - columns: name(제품명), image(제품 사진 링크), summary(베스트리뷰), count(리뷰수)
  #### star
   - columns: name(제품명), total(총별점), durability(내구성별점), service(서비스별점), design(디자인별점),   price(가격별점)
  #### visualization
   - columns: name(제품명), wordcloud_negative(부정 워드클라우드), wordcloud_positive(긍정 워드클라우드), star_old(기존 별점 분포 BarChart), star_new(새로운 별점 분포 BarChart), star_new_pie(새로운 별점 분포 PieChart)
