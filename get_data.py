# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import re
# from konlpy.tag import Okt
# import requests
# import urllib.request
# import urllib.error
#
# def hangul_only(s):
#     hangul = re.compile('[ ㄱ-ㅣ가-힣]+')
#     result = hangul.sub('', s)
#     result = hangul.findall(s)
#     return result
#
#
# stop_words = []
# with open("./stopwords.txt", "r") as r:
#     lines = r.readlines()
#     for line in lines:
#         stop_words.append(line.strip())
#
# DRIVER_DIR = 'C:/Users/User/Documents/ai school/chromedriver'
#
# url = 'https://www.instagram.com/explore/'
# driver = webdriver.Chrome(DRIVER_DIR)
# driver.get(url)
# time.sleep(5)
# driver.find_element_by_name("username").send_keys("01099040959")
# driver.find_element_by_name("password").send_keys("09590959")
# driver.find_element_by_xpath("//div/form/div[4]/button/div").submit()
#
# from bs4 import BeautifulSoup
#
# SCROLL_PAUSE_TIME = 10
# reallink = []
# a = 0
# while (a < 200):
#     pageString = driver.page_source
#     bsObj = BeautifulSoup(pageString, "lxml")
#
#     for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
#         title = link1.select('a')[0]
#         real = title.attrs['href']
#         reallink.append(real)
#         title = link1.select('a')[1]
#         real = title.attrs['href']
#         reallink.append(real)
#         title = link1.select('a')[2]
#         real = title.attrs['href']
#         reallink.append(real)
#
#
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     a = a + 1
#     # driver.implicitly_wait(3)
#     # new_height = driver.execute_script("return document.body.scrollHeight")
#     # if new_height == last_height:
#     #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     #     driver.implicitly_wait(5)
#     #     new_height = driver.execute_script("return document.body.scrollHeight")
#     #     if new_height == last_height:
#     #         break
#     #
#     #     else:
#     #         last_height = new_height
#     #         continue
#
# texts = []
# hashtags = []
# texts_final = []
# hashtags_final = []
#
# for i in range(len(reallink)-1):
#     try:
#         webpage = urllib.request.urlopen('https://www.instagram.com/p' + reallink[i]).read()
#         soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')
#     except  urllib.error.HTTPError as e:
#         print(e.reason)
#     except urllib.error.URLError as e:
#         print(e.reason)
#     soup1 = soup.title.find(string=True)
#     soup1 = soup1[soup1.find(':') + 1:]
#     soup1 = soup1.strip()
#     text = [soup1[1:-1]]
#     okt = Okt()
#     okt_morphs = okt.pos(soup1)
#     words = []
#
#     for word, pos in okt_morphs:
#         if word not in stop_words:
#             if pos == 'Noun' or pos == 'Verb' or pos == 'Adverb':
#                 words.append(word)
#
#     texts.append(words)
#
#     hashtag = []
#
#     for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
#         reallink2 = reallink2['content']
#         reallink2 = hangul_only(reallink2)
#         if reallink2 != []:
#             hashtag.append(''.join(reallink2))
#     hashtags.append(hashtag)
#
#
#
# for i in range(len(texts) - 1):
#     if texts[i] != [] and hashtags[i] != []:
#         texts_final.append(texts[i])
#         hashtags_final.append(hashtags[i])
#
# with open("./insta_hashtag.txt", 'a', encoding='utf-8', errors='ignore') as f:
#     for i in range(len(texts_final) - 1):
#         f.write(' '.join(texts_final[i]) + '\t' + ' '.join(hashtags_final[i]) + '\n')
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from konlpy.tag import Okt
import requests
import urllib.request
import urllib.error


def hangul_only(s):
    hangul = re.compile('[ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('', s)
    result = hangul.findall(s)
    return result

def strip_e(st):
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    return RE_EMOJI.sub(r'', st)

stop_words = []
with open("./stopwords.txt", "r") as r:
    lines = r.readlines()
    for line in lines:
        stop_words.append(line.strip())

DRIVER_DIR = 'C:/Users/User/Documents/ai school/chromedriver'

url = 'https://www.instagram.com/explore/tags/일탈'
driver = webdriver.Chrome(DRIVER_DIR)
driver.get(url)
time.sleep(5)
# driver.find_element_by_name("username").send_keys("01099040959")
# driver.find_element_by_name("password").send_keys("09590959")
# driver.find_element_by_xpath("//div/form/div[4]/button/div").submit()

from bs4 import BeautifulSoup


SCROLL_PAUSE_TIME=3
while (True):
    reallink = []
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, "lxml")

    for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
        title = link1.select('a')[0]
        real = title.attrs['href']
        reallink.append(real)
        title = link1.select('a')[1]
        real = title.attrs['href']
        reallink.append(real)
        title = link1.select('a')[2]
        real = title.attrs['href']
        reallink.append(real)

    for i in range(len(reallink)):
        with open("./insta_hashtag.txt", 'a', encoding='utf-8', errors='ignore') as f:
            texts = []
            hashtags = []
            try:
                webpage = urllib.request.urlopen('https://www.instagram.com/p' + reallink[i]).read()
                soup = BeautifulSoup(webpage, "lxml", from_encoding='utf-8')
            except  urllib.error.HTTPError as e:
                print(e.reason)
            except urllib.error.URLError as e:
                print(e.reason)
            soup1 = soup.title.find(string=True)
            soup1 = soup1[soup1.find(':') + 1:]
            soup1 = soup1.strip()
            text = [soup1[1:-1]]
            okt = Okt()
            soup1=strip_e(soup1)
            okt_morphs = okt.pos(soup1)
            words = []

            for word, pos in okt_morphs:
                if word not in stop_words:
                    if pos == 'Noun' or pos == 'Verb' or pos == 'Adverb':
                        words.append(word)

            hashtag = []

            for reallink2 in soup.find_all("meta", attrs={"property": "instapp:hashtags"}):
                reallink2 = reallink2['content']
                reallink2=strip_e(reallink2)
                reallink2 = hangul_only(reallink2)
                if reallink2 != []:
                    hashtag.append(''.join(reallink2))
            print(words)
            print(hashtag)
            if words != [] and hashtag != []:
                print(words)
                print(hashtag)
                f.write(' '.join(words) + '\t' + ' '.join(hashtag) + '\n')

        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            else:
                last_height = new_height
                continue
