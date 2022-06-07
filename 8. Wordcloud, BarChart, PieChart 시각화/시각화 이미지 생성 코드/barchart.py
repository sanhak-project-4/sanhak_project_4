#우리별점

from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import numpy as np

def searchAPI():
    es = Elasticsearch('http://172.20.40.52:9200')
    res = es.search(
        index='sofa',
        body={ "query":
            {"match_all":  {   }}})
    return res
elastic = searchAPI()
stars = elastic['hits']['hits'][0]['_source']['spacing_spell_review']  # 보고 싶은 키값 ex) spacing_spell_review

star = []
for i in stars:
  a = len(i[2])
  star.append(a)

a = star.count(1)
b = star.count(2)
c = star.count(3)
d = star.count(4)
e = star.count(5)
values = [a,b,c,d,e]
print(len(star))

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
plt.ylim([0,575])

plt.savefig('star_sofa_new2.png',bbox_inches='tight')
plt.close()


#기존별점

from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import numpy as np

def searchAPI():
    es = Elasticsearch('http://172.20.40.52:9200')
    res = es.search(
        index='closet',
        body={ "query":
            {"match_all":  {   }}})
    return res
elastic = searchAPI()
stars = elastic['hits']['hits'][0]['_source']['spacing_spell_review']  # 보고 싶은 키값 ex) spacing_spell_review

star = []
for i in stars:
  a = len(i[1])
  star.append(a)

a = star.count(1)
b = star.count(2)
c = star.count(3)
d = star.count(4)
e = star.count(5)
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
plt.ylim([0,575])
plt.savefig('star_closet_old2.png',bbox_inches='tight')
plt.close()

