import re
import time
import unicodedata
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from konlpy.tag import Okt

def show_plot(points):
    plt.figure()
    fig, ax = plt.subplots()
    loc = ticker.MultipleLocator(base=0.2)  # put ticks at regular intervals
    ax.yaxis.set_major_locator(loc)
    plt.plot(points)


def as_minutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def time_since(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (as_minutes(s), as_minutes(rs))


def validate_language(l):
    p = './data/{}.txt'.format(l)
    p = os.path.abspath(p)
    print(p)

    # if not os.path.exists(p):
    #     url = 'http://www.manythings.org/anki/'
    #     print("{}.txt does not exist in the data directory. Please go to '{}' and download the data set.".format(l, url))
    #     exit(1)


def validate_language_params(l):
    is_missing = (not os.path.exists('./data/attention_params_{}'.format(l))
                  or not os.path.exists('./checkpoint/decoder_params_{}'.format(l))
                  or not os.path.exists('./checkpoint/encoder_params_{}'.format(l)))

    if is_missing:
        print(
            "Model params for language '{}' do not exist in the data directory. Please train a new model for this language.".format(
                l))
        exit(1)
def hangul_only(s):
    hangul = re.compile('[ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', s)
    result = hangul.findall(s)
    return result
        
        
def preprocessing_korean(inputs):
    stop_words = []
    with open("./data/stopwords.txt", "r",encoding="utf-8") as r:
      lines = r.readlines()
      for line in lines:
          stop_words.append(line.strip())

    okt=Okt()
    words=[]
    inputs=hangul_only(inputs)
    inputs = ' '.join(inputs)
    okt_morphs =okt.pos(inputs)
    for word, pos in okt_morphs:
        if word not in stop_words:
            if pos=='Noun' :
                words.append(word)
    return words

