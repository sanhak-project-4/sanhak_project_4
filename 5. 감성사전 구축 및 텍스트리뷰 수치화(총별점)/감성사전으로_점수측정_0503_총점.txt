# 우리 감성사전으로 점수 측정

import json
import csv

class KnuSL():

    def data_list(wordname):
        
        # 감성 사전 불러오기
        with open('감성사전_ver_최종2022-04-25_않다 불포함 (1).json',encoding='utf-8', mode='r') as f:
            data = json.load(f)
        result = [0,0]
        
        # 2-gram 카운터 초기화
        j= 0
        
        # 2-gram과 1-gram 계산 - 2-gram에 포함되면 1-gram은 계산하지 않고 다음으로 넘어감 
        for i in range(0, len(data)):
            if j < 125:
                if (data[i]['word_root'] in wordname):
                    result.pop()
                    result.pop()
                    result.append(data[i]['word_root'])
                    result.append(data[i]['polarity'])	
   
                    j += 1
                    break
                else:
                    j += 1
            elif j >= 125:
                if (data[i]['word_root'] in wordname):                    
                    result[1] += int(data[i]['polarity'])
                    j += 1
                else:
                    j += 1
        try:
            r_word = result[0]
            s_word = result[1]
        except:
            pass
        return s_word
n = 0
ksl = KnuSL    

# 토큰화 리뷰 데이터 불러오기
f = open('total_불용어제거_0428.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
점수리스트 = []

# 토큰화한 리뷰 데이터를 하나의 리스트로 결합
for i in rdr:
    score = 0
    
    # ,를 기준으로 결합
    r = ','.join(i).replace(',',' ')
    word = r.split()
    z = zip(word,word[1:])

    if len(word) < 2:
        a = ksl.data_list(word)
        try:
            score += int(a)
        except:
            pass
    else:
        for j in z:
            two_gram_word = ' '.join(j)
            
            # 점수를 측정 후 scroe 변수에 넣어줌
            a = ksl.data_list(two_gram_word)
            try:
                score += int(a)
            except:
                pass
    print(score)
    n +=1   
    print('---------------------------------------------------------------------')
    print(n)
    
    # 점수리스트에 추가
    점수리스트.append(score)