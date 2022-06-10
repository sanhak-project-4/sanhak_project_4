from matplotlib import font_manager
import re
import pandas as pd
import numpy as np
import urllib.request
from sklearn.model_selection import train_test_split
import time
import csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import konlpy
from konlpy.tag import Okt
from konlpy.utils import pprint
from collections import Counter
from PIL import Image
# 파일과 형태소 분석기 설정
negative = ['전처리 완료한 데이터 리스트']
positive = ['전처리 완료한 데이터 리스트']
okt = Okt()
result_negative = []
result_positive = []

def WordCloud_bed_negative(df):
    for i in negative:
        words = okt.nouns(i)
        for word in words:
            result_negative.append(word)

    words = Counter(result_negative)
    tags = words.most_common(100)

    c = dict(tags)

    img = Image.open('/content/bed.png')
    mask = np.array(img)

    wc = WordCloud(font_path = '/content/malgunbd.ttf', width = 400, height = 400, max_font_size=100, background_color = 'white', mask = mask, colormap = 'gist_heat')
    wc_g = wc.generate_from_frequencies(c)


    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(wc_g)
    plt.show()
    plt.savefig('WordCloud_bed_negative.png',bbox_inches='tight')

WordCloud_bed_negative(negative)


def WordCloud_bed_positive(df):
    for i in positive:
        words = okt.nouns(i)
        for word in words:
            result_positive.append(word)

    words = Counter(result_positive)
    tags = words.most_common(100)

    c = dict(tags)

    img = Image.open('/content/bed.png')
    mask = np.array(img)

    wc = WordCloud(font_path = '/content/malgunbd.ttf', width = 400, height = 400, max_font_size=100, background_color = 'white', mask = mask, colormap = 'winter')
    wc_g = wc.generate_from_frequencies(c)


    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(wc_g)
    plt.show()
    plt.savefig('WordCloud_bed_positive.png',bbox_inches='tight')

WordCloud_bed_positive(positive)