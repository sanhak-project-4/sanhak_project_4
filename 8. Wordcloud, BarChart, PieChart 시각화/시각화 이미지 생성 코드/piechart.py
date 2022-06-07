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

v_sum = sum(values)
v_a = []
for i in values:
    q = round(i/v_sum*100, 1)
    v_a.append(q)

score = ['1 Star','2 Star','3 Star','4 Star','5 Star   Unit : %']
colors = ['#EFA2A1', '#E0BAAA', '#C9D8B5', '#BAEBBA', '#B3F5BE']
width_num = 0.4
#count = '125'
count = [v_sum]
fig, ax = plt.subplots()
ax.axis('equal')
plt.rcParams["figure.figsize"] = (50, 30)
plt.rcParams["font.size"] = 14

pie_outside, _ = ax.pie(v_a,radius=1.3,labeldistance=0.8,colors = colors, pctdistance=0.85,labels=v_a)
plt.setp(pie_outside,width=width_num, edgecolor='white')
pie_inside, plt_labels, junk = ax.pie(count, radius=(1.3 - width_num),labeldistance=0.75,autopct='                            Total count \n                           {}'.format(count[0]),colors=['white'])
plt.setp(pie_inside,width=width_num, edgecolor='white') 
plt.title("New Star \n ", fontsize=20)
#########################################################
plt.legend(score,loc='lower center', bbox_to_anchor=(0.35, -0.3, 0.3, 1),ncol=3)
#########################################################
plt.savefig('star_sofa_new_pie2.png',bbox_inches='tight')
plt.close()