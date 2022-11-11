#!/usr/bin/env python
# coding: utf-8

# In[18]:


'''221110 ver1.30 / chromedriver 경로 = 설정안함(설정 시, 서버 내 1. 크롬 버전 확인, 2. linux용 크롬드라이버 설치 필요)

              수정) 1. db 디폴트/크롤링 2중 저장
              2. 기타 코드 수정
              3. 오류 문구 수정
              4. db - 테마, 메모 컬럼 추가
                     '''

import requests
import re
import pymysql
import json
import urllib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import urllib.request
import sys
from urllib import parse
import http.client
http.client._MAXHEADERS = 1000
from user_agent import generate_user_agent, generate_navigator
import datetime
from collections import Counter, OrderedDict
import random 

# data - mysql DB 접속 #라니 오픈
try:
    db = pymysql.connect(host="moum3.cjk00gposwcb.ap-northeast-2.rds.amazonaws.com", user='admin', password='fnucni1234!', db='moum', charset='utf8mb4')
    cur = db.cursor()

except Exception as e:
    print("디비 접속 에러...")

# 리스트 공간

Type = []
Category_in = []
Distributor = []
Publisher = []
Category_out = []
Logo_image = []
Channel_logo = []
Thumbnail_image = []
User_url = []
Title = []
Maker = []
Date = []
Summary = []
crawl_Content = []
Emotion_cnt = []
Comm_cnt = []
Description = []
Comment = []
Tag = []
View_cnt = []
Duration = []
Lower_price = []
Lower_mall = []
Lower_price_card = []
Lower_mall_card = []
Star_cnt = []
Review_cnt = []
Review_content = []
Dscnt_rate = []
Origin_price = []
Dlvry_price = []
Dlvry_date = []
Model_no = []
Color = []
Location = []
Title_searched = []
Lower_price_searched = []
Lower_mall_searched = []
Lower_url_searched = []

dt_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
createdAt = dt_kst
updatedAt = dt_kst

# # 라니 오픈
# # https://wikidocs.net/16049 참고
# # 파이썬 실행시 파라미터로 url 받도록 수정
User_url = sys.argv[1]
UserId = sys.argv[2]
# Mymemo = sys.argv[3]
# MyThema = sys.argv[4]
Mymemo = ['메모 작성 가능!']
MyThema = ['테마 선택 가능!']


start = time.time()  # 시작 시간 저장

# # 제이 오픈, 라니 클로즈
# UserId = None
# User_url = input("???")

#Title_key
try:
    User_url = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\-@\.&+#:\/?=_]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+', User_url)[0]
    print('포맷체크 완료, ', User_url)
except:
    print('포맷체크 실패, User_url 수정(https://www. 삭제 후 추가)')
    User_url = re.sub(r'http[s]?://|www.', '', User_url)
    User_url = 'https://www.' + User_url
    print('포맷수정된 User_url?, ', User_url)
try:
    Title_key_default_re = re.compile('(?<=\/\/)(.*?)(?=\/)')
    Title_key = Title_key_default_re.findall(User_url)[0]
except:
    Title_key = User_url
Title.append(Title_key)    

#Thumbnail_image
Thumbnail_image_key = 'https://lh3.googleusercontent.com/drive-viewer/AJc5JmQtu9w8WEBCv2de0MiHFyUdDp8Lk9sGAkHTl_b0d0bMbJzfU0wriDr9WGWLNE_hcoR8-USSsvA=w1920-h902' #라니(서버)
Thumbnail_image.append(Thumbnail_image_key)

#Distributor
try:
    User_url_domain_re = re.compile('https?://([A-Za-z_0-9.-]+).*')
    User_url_domain = User_url_domain_re.findall(User_url)[0]
    User_url_domain_list = re.split('\.|/|\?|&|=', User_url_domain)

    User_url_delete_keywords = ['guide', 'app', 'show', 'https:', 'or', 'www', 'co', 'kr', 'onelink','page','link', 'www', 
                                'se','io','in', 'tv','subium','go','net','me','m','com','store', 'place','map','brand', 'team',
                               'toastoven', 'dn', 'au', 'org', 're']
    
    User_url_domain_list = list((Counter(User_url_domain_list) - Counter(User_url_delete_keywords)).elements())
    Distributor_key = User_url_domain_list[-1]
except:
    Distributor_key = "해당 링크에서 직접 보기"
Distributor.append(Distributor_key)

#Category_in
# Keyword 데이터 호출 # 라니 파일 주고 서버에 저장 후 서버 경로 입력
#제이 경로
# with open('C:/Users/FNUCNI/Desktop/python_crawling_ver/keyword/221109_keyword.json', 'r', encoding='utf-8-sig') as json_file:
#     keyword_data = json.load(json_file)
#토니 경로
# with open('C:/Users\FNUCNI\Desktop\python/221109_keyword.json', 'r', encoding='utf-8-sig') as json_file:
#     keyword_data = json.load(json_file)
# #라니 경로
with open('/home/ec2-user/MoEum2/nodebird/221109_keyword.json', 'r', encoding='utf-8-sig') as json_file:
    keyword_data = json.load(json_file)

Category_keyword_list = ['shopping', 'blog', 'sns', 'video', 'second', 'cafe', 'news', 'images', 'enter', 'reading', 'map']
for Category_keyword_keyword in Category_keyword_list:
    globals()["Category_in_keyword_list_{}".format(Category_keyword_keyword)] = keyword_data['Category_keyword'][Category_keyword_keyword]['Kor'] + keyword_data['Category_keyword'][Category_keyword_keyword]['Eng']

Category_in_keyword_list_all = [Category_in_keyword_list_cafe, Category_in_keyword_list_news, 
                                Category_in_keyword_list_shopping, Category_in_keyword_list_blog, Category_in_keyword_list_sns, 
                                Category_in_keyword_list_video, Category_in_keyword_list_second, Category_in_keyword_list_images,
                                Category_in_keyword_list_enter, Category_in_keyword_list_map, Category_in_keyword_list_reading]

Category_in_keyword_dict = {'image' : Category_in_keyword_list_images, 'news' : Category_in_keyword_list_news, 
                            'cafe' : Category_in_keyword_list_cafe, 'second' : Category_in_keyword_list_second, 
                            'blog' : Category_in_keyword_list_blog, 'shopping' : Category_in_keyword_list_shopping, 
                            'sns' : Category_in_keyword_list_sns, 'video' : Category_in_keyword_list_video,
                            'enter' : Category_in_keyword_list_enter, 'map' : Category_in_keyword_list_map,
                           'reading' : Category_in_keyword_list_reading}

#참고: Category_in_keyword_dict 의 vlaues 값 중복 시 마지막 하나만 표현(dict 고유의 성격), 따라서 key값이 마지막것으로 표현됨

Category_in_keyword_match_list_cnt_dict = dict()
User_url_list = re.split('\.|/|\?|&|=', User_url)

for Category_in_keyword_list_all_i in Category_in_keyword_list_all:
    Category_in_keyword_match_list = list(set(User_url_list).intersection(Category_in_keyword_list_all_i))
    Category_in_keyword_match_list_cnt = len(Category_in_keyword_match_list)
    Category_in_keyword_match_list_cnt_dict[Category_in_keyword_match_list_cnt] = Category_in_keyword_list_all_i
if max(Category_in_keyword_match_list_cnt_dict.keys()) == 0:
    Category_in_key = "해당 링크에서 직접 보기"
else:
    Category_in_keyword_match_list_cnt_dict_keys_max_values = Category_in_keyword_match_list_cnt_dict[max(Category_in_keyword_match_list_cnt_dict.keys())]

    for key, value in Category_in_keyword_dict.items():
        if value == Category_in_keyword_match_list_cnt_dict_keys_max_values:
            Category_in_key = key
Category_in.append(Category_in_key)

#Type

if Category_in_key in ['news', 'cafe', 'blog', 'sns']:
    Type_key = "글"

elif Category_in_key in ['shopping', 'second']:
    Type_key = "위시"

elif Category_in_key in ['video', 'enter', 'reading']:
    Type_key = "동영상" 

# elif Category_in_key in ['sns', 'image']:
#     Type_key = "이미지"

#     # jpg 등 이미지 확장자가 url에 포함된 경우 이를 이미지로 분류
# elif any(Category_in_keyword_list_image in User_url for Category_in_keyword_list_image in Category_in_keyword_list_images) == True:
#     Type_key = "이미지"

elif Category_in_key in ['map']:
    Type_key = "지도"
    
else:
    Type_key = "기타" #enter를 일단 기타로. image = 기타

Type.append(Type_key)

# default db input

# all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched
all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt, Mymemo, MyThema

for list_one in all_list:
    if len(list_one) == 0:
        list_one.append("--")

# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched)
all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt, Mymemo, MyThema)

sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt, Mymemo, MyThema) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

cur.execute(sql, all_list_tuple)
db.commit()
print('Title_key: ', Title_key, " / Distributor_key: ", Distributor_key, " / Category_in_key: ", Category_in_key, " / Type_key: ", Type_key)
print("default db commit 완료")

#설명 1번

#url accessibility check

#개인 헤더값
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
#FB 헤더값
# headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)', 'Referer': 'https://www.naver.com/'}

#url format check
try:
    User_url = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\-@\.&+#:\/?=_]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+', User_url)[0]
    print('포맷체크 완료, ', User_url)
except:
    print('포맷체크 실패, User_url 수정(https://www. 삭제 후 추가)')
    User_url = re.sub(r'http[s]?://|www.', '', User_url)
    User_url = 'https://www.' + User_url
    print('포맷수정된 User_url?, ', User_url)

#header값 설정
try:
    res = requests.get(User_url, timeout=5, headers = headers) 
    print('facebook 헤더로 접속 완료')
except:
    try:
        print("개인 UA 헤더 설정") 
        def headers_random_list():
            headers_verified_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
                                     'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                                     'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 KAKAOTALK 9.9.7',
                                     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
                                     'Mozilla/5.0 (Linux; Android 12; SM-F711N Build/SP2A.220305.013; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.136 Mobile Safari/537.36;KAKAOTALK 2409960'
                                ]
            headers_random = random.choices(headers_verified_list)[0]
            global headers
            headers = {'User-Agent': headers_random}
            print("headers_verified_list 적용, ", headers)
            return
        headers_random_list()
        res = requests.get(User_url, timeout=5, headers = headers) 
        print("헤더값 변경 완료 ", res.status_code)
    except:
        try:
            headers = {'user-agent': generate_user_agent(device_type='smartphone')}
            print("헤더값 fb -> 랜덤 변경 시도")
            res = requests.get(User_url, timeout=5, headers = headers) 
            print("헤더값 fb -> 랜덤 변경, 접속 완료!")
        except:#headers = 랜덤으로도 접속 불가
            print("접속 불가")
            User_url = User_url        

print("헤더 접속 소요 시간 :", time.time() - start)  

#redirection 요소 파악
# Naver mobile url 임의 변경

if 'msearch' in User_url:
    User_url = User_url.replace("https://msearch", "https://search")
    res = requests.get(User_url, headers=headers) 

# url redirection 잡기

if 'skyscanner' not in User_url: 
    try:
        with urllib.request.urlopen(User_url, timeout = 3) as response:
            User_url_red = response.geturl()
            if 'no-access' in User_url_red:
                User_url = User_url
            else:
                User_url = User_url_red
                res = requests.get(User_url, timeout=2, headers = headers) 
            print("Redirection된 URL은, ", User_url)        
    except:    
        User_url = User_url
        print("No Redirection된 URL은, ", User_url) 

# naver 앱 url(shorten and redirection and decode)
if 'link.naver.com' in User_url:
    try:
        User_url_decoded = parse.unquote(User_url)
        User_url_decoded_re = re.compile('(?<=bridge\?url\=)(.*?)(?=\&dst)')
        User_url_decoded_red = User_url_decoded_re.findall(User_url_decoded)[0]
        User_url = User_url_decoded_red
        res = requests.get(User_url, headers=headers) 
        print("link.naver의 redirection은", User_url)
    except:
        User_url = User_url
        print("No link.naver의 redirection은 URL은, ", User_url) 
               
#네이버 부동산 url 수정 (complex의 경우 newMobile 들어가면 500에러)
if 'land.naver' in User_url:
    if 'article' in User_url:
        User_url = User_url + '?newMobile'
        print('수정된 네이버 부동산 url? ', User_url)
        res = requests.get(User_url, headers=headers) 
    else:
        User_url = User_url

# meta og:url redirection check
if 'hsGateway' in User_url or 'cafe.daum' in User_url or '//g.co' in User_url:
    print('meta og:url 값 확인')
    try:
        soup = BeautifulSoup(res.content, 'html.parser')
        meta_user_url = soup.select_one('meta[property="og:url"]')['content']
        print("og:url은? ", meta_user_url)
    except:
        meta_user_url = User_url

    if len(meta_user_url) > 1:
        try:
            User_url = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:\/?=_]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+', meta_user_url)[0]
            res = requests.get(User_url, headers=headers) 
        except:
            User_url = User_url

if 'balaan' in User_url:
    soup = BeautifulSoup(res.content, 'html.parser')
    User_url_re = re.compile('(?<=replace).+')
    add_url = User_url_re.findall(str(soup))[0].strip("\(\)\" ")
    if '.php' in add_url:
        User_url = 'https://www.balaan.co.kr' + add_url
        res = requests.get(User_url, headers=headers) 
    else:
        User_url = User_url
        
    print("balaan User_url은?", User_url)

if 'a.co/' in User_url:   
    soup = BeautifulSoup(res.content, 'html.parser')
    try:
        User_url = 'https://www.amazon.com/' + str(soup.select_one('input[name="amzn-r"]')['value'])
        res = requests.get(User_url, headers=headers) 
    except:
        try:
            User_url = soup.select_one('meta[property="og:url"]')['content']
            res = requests.get(User_url, headers=headers) 
        except:
            User_url = User_url
    print("amazon user_url", User_url)
        
# url split

User_url_list = re.split('\.|/|\?|&|=', User_url)
print("User_url_list는 ", User_url_list)

# DIstributor 키워드가 2개 이상 들어간 경우를 대비, 0~6번째까지 추출하여 Dstributor_key 와 매칭

User_url_list_Distributor = User_url_list[0:7]
print("User_url_list_Distributor는 ", User_url_list_Distributor)

# 설명 2번
# Keyword 데이터 호출 # 라니 파일 주고 서버에 저장 후 서버 경로 입력
#제이 경로
# with open('C:/Users/FNUCNI/Desktop/python_crawling_ver/keyword/221109_keyword.json', 'r', encoding='utf-8-sig') as json_file:
#     keyword_data = json.load(json_file)
#토니 경로
# with open('C:/Users\FNUCNI\Desktop\python/21109_keyword.json', 'r', encoding='utf-8-sig') as json_file:
#     keyword_data = json.load(json_file)
# #라니 경로
with open('/home/ec2-user/MoEum2/nodebird/221109_keyword.json', 'r', encoding='utf-8-sig') as json_file:
    keyword_data = json.load(json_file)

# url - Distributor_keyword list match

# soup 정의 설정
# ua = UserAgent(use_cache_server=True)
try:
    soup = BeautifulSoup(res.content, 'html.parser')
    personal_headers_keywords = ['nike', 'blog.naver', '11st', 'musinsaapp']
    if len(soup.text.replace("\n","").replace(" ","")) < 150 or any(personal_headers_keyword in User_url for personal_headers_keyword in personal_headers_keywords) == True:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        print('헤더 개인으로 변경')
        res = requests.get(User_url, headers=headers) 
        soup = BeautifulSoup(res.content, 'html.parser')
except:
    pass        
#221019 Distributor 로직 추가
try:
    User_url_domain_re = re.compile('https?://([A-Za-z_0-9.-]+).*')
    User_url_domain = User_url_domain_re.findall(User_url)[0]
    User_url_domain_list = re.split('\.|/|\?|&|=', User_url_domain)

    User_url_delete_keywords = ['guide', 'app', 'show', 'https:', 'or', 'www', 'co', 'kr', 'onelink','page','link', 'www', 
                                'se','io','in', 'tv','subium','go','net','me','m','com','store', 'place','map','brand', 'team',
                               'toastoven', 'dn', 'au', 'org', 're']
    User_url_domain_list = list((Counter(User_url_domain_list) - Counter(User_url_delete_keywords)).elements())
    Distributor_key = User_url_domain_list[-1]
except:
    Distributor_key = "해당 링크에서 직접 보기"
print('Distributor_key는? ', Distributor_key)
#221019 Distributor 로직 추가_끝
                                   
Distributor_key_change_dict = {'mycake':'cake', 'dabangapp':'dabang', 'musinsaapp':'musinsa'}

if Distributor_key in Distributor_key_change_dict.keys():
    Distributor_key =  Distributor_key_change_dict[Distributor_key]    
try:
    liveplayers = ['shoplive','sauceflex', 'sflex']
    for liveplayer in liveplayers:
        if liveplayer in User_url:
            Distributor_in_html_keys = ['musinsa', 'zigzag', 'queenit', 'samsung', 'wconcept', 'wemakeprice', 'hfashionmall', 'kolonmall', 
                                        'thehandsome', 'shinhan', 'thenorthface', 'millie', 'Pulmuone', 'auction', 'lotteimall', 
                                        'hanssem', 'gmarket','elandmall','hnsmall', 'lkebay'] #지마켓 url의 ebay는 라방에만 있는 것으로 확인 
            for Distributor_in_html_key in Distributor_in_html_keys:
                Distributor_in_html = str(soup).find(Distributor_in_html_key)
                if Distributor_in_html > -1:
                    Distributor_key = Distributor_in_html_key
                else:
                    Distributor_in_User_url = str(User_url).find(Distributor_in_html_key)
                    if Distributor_in_User_url > -1:
                        Distributor_key = Distributor_in_html_key
except:
    pass
# 설명 3번

# Category_in_keyword input

#BOW
Category_keyword_list = ['shopping', 'blog', 'sns', 'video', 'second', 'cafe', 'news', 'images', 'enter', 'reading', 'map']
for Category_keyword_keyword in Category_keyword_list:
    globals()["Category_in_keyword_list_{}".format(Category_keyword_keyword)] = keyword_data['Category_keyword'][Category_keyword_keyword]['Kor'] + keyword_data['Category_keyword'][Category_keyword_keyword]['Eng']

try:
    soup_str = str(soup)

    soup_str_list_en = re.split(' |\s|\-|\_|\:|\=|\.|\/', re.sub(r'[^A-Za-z \s\-\_\:\=\.\/]', '', soup_str))
    soup_str_list_en = list(filter(None,soup_str_list_en))
    soup_str_list_ko = re.split(' |\s|\-|\_|\:|\=|\.|\/', re.sub(r'[^가-힣 \s\-\_\:\=\.\/]', '', soup_str))
    soup_str_list_ko = list(filter(None,soup_str_list_ko))
    User_url_list_100 =  User_url_list * 100

    User_url_soup_list = User_url_list_100 + soup_str_list_en + soup_str_list_ko

    Category_in_keyword_shopping_count = 0
    Category_in_keyword_blog_count = 0
    Category_in_keyword_sns_count = 0
    Category_in_keyword_video_count = 0
    Category_in_keyword_second_count = 0
    Category_in_keyword_cafe_count = 0
    Category_in_keyword_news_count = 0
    Category_in_keyword_images_count = 0
    Category_in_keyword_enter_count = 0
    Category_in_keyword_reading_count = 0
    Category_in_keyword_map_count = 0

    for User_url_soup_keyword in User_url_soup_list:
        for Category_in_keyword_shopping in Category_in_keyword_list_shopping:
            if Category_in_keyword_shopping in User_url_soup_keyword:
                Category_in_keyword_shopping_count += 1

        for Category_in_keyword_blog in Category_in_keyword_list_blog:
            if Category_in_keyword_blog in User_url_soup_keyword:
                Category_in_keyword_blog_count += 1

        for Category_in_keyword_sns in Category_in_keyword_list_sns:
            if Category_in_keyword_sns in User_url_soup_keyword:
                Category_in_keyword_sns_count += 1

        for Category_in_keyword_video in Category_in_keyword_list_video:
            if Category_in_keyword_video in User_url_soup_keyword:
                Category_in_keyword_video_count += 1

        for Category_in_keyword_second in Category_in_keyword_list_second:
            if Category_in_keyword_second in User_url_soup_keyword:
                Category_in_keyword_second_count += 1

        for Category_in_keyword_cafe in Category_in_keyword_list_cafe:
            if Category_in_keyword_cafe in User_url_soup_keyword:
                Category_in_keyword_cafe_count += 1

        for Category_in_keyword_news in Category_in_keyword_list_news:
            if Category_in_keyword_news in User_url_soup_keyword:
                Category_in_keyword_news_count += 1

        for Category_in_keyword_images in Category_in_keyword_list_images:
            if Category_in_keyword_images in User_url_soup_keyword:
                Category_in_keyword_images_count += 1

        for Category_in_keyword_enter in Category_in_keyword_list_enter:
            if Category_in_keyword_enter in User_url_soup_keyword:
                Category_in_keyword_enter_count += 1

        for Category_in_keyword_reading in Category_in_keyword_list_reading:
            if Category_in_keyword_reading in User_url_soup_keyword:
                Category_in_keyword_reading_count += 1

        for Category_in_keyword_map in Category_in_keyword_list_map:
            if Category_in_keyword_map in User_url_soup_keyword:
                Category_in_keyword_map_count += 1

    print('Category_in_keyword_shopping_count? ', Category_in_keyword_shopping_count)
    print('Category_in_keyword_blog_count? ', Category_in_keyword_blog_count)
    print('Category_in_keyword_sns_count? ', Category_in_keyword_sns_count)
    print('Category_in_keyword_video_count? ', Category_in_keyword_video_count)
    print('Category_in_keyword_second_count? ', Category_in_keyword_second_count)
    print('Category_in_keyword_cafe_count? ', Category_in_keyword_cafe_count)
    print('Category_in_keyword_news_count? ', Category_in_keyword_news_count)
    print('Category_in_keyword_images_count? ', Category_in_keyword_images_count)
    print('Category_in_keyword_enter_count? ', Category_in_keyword_enter_count)
    print('Category_in_keyword_reading_count? ', Category_in_keyword_reading_count)
    print('Category_in_keyword_map_count? ', Category_in_keyword_map_count)

    Category_in_keyword_count_dict = {'image' : Category_in_keyword_images_count, 'news' : Category_in_keyword_news_count, 
                                'cafe' : Category_in_keyword_cafe_count, 'second' : Category_in_keyword_second_count, 
                                'blog' : Category_in_keyword_blog_count, 'shopping' : Category_in_keyword_shopping_count, 
                                'sns' : Category_in_keyword_sns_count, 'video' : Category_in_keyword_video_count,
                                'enter' : Category_in_keyword_enter_count, 'map' : Category_in_keyword_map_count,
                               'reading' : Category_in_keyword_reading_count}

    Category_in_keyword_count_dict_value_max= max(Category_in_keyword_count_dict.values())

    Category_in_keyword_count_dict_reversed= dict(map(reversed, Category_in_keyword_count_dict.items()))
    Category_in_key = Category_in_keyword_count_dict_reversed[Category_in_keyword_count_dict_value_max]

    if sum(Category_in_keyword_count_dict.values()) == 0:
        Category_in_key = '해당 링크에서 직접 보기'

except:
    print('Category_in_key를 url로만 파악 시도')
    #url - Distributor_keyword list match

    Category_in_keyword_list_all = [Category_in_keyword_list_cafe, Category_in_keyword_list_news, 
                                    Category_in_keyword_list_shopping, Category_in_keyword_list_blog, Category_in_keyword_list_sns, 
                                    Category_in_keyword_list_video, Category_in_keyword_list_second, Category_in_keyword_list_images,
                                    Category_in_keyword_list_enter, Category_in_keyword_list_map, Category_in_keyword_list_reading]

    Category_in_keyword_dict = {'image' : Category_in_keyword_list_images, 'news' : Category_in_keyword_list_news, 
                                'cafe' : Category_in_keyword_list_cafe, 'second' : Category_in_keyword_list_second, 
                                'blog' : Category_in_keyword_list_blog, 'shopping' : Category_in_keyword_list_shopping, 
                                'sns' : Category_in_keyword_list_sns, 'video' : Category_in_keyword_list_video,
                                'enter' : Category_in_keyword_list_enter, 'map' : Category_in_keyword_list_map,
                               'reading' : Category_in_keyword_list_reading}

    #참고: Category_in_keyword_dict 의 vlaues 값 중복 시 마지막 하나만 표현(dict 고유의 성격), 따라서 key값이 마지막것으로 표현됨

    Category_in_keyword_match_list_cnt_dict = dict()

    for Category_in_keyword_list_all_i in Category_in_keyword_list_all:
        Category_in_keyword_match_list = list(set(User_url_list).intersection(Category_in_keyword_list_all_i))
        Category_in_keyword_match_list_cnt = len(Category_in_keyword_match_list)
        Category_in_keyword_match_list_cnt_dict[Category_in_keyword_match_list_cnt] = Category_in_keyword_list_all_i
    if max(Category_in_keyword_match_list_cnt_dict.keys()) == 0:
        Category_in_key = "해당 링크에서 직접 보기"
    else:
        Category_in_keyword_match_list_cnt_dict_keys_max_values = Category_in_keyword_match_list_cnt_dict[max(Category_in_keyword_match_list_cnt_dict.keys())]

        for key, value in Category_in_keyword_dict.items():
            if value == Category_in_keyword_match_list_cnt_dict_keys_max_values:
                Category_in_key = key
                
#Category_in_key 검사                
if Category_in_key == 'map':
    Category_in_keyword_list_map_match_list = list(set(User_url_list).intersection(Category_in_keyword_list_map))
    Category_in_keyword_list_map_match_list_cnt = len(Category_in_keyword_list_map_match_list)
    if Category_in_keyword_list_map_match_list_cnt > 0:
        pass
    else:
        print("Category_in_keyword 탐색 재시도(not map)")
        Category_in_keyword_count_dict_value_list = list(Category_in_keyword_count_dict.values())
        Category_in_keyword_count_dict_value_list.sort()
        Category_in_keyword_count_dict_value_second_count = Category_in_keyword_count_dict_value_list[-2]


        Category_in_keyword_count_dict_reversed= dict(map(reversed, Category_in_keyword_count_dict.items()))
        Category_in_key = Category_in_keyword_count_dict_reversed[Category_in_keyword_count_dict_value_second_count]

Category_in.append(Category_in_key)
  
print("Category_in 리스트 값은 ", Category_in)

#Publisher & Distributor & Category_out 파악

if Category_in_key == 'news' or Distributor_key == '언론사 뷰':
    
#     if Distributor_key == 'naver':

#         #시도 1
#         try:
#             Category_out2 = []
#             Category_out_key1 = soup.select('em.media_end_categorize_item') or soup.select('em.guide_categorization_item')
#             for Category_out_key in Category_out_key1:
#                 Category_out2.append(Category_out_key.text)
#             Category_out = Category_out2
#             print("확인", Category_out)
#         except:
#             Category_out_key = "해당 링크에서 직접 보기"
#             Category_out.append(Category_out_key)

#         #시도2
#         try:
#             Category_out_key1 = soup.select('em.media_end_categorize_item')
#             for Category_out_key in Category_out_key1:
#                 Category_out.append(Category_out_key.text)
#         except:
#             try:
#                 Category_out_key1 = soup.select('em.guide_categorization_item')
#                 for Category_out_key in Category_out_key1:
#                     Category_out.append(Category_out_key.text)

#             except:
#                 Category_out_key = "해당 링크에서 직접 보기"
#                 Category_out.append(Category_out_key)

#         print("Category_out 리스트 값은 ", Category_out)

    try:
        Publisher_key = soup.select_one('meta[property="og:article:author"]')['content']
        if 'daum' in User_url:
            Distributor_key = Publisher_key +' | 다음'
        else:    
            Distributor_key = Publisher_key

    except: 
        Publisher_key = "해당 링크에서 직접 보기"

    Publisher.append(Publisher_key)

    print("Publisher 리스트 값은 ", Publisher_key)
    print("수정된 Distributor_key값은? ", Distributor_key)

else:
    print("Distributor_key값은? ", Distributor_key)

# 설명 4번

# Type 파악
try:
    count_all_shopping_second = Category_in_keyword_shopping_count + Category_in_keyword_second_count
    count_all_blog_sns_cafe_news = Category_in_keyword_blog_count + Category_in_keyword_sns_count + Category_in_keyword_cafe_count + Category_in_keyword_news_count
    count_all_video_enter_reading = Category_in_keyword_video_count + Category_in_keyword_enter_count + Category_in_keyword_reading_count

    count_all = [count_all_shopping_second, count_all_blog_sns_cafe_news, count_all_video_enter_reading, Category_in_keyword_map_count]

    if max(count_all) == 0:
        Type_key = "기타"
    elif max(count_all) == count_all_blog_sns_cafe_news:
        Type_key = '글'
    elif max(count_all) == count_all_shopping_second:
        Type_key = '위시'
    elif max(count_all) == count_all_video_enter_reading:
        Type_key = '동영상'   

    # elif Category_in_key in ['sns', 'image']:
    #     Type_key = "이미지"

    #     # jpg 등 이미지 확장자가 url에 포함된 경우 이를 이미지로 분류
    # elif any(Category_in_keyword_list_image in User_url for Category_in_keyword_list_image in Category_in_keyword_list_images) == True:
    #     Type_key = "이미지"

    elif Category_in_key in ['map'] or max(count_all) == Category_in_keyword_map_count:
        Type_key = "지도"

    else:
        Type_key = "기타" #enter를 일단 기타로. image = 기타
except:
    print("category_count 파악 불가")
    Type_key = "기타"

Type.append(Type_key)
print("Type 리스트 값은 ", Type)

#설명 5번

# 기본 3개(Title, Description, Thumbnail_image) 값 찾기

# 기본 bs4 크롤링 설정: headers 값은 상단에서 변경된 경우, 변경된 상태 그대로 유지
# headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
try:
    cafe24_url = re.match('^(https:\/\/|http:\/\/)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\/(product)\/(.*?)\/[0-9]+\/', User_url)  # cafe24 썸네일 정교하게 잡기 위해 선행
except:
    pass

try:
#     res = requests.get(User_url, timeout=5, headers=headers) #여기 중복 접속 삭제
#     soup = BeautifulSoup(res.content, 'html.parser')
    
    print("응답코드 bs4 일반: ", res.status_code)

    # Title scraping: og, twitter, title tag 텍스트 중 가장 긴 값 or 조건(0자 미만 or 탈출문구) 불만족 시 h1, h2, h3 텍스트 중 가장 긴 값 scraping 
    # 한글이 없을 경우 ((re.search('[가-힣]', Title_key)) == None) 는 해외사이트 고려하여 조건 추가 안함

    try:
        Title_key_og = soup.select_one('meta[property="og:title"]')['content']
    except:
        try:
            Title_key_og = " "
            Title_key_twitter = soup.select_one('meta[name="twitter:title"]')['content']
        except:
            try:
                Title_key_twitter = " "
                Title_key_title = soup.select_one('title').get_text()   
            except:
                Title_key_title = "해당 링크에서 직접 보기"
        else:
            try:
                Title_key_title = soup.select_one('title').get_text()
            except:
                Title_key_title = "해당 링크에서 직접 보기"
    else:
        try:
            Title_key_twitter = soup.select_one('meta[name="twitter:title"]')['content']
        except:
            try:
                Title_key_twitter = " "
                Title_key_title = soup.select_one('title').get_text()
            except:
                Title_key_title = "해당 링크에서 직접 보기"
        else:
            try:
                Title_key_title = soup.select_one('title').get_text()
            except:
                Title_key_title = "해당 링크에서 직접 보기"
    finally:
        
        try: # meta / len / count 로직 
            '''
            현재 가중치
            1. tag(og, twitter, title) 순: 8 / 3 / 1 점
            2. len max 순: 8 / 3 / 1 점
            3. count max 순: 8 / 6 / 4 점
            '''
            # basic 가중치 : og / twitter / title (우선은 이 가중치는 적용하지 않기로 함(9.22)) #적용 필요: 피터팬
            Title_key_basic_dict = {Title_key_og : 0, Title_key_twitter : 0, Title_key_title : 0} # 0점으로 시작한다는 의미
            Title_key_all = [Title_key_og, Title_key_twitter, Title_key_title ]
            Title_key_all = list(dict.fromkeys(Title_key_all)) #중복 제거
            for Title_key_i in Title_key_all:
                if len(re.sub(r'[^A-Za-z0-9가-힣]', '', Title_key_i)) < 2 or Title_key_i.strip('[]') in list(keyword_data['Distributor_keyword'].values()):
                    del(Title_key_basic_dict[Title_key_i])
            print("후보 Title_key는? ", Title_key_all)
            # len 설정
            Title_key_len_dict = {Title_key_og:len(Title_key_og.encode('UTF-8')), Title_key_twitter:len(Title_key_twitter.encode('UTF-8')), Title_key_title:len(Title_key_title.encode('UTF-8'))}
            # count 설정
            Title_key_og_count = str(soup).count(Title_key_og)
            Title_key_twitter_count = str(soup).count(Title_key_twitter)
            Title_key_title_count = str(soup).count(Title_key_title)
            Title_key_count_dict = {Title_key_og:Title_key_og_count, Title_key_twitter:Title_key_twitter_count, Title_key_title:Title_key_title_count}

            # 각 dict.의 value값 및 상응하는 key값 출력
            class Title_key_ordered(Counter, OrderedDict):
                pass
            Title_key_ordered_basic = Title_key_ordered(Title_key_basic_dict)

            Title_key_ordered_basic1 = Title_key_ordered_basic.most_common()[0]

            Title_key_ordered_basic1_list = list(Title_key_ordered_basic1)
            Title_key_ordered_basic1_list[1] = 8
            Title_key_ordered_basic1_changed = tuple(Title_key_ordered_basic1_list)
    #         print('changed', Title_key_ordered_basic1_changed)
            try:
                Title_key_ordered_basic2 = Title_key_ordered_basic.most_common()[1]

                Title_key_ordered_basic2_list = list(Title_key_ordered_basic2)
                Title_key_ordered_basic2_list[1] = 3
                Title_key_ordered_basic2_changed = tuple(Title_key_ordered_basic2_list)
    #             print('changed', Title_key_ordered_basic2_changed)
                try:
                    Title_key_ordered_basic3 = Title_key_ordered_basic.most_common()[2]

                    Title_key_ordered_basic3_list = list(Title_key_ordered_basic3)
                    Title_key_ordered_basic3_list[1] = 1
                    Title_key_ordered_basic3_changed = tuple(Title_key_ordered_basic3_list)
    #                 print('changed', Title_key_ordered_basic3_changed)
                except:
                    pass
            except:
                pass

            Title_key_ordered_len = Title_key_ordered(Title_key_len_dict)

            Title_key_ordered_len1 = Title_key_ordered_len.most_common()[0]

            Title_key_ordered_len1_list = list(Title_key_ordered_len1)
            Title_key_ordered_len1_list[1] = 8
            Title_key_ordered_len1_changed = tuple(Title_key_ordered_len1_list)
    #         print('changed', Title_key_ordered_len1_changed)
            try:
                Title_key_ordered_len2 = Title_key_ordered_len.most_common()[1]

                Title_key_ordered_len2_list = list(Title_key_ordered_len2)
                Title_key_ordered_len2_list[1] = 3
                Title_key_ordered_len2_changed = tuple(Title_key_ordered_len2_list)
    #             print('changed', Title_key_ordered_len2_changed)
                try:
                    Title_key_ordered_len3 = Title_key_ordered_len.most_common()[2]

                    Title_key_ordered_len3_list = list(Title_key_ordered_len3)
                    Title_key_ordered_len3_list[1] = 1
                    Title_key_ordered_len3_changed = tuple(Title_key_ordered_len3_list)
    #                 print('changed', Title_key_ordered_len3_changed)
                except:
                    pass
            except:
                pass

            Title_key_ordered_count = Title_key_ordered(Title_key_count_dict)

            Title_key_ordered_count1 = Title_key_ordered_count.most_common()[0]

            Title_key_ordered_count1_list = list(Title_key_ordered_count1)
            Title_key_ordered_count1_list[1] = 8
            Title_key_ordered_count1_changed = tuple(Title_key_ordered_count1_list)
    #         print('changed', Title_key_ordered_count1_changed)
            try:
                Title_key_ordered_count2 = Title_key_ordered_count.most_common()[1]
                Title_key_ordered_count2_list = list(Title_key_ordered_count2)
                Title_key_ordered_count2_list[1] = 6
                Title_key_ordered_count2_changed = tuple(Title_key_ordered_count2_list)
    #             print('changed', Title_key_ordered_count2_changed)
                try:
                    Title_key_ordered_count3 = Title_key_ordered_count.most_common()[2]
                    Title_key_ordered_count3_list = list(Title_key_ordered_count3)
                    Title_key_ordered_count3_list[1] = 4
                    Title_key_ordered_count3_changed = tuple(Title_key_ordered_count3_list)
    #                 print('changed', Title_key_ordered_count3_changed)
                except:
                    pass
            except:
                pass

            # 튜플 다 모으기
            try:
                Title_key_ordered_all = [Title_key_ordered_basic1_changed, Title_key_ordered_basic2_changed, Title_key_ordered_basic3_changed
                                         , Title_key_ordered_len1_changed, Title_key_ordered_len2_changed, Title_key_ordered_len3_changed
                                         , Title_key_ordered_count1_changed, Title_key_ordered_count2_changed, Title_key_ordered_count3_changed]
            except:
                try:
                    Title_key_ordered_all = [Title_key_ordered_basic1_changed, Title_key_ordered_basic2_changed , Title_key_ordered_len1_changed, 
                                             Title_key_ordered_len2_changed, Title_key_ordered_count1_changed, Title_key_ordered_count2_changed]
                except:
                    Title_key_ordered_all = [Title_key_ordered_basic1_changed, Title_key_ordered_len1_changed, Title_key_ordered_count1_changed]

            # 튜플 합치기

            i = 0
            for i, Title_key_ordered_i in enumerate(Title_key_ordered_all):
                globals()['var'+str(i)] = Counter({Title_key_ordered_i[0] : Title_key_ordered_i[1]})
    #             print(i, globals()['var'+str(i)])
            if i == 9:
                Title_key_dict_final =  var0 + var1 + var2 + var3 + var4 + var5 + var6 + var7 + var8 + var9   
            elif i == 8:
                Title_key_dict_final =  var0 + var1 + var2 + var3 + var4 + var5 + var6 + var7 + var8 
            elif i == 7:
                Title_key_dict_final =  var0 + var1 + var2 + var3 + var4 + var5 + var6 + var7    
            elif i == 6:
                Title_key_dict_final =  var0 + var1 + var2 + var3 + var4 + var5 + var6
            elif i == 5:
                Title_key_dict_final =  var0 + var1 + var2 + var3 + var4 + var5
            elif i == 4:
                Title_key_dict_final =  var0 + var1 + var2 + var3 + var4
            elif i == 3:
                Title_key_dict_final =  var0 + var1 + var2 + var3
            elif i == 2:
                Title_key_dict_final =  var0 + var1 + var2
            elif i == 1:
                Title_key_dict_final =  var0 + var1
            elif i == 0:
                Title_key_dict_final =  var0 
            print("Title_key 후보 점수??", Title_key_dict_final)
            Title_key_dict_final_max_value = max(Title_key_dict_final.values())
            Title_key_dict_final_reversed= dict(map(reversed, Title_key_dict_final.items()))
            Title_key = Title_key_dict_final_reversed[Title_key_dict_final_max_value]
            if len(Title_key) < 2:
                del(Title_key_dict_final[Title_key])
                print('삭제 후 dict', Title_key_dict_final)
                Title_key_dict_final_max_value = max(Title_key_dict_final.values())
                Title_key_dict_final_reversed= dict(map(reversed, Title_key_dict_final.items()))
                Title_key = Title_key_dict_final_reversed[Title_key_dict_final_max_value]
            print("scoring 통한 Title_key??? ", Title_key)
        except:
            try: #단순 len 비교로 Title_key 추출 (구 로직)
                Title_key_dict = {Title_key_og:len(Title_key_og.encode('UTF-8')), Title_key_twitter:len(Title_key_twitter.encode('UTF-8')), Title_key_title:len(Title_key_title.encode('UTF-8'))}
                Title_key_dict_max_values = max(Title_key_dict.values())
                Title_key_dict_reversed= dict(map(reversed, Title_key_dict.items()))
                Title_key = Title_key_dict_reversed[Title_key_dict_max_values]
            except:
                Title_key = "해당 링크에서 직접 보기"
            print("len 통한 Title_key??? ", Title_key)

    def Title_key_h_tag():
        global Title_key  
        try:
            Title_key_h1 = soup.select_one('h1').get_text()
        except:
            try:
                Title_key_h1 = " "
                Title_key_h2 = soup.select_one('h2').get_text()
            except:
                try:
                    Title_key_h2 = " "
                    Title_key_h3 = soup.select_one('h3').get_text()
                except:
                    Title_key_h3 = "해당 링크에서 직접 보기"
        else:
            try:
                Title_key_h2 = soup.select_one('h2').get_text()
            except:
                try:
                    Title_key_h2 = " "
                    Title_key_h3 = soup.select_one('h3').get_text()
                except:
                    Title_key_h3 = "해당 링크에서 직접 보기"
        finally:
            try:
                Title_key = max(Title_key_h1, Title_key_h2, Title_key_h3, key = len)
            except:
                try:
                    Title_key = Title_key
                except:
                    Title_key = "해당 링크에서 직접 보기"
                    
    try:
        if len(Title_key) < 2 or Title_key == "해당 링크에서 직접 보기" or Title_key == Distributor_key or Title_key == keyword_data['Distributor_keyword'][Distributor_key]:
            Title_key_h_tag()
    except:
        if len(Title_key) < 2 or Title_key == "해당 링크에서 직접 보기":
            Title_key_h_tag()    

    if len(Title_key) < 2:
        Title_key = "해당 링크에서 직접 보기"

    # Desc. 우선순위대로 실행    
    try:
        Description_key_og = soup.select_one('meta[property="og:description"]')['content']
    except:
        try:
            Description_key_og = " "
            Description_key_name = soup.select_one('meta[name="description"]')['content']   
        except:
            try:
                Description_key_name = " "
                Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']        
            except:
                Description_key_twitter = "해당 링크에서 직접 보기"
        else:
            try:
                Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']        
            except:
                Description_key_twitter = "해당 링크에서 직접 보기"
    else:
        try:
            Description_key_name = soup.select_one('meta[name="description"]')['content']   
        except:
            try:
                Description_key_name = " "
                Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']
            except:
                Description_key_twitter = "해당 링크에서 직접 보기"
        else:
            try:
                Description_key_twitter = soup.select_one('meta[property="twitter:description"]')['content']
            except:
                Description_key_twitter = "해당 링크에서 직접 보기"
    finally:
        try:
            Description_key = max(Description_key_og, Description_key_name, Description_key_twitter, key = len)
        except:
            Description_key = "해당 링크에서 직접 보기"

    if len(Description_key) < 5 or Description_key == "해당 링크에서 직접 보기":
        try:
            Description_key_h1 = soup.select_one('h1').get_text()
        except:
            try:
                Description_key_h2 = soup.select_one('h2').get_text()
            except:
                Description_key_h2 = "해당 링크에서 직접 보기"
        else:
            try:
                Description_key_h2 = soup.select_one('h2').get_text()
            except:
                Description_key_h2 = "해당 링크에서 직접 보기"
        finally:
            try:
                Description_key = max(Description_key_h1, Description_key_h2, key = len)
            except:
                Description_key = "해당 링크에서 직접 보기"

    if len(Description_key) < 5:
        Description_key = "해당 링크에서 직접 보기"

    # Image
    try:
        Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
    except:
        try:
            Thumbnail_image_key = soup.select_one('meta[name="og:image"]')['content']
        except:
            try:
                Thumbnail_image_key = soup.select_one('meta[property="twitter:image"]')['content']
            except:
                try:
                    Thumbnail_image_key = soup.select_one('meta[name="twitter:image"]')['content']
                except:
                    try:
                        Thumbnail_image_key = soup.select_one('meta[property="op:image"]')['content']
                    except:
                        try:
                            Thumbnail_image_key = soup.select_one('img')['src']        
                        except:
                            Thumbnail_image_key = "해당 링크에서 직접 보기"
except:
    print("기본 3요소 스크래핑 불가")
    Title_key = "해당 링크에서 직접 보기"
    Description_key = "해당 링크에서 직접 보기"
    Thumbnail_image_key = "해당 링크에서 직접 보기"
    
print('기본 bs Title_key 값은, ', Title_key)
print('기본 bs Description_key 값은, ', Description_key)
print('기본 bs Thumbnail_image_key 값은, ', Thumbnail_image_key)    
    
# 개별 site 크롤링 설정

# 크롬드라이버 생성
# 라니 오픈(제이 클로즈)
# chromedriver = 'D:\moEum\nodejs-book-master\ch9\9.5.7_공개컨텐츠 퍼오기\nodebird_web'  # 윈도우 / 로컬
# chromedriver = '/home/ec2-user/MoEum2/nodebird' # AWS EC2 / 서버
# 제이 경로
# chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥
chromedriver = 'C:/Users/FNUCNI/chromedriver.exe' #윈도우

try:
    if 'blog.naver' in User_url:
    #설명 5번_iframe
        #iframe 대비 src_url 설정
        #FB일 경우 SRC 탐색 X
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
#         res = requests.get(User_url, timeout=3, headers=headers) 
#         soup = BeautifulSoup(res.content, 'html.parser')

        src_url = "https://blog.naver.com/" + soup.iframe['src']
        print(src_url)
        res_iframe = requests.get(src_url, timeout=3, headers=headers)
    #     res_noifr.status_code
        soup_iframe = BeautifulSoup(res_iframe.content, "html.parser") 
        try:
            Title_key = soup_iframe.select_one('meta[property="og:title"]')['content']    
        except:
            Title_key = Title_key
        try:
            Description_key = soup_iframe.select_one('meta[property="og:description"]')['content']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = soup_iframe.select_one('meta[property="og:image"]')['content']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    # elif 'music-flo' in User_url:

    #     print("응답코드: ", res.status_code)

    #     #iframe 대비 src_url 설정

    #     src_url = "https://blog.naver.com/" + soup.select_one('iframe["src"]')
    #     res_iframe = requests.get(src_url, headers=headers)
    # #     res_noifr.status_code
    #     soup_iframe = BeautifulSoup(res_iframe.content, "html.parser") 
    #     try:
    #         Title_key = soup_iframe.select_one('meta[property="og:title"]')['content']    
    #     except:
    #         Title_key = "해당 링크에서 직접 보기"
    #     try:
    #         Description_key = soup_iframe.select_one('meta[property="og:description"]')['content']
    #     except:
    #         Description_key = "해당 링크에서 직접 보기"
    #     try:
    #         Thumbnail_image_key = soup_iframe.select_one('meta[property="og:image"]')['content']
    #     except:
    #         Thumbnail_image_key = "해당 링크에서 직접 보기"

    elif 'cafe.naver' in User_url: 
        try:
            headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
#             headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
            res = requests.get(User_url, headers=headers) 
            soup = BeautifulSoup(res.content, 'html.parser')
            try:
                Title_key = soup.select_one('meta[property="og:title"]')['content']
            except:
                Title_key = Title_key
            try:
                Description_key = soup.select_one('meta[property="og:article:author"]')['content']
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
            except:
                Thumbnail_image_key = Thumbnail_image_key
            if 'joonggonara' in User_url: #여기 / 모든 카페를 다 접속시키기에는 차단 부담... 그렇다고 다 정의할순 없고...
                try:
                    if 'm.' in User_url:
                        User_url = User_url.replace('m.cafe.', 'cafe.')
    #                 headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
                    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
                    res = requests.get(User_url, timeout=3, headers=headers) 
                    soup = BeautifulSoup(res.content.decode('euc-kr', 'replace'), 'html.parser')

                    article_no_re = re.compile('[0-9]{4,}.+')
                    article_no = article_no_re.findall(User_url)[0]
                    clubid = soup.select_one('input[name="clubid"]')['value']

                    User_url_api = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/' + str(clubid) + '/articles/' + str(article_no)
                    res_api = requests.get(User_url_api, timeout=3, headers=headers) 
                    soup_api = BeautifulSoup(res_api.text, 'html.parser')
                    dict_result_script_api = json.loads(soup_api.text)
                    try: 
                        Lower_price_key = dict_result_script_api['result']['saleInfo']['price']
                        Lower_price.append(Lower_price_key)
                        print("네이버 중고나라 가격은?, ", Lower_price)
                    except:
                        pass
                except:
                    Lower_price_key = "해당 링크에서 다시 보기" #type == '위시'로 분류되지 않으면 list 내 저장 X
            
        except:
        #설명 5번_api    
            #내부 API
            #header값을 유저로 설정 -> meta값 이외 스크래핑 가능
            if 'm.' in User_url:
                User_url = User_url.replace('m.cafe.', 'cafe.')
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
    #         headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
            res = requests.get(User_url, timeout=3, headers=headers) 
            soup = BeautifulSoup(res.content.decode('euc-kr', 'replace'), 'html.parser')

            article_no_re = re.compile('[0-9]{4,}.+')
            article_no = article_no_re.findall(User_url)[0]
            clubid = soup.select_one('input[name="clubid"]')['value']

            User_url_api = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/' + str(clubid) + '/articles/' + str(article_no)
            res_api = requests.get(User_url_api, timeout=3, headers=headers) 
            soup_api = BeautifulSoup(res_api.text, 'html.parser')
            dict_result_script_api = json.loads(soup_api.text)
            
            #meta값
            try:
                Title_key = dict_result_script_api['result']['article']['subject']
            except:
                try:
                    #selenium 크롤링 설정(iframe 다중)
                    soup = BeautifulSoup(res.text, 'html.parser')

                    options = webdriver.ChromeOptions()
                    options.add_argument('headless')
                    options.add_argument('disable-gpu')
                    options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                    options.add_argument('lang = ko_KR')
                    
                    driver = webdriver.Chrome(chromedriver, options=options)

                    # 크롤링할 사이트 호출
                    driver.get(User_url)
                    # iframe 진입
                    driver.switch_to.frame("cafe_main")

                    res_iframe = driver.page_source
                    soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                    driver.quit()
                    Title_key = soup_iframe.select_one('h3.title_text').get_text()
                    
                except:
                    Title_key = Title_key

            try:
                Description_key = dict_result_script_api['result']['article']['contentHtml']
            except: # Publisher (카페 네임)
                try:
                    Description_key = dict_result_script_api['result']['cafe']['pcCafeName']
                except:  
                    try:
                        #selenium 크롤링 설정(iframe 다중)
                        soup = BeautifulSoup(res.text, 'html.parser')

                        options = webdriver.ChromeOptions()
                        options.add_argument('headless')
                        options.add_argument('disable-gpu')
                        options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                        options.add_argument('lang = ko_KR')

                        driver = webdriver.Chrome(chromedriver, options=options)

                        # 크롤링할 사이트 호출
                        driver.get(User_url)
                        # iframe 진입
                        driver.switch_to.frame("cafe_main")

                        res_iframe = driver.page_source
                        soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                        driver.quit()
                        Description_key = soup_iframe.select_one('div.se-main-container').get_text()
                    except:
                        Description_key = Description_key

            try: 
                # 카페 대표 썸네일 (게시물 썸네일 불러올 경우 Selenium 필요)
                Thumbnail_image_key = dict_result_script_api['result']['cafe']['image']['url']
            except:
                try:
                    #selenium 크롤링 설정(iframe 다중)
                    soup = BeautifulSoup(res.text, 'html.parser')

                    options = webdriver.ChromeOptions()
                    options.add_argument('headless')
                    options.add_argument('disable-gpu')
                    options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                    options.add_argument('lang = ko_KR')

                    driver = webdriver.Chrome(chromedriver, options=options)

                    # 크롤링할 사이트 호출
                    driver.get(User_url)
                    # iframe 진입
                    driver.switch_to.frame("cafe_main")

                    res_iframe = driver.page_source
                    soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                    driver.quit()
                    Title_key = soup_iframe.select_one('h3.title_text').get_text()
                except:
                    try:
                        se_main_container = soup_iframe.select_one('div.se-main-container')
                        Thumbnail_image_key = se_main_container.select_one('img')['src']
                    except:
                        Thumbnail_image_key = Thumbnail_image_key
            try: 
                Lower_price_key = dict_result_script_api['result']['saleInfo']['price']
                Lower_price.append(Lower_price_key)
                print("네이버 카페 상품 가격은?, ", Lower_price)
            except:
                Lower_price_key = "해당 링크에서 다시 보기" #type == '위시'로 분류되지 않으면 list 내 저장 X
                
    elif 'map.naver' in User_url: 
        product_id_naver_map_re = re.compile('(?<=place\/)[0-9]+')
        product_id_naver_map = product_id_naver_map_re.findall(User_url)[0]

        User_url_api = 'https://map.naver.com/v5/api/sites/summary/' + str(product_id_naver_map) + '?lang=ko'

        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        script_api = BeautifulSoup(res_api.text, 'html.parser').text
        dict_result_script_api = json.loads(script_api)
        try:
            Title_key = dict_result_script_api['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_api['fullRoadAddress']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_api['imageURL']
        except:
            try:
                Thumbnail_image_key = dict_result_script_api['images'][0]['url']
            except:
                Thumbnail_image_key = Thumbnail_image_key
        try:
            Title_key = Title_key + str(" ,") + Description_key
        except:
            pass 
                
    elif 'stock.naver' in User_url:
        product_id_re = re.compile('(?<=stock\/)[0-9]+')
        product_id = product_id_re.findall(User_url)[0]

        User_url_api = 'https://api.stock.naver.com/chart/domestic/item/' + str(product_id) + '?periodType=dayCandle'
        print(User_url_api)
        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        script_api = BeautifulSoup(res_api.text, 'html.parser').text
        dict_result_script_api = json.loads(script_api)
        Lower_price_key = dict_result_script_api['priceInfos'][-1]['openPrice']
        Title_key = Title_key + str(" ,당일 시가: ") + str(format(round(Lower_price_key), ',')) + str("원")
        
    elif 'now.naver' in User_url:            
        if '/l/' in User_url: #라이브
            product_id_naver_now_live_re = re.compile('(?<=\/l\/)[0-9]+')
            product_id_naver_now_live = product_id_naver_now_live_re.findall(User_url)[0]

            User_url_api = 'https://apis.naver.com/now_web/oldnow_web/v4/stream/' + str(product_id_naver_now_live) + '/content/'

            res_api = requests.get(User_url_api, timeout=3, headers=headers) 
            script_api = BeautifulSoup(res_api.text, 'html.parser').text
            dict_result_script_api = json.loads(script_api)

            try:
                Title_key = dict_result_script_api['contentList'][0]['title']['text']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_api['contentList'][0]['description']['text']
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key = dict_result_script_api['contentList'][0]['image']['url']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
        elif 'replay' in User_url:#재방송
            product_id_naver_now_replay1_re = re.compile('(?<=now\.)[0-9]+')
            product_id_naver_now_replay1 = product_id_naver_now_replay1_re.findall(User_url)[0]

            product_id_naver_now_replay2_re = re.compile('(?<=ReplayId=)[0-9]+')
            product_id_naver_now_replay2 = product_id_naver_now_replay2_re.findall(User_url)[0]

            User_url_api = 'https://apis.naver.com/now_web/oldnow_web/v4/shows/now.' + str(product_id_naver_now_replay1) + '/vod/' + str(product_id_naver_now_replay2)

            res_api = requests.get(User_url_api, timeout=3, headers=headers) 
            script_api = BeautifulSoup(res_api.text, 'html.parser').text
            dict_result_script_api = json.loads(script_api)

            try:
                Title_key = dict_result_script_api['episode']['title']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_api['episode']['title']
            except:
                Description_key  = Description_key 
            try:
                Thumbnail_image_key = dict_result_script_api['thumbnail_image_url']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
        else:
            product_id_naver_now_re = re.compile('(?<=now\.)[0-9]+')
            product_id_naver_now = product_id_naver_now_re.findall(User_url)[0]

            User_url_api = 'https://apis.naver.com/now_web/oldnow_web/v4/shows/now.' + str(product_id_naver_now) + '/'

            res_api = requests.get(User_url_api, timeout=3, headers=headers) 
            script_api = BeautifulSoup(res_api.text, 'html.parser').text
            dict_result_script_api = json.loads(script_api)

            try:
                Title_key = dict_result_script_api['title']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_api['description']
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key = dict_result_script_api['profile_image_url']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'sflex.' in User_url: #특정 라이브 쇼핑사(최저가 포함 로직) 다른 distributors보다 앞에 있어야 함
        product_id_sflex_re = re.compile('(?<=const broadcastId = ).+(?=\;)')
        product_id_sflex = product_id_sflex_re.findall(str(soup))[0].strip('''"''')
        User_url_api = 'https://api.sauceflex.com/V1/internal/broadcast/' + str(product_id_sflex)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        result_dict = json.loads(res_api.text)

        try:
            Title_key = result_dict['response']['items'][0]['broadcastName']
        except:
            Title_key = Title_key

        try:
            Description_key = result_dict['response']['items'][0]['explanation']
            if Description_key is None :
                Description_key = '설명없음' 
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = result_dict['response']['items'][0]['thumbnailList'][0]['thumbnailUrl']
        except:
            Thumbnail_image_key = Thumbnail_image_key

        try:
            Lower_price_key = result_dict['response']['items'][0]['productListDetail'][0]['sellingPrice']
        except:
            Lower_price_key = Lower_price_key
            
    elif 'sauceflex.' in User_url: #특정 라이브 쇼핑사(최저가 포함 로직)
        product_id_sauceflex_re = re.compile('(?<=broadcast\/).+')
        product_id_sauceflex = product_id_sauceflex_re.findall(User_url)[0]
        User_url_api = 'https://api.sauceflex.com/V1/internal/broadcast/' + str(product_id_sauceflex)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        result_dict = json.loads(res_api.text)
        try:
            Title_key = result_dict['response']['items'][0]['broadcastName']
        except:
            try:
                Title_key = result_dict['response']['items'][0]['productListDetail'][0]['productName']
            except:
                Title_key = Title_key

        try:
            Thumbnail_image_key = result_dict['response']['items'][0]['thumbnailList'][0]['thumbnailUrl']
        except:
            try:
                Thumbnail_image_key = result_dict['response']['items'][0]['productListDetail'][0]['productThumbnailUrlList'][0]['thumbnailUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key

        try:
            Description_key = result_dict['response']['items'][0]['explanation']
            if Description_key is None :
                Description_key = '설명없음' 
        except:
            Description_key = Description_key
            
        try:
            Lower_price_key = result_dict['response']['items'][0]['productListDetail'][0]['sellingPrice']
        except:
            Lower_price_key = Lower_price_key
            
    elif 'coupang.' in User_url: #뒤에 . 꼭 붙여야 coupangplay등 이랑 구분됨
    #설명 5번_script     
        #header 값을 fb로 잡아야 무한로딩 우회
        headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'} #여기
        headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)', 'Referer': 'https://www.naver.com/'}

        #일반 bs

        res = requests.get(User_url, timeout=3, headers=headers) 

        soup = BeautifulSoup(res.text, 'html.parser')

        script_re = re.compile('(?<=exports.sdp =).+')
        script_text1 = script_re.findall(str(soup))
        script_text = str(script_text1[0].strip().replace(';', ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['itemName']
        except:
            try:
                Title_key = dict_result_script_text['title']
            except:
                Title_key = Title_key
        try:

            Description_key1 = dict_result_script_text['sellingInfoVo']['sellingInfo']    
            for Description_key in Description_key1:
                Description_key = Description_key
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['images'][0]['detailImage']    
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'yslbeautykr'in User_url:                 
        try:                    
            Thumbnail_image_key = soup.select_one('link[rel="image_src"]')['href']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
            
    elif 'ysl.'in User_url: 
        script = soup.select_one('script[type="application/ld+json"]').text
        result_dict = json.loads(str(script))
       
        try:
            Thumbnail_image_key = result_dict['image']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'kbchachacha'in User_url: 
        script = soup.select_one('script[type="application/ld+json"]').text
        result_dict = json.loads(str(script))
       
        try:
            Title_key = result_dict['name']
        except:
            Title_key = Title_key
                
            
    elif 'gmarket' in User_url:
        if 'Live' in User_url:
            try: 
                Title_key = soup.select_one('div.box__live-info > div.text__title').text
            except:
                Title_key = Title_key     #if 'Live' in~부터 요까지 추가
        else:        
            try:
                script_re = re.compile('(?<=groupLayerItems = ).+(?=;)')
                script_text = script_re.findall(str(soup))[0]
                dict_result_script_text = json.loads(script_text)

            except:
                try:   
                    script_re = re.compile('(?<=setOptionLayer\().+(?=, \'vipOptionAreaSub\'\);)')
                    script_text = script_re.findall(str(soup))[0]
                    dict_result_script_text = json.loads(script_text)  

                except:
                    pass

            try:
                Title_key = dict_result_script_text['GoodsInfo']['GoodsName']
            except:
                try:
                    Title_key = dict_result_script_text['Order']['GoodsName']
                except:
                    try:
                        Title_key = dict_result_script_text['GoodsDetail']['GoodsName']
                    except:
                        Title_key = Title_key
            try:
                Thumbnail_image_key = dict_result_script_text['GoodsInfo']['ImageUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key
            
    elif 'oliveyoung' in User_url:
        try:
            product_id_olive_re = re.compile('(?<=goodsNo\=)[\w]+')
            product_id_olive = product_id_olive_re.findall(User_url)[0]
        except:
            product_id_olive_re = re.compile('(?<=sndVal=)[\w]+')
            product_id_olive = product_id_olive_re.findall(User_url)[0]
        User_url_api = 'https://www.oliveyoung.co.kr/store/goods/getGoodsGtmInfoAjaxNew.do?goodsNoArrStr=' + str(product_id_olive) + '&itemNoArrStr=001&positionArrStr=1&giftCardYn=N'
        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        result_dict = json.loads(res_api.text)[0]

        try:
            Title_key = result_dict['goodsNm']
        except:
            try:
                Title_key = soup.select_one('p.prd_name').get_text()
            except:
                try:
                    Title_key = soup.select_one('h2.contents_header_logo').text 
                except:
                    Title_key = Title_key  
            
        if Type_key == '기타' and Category_in_key != 'sns':
            Thumbnail_image_key = User_url
        else:
            try:
                Thumbnail_image_key = soup.select_one('div > #mainImg')['src']
            except:
                Thumbnail_image_key = Thumbnail_image_key
        try:
            Description_key = result_dict['dispCatNm']
        except:
            try:
                Description_key = result_dict['stdCatNm']
            except:
                Description_key = Description_key
                
    elif 'wemakeprice' in User_url:
    #설명 5번_selenium    
#         options = webdriver.ChromeOptions()
#         options.add_argument('headless')
#         options.add_argument('disable-gpu')
#         options.add_argument('User-Agent: facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)')
#         options.add_argument('lang = ko_KR')

#         driver = webdriver.Chrome(chromedriver, options=options)

#         driver.get(User_url)
#         User_url = driver.current_url

#         print('final redirected url은', User_url)
#         driver.quit()

        User_url =  User_url.replace('share/','')
        headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)', 'Referer': 'https://www.naver.com/'}
        res = requests.get(User_url, timeout=3, headers=headers) 
        soup = BeautifulSoup(res.content, 'html.parser')

        script_re = re.compile('(?<=initialData\'\, JSON\.parse\(\').+')
        script_text1 = script_re.findall(str(soup))

        script_text = str(script_text1[0].strip().replace("'));", "").replace('\\"',"").replace("\\", "").replace("[\t\n\r\f\v]", ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['dealNm']
        except:
            try:          
                Title_key = dict_result_script_text['ogTitle']
            except:
                Title_key = Title_key

        try:
            Description_key = dict_result_script_text['dcateNm']
        except:
            try:
                Description_key = dict_result_script_text['lcateNm']       
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['mainImgList'][0]['thumb']['imgUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['mainImgList'][0]['origin']['imgUrl'] 
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'bunjang' in User_url:
        #api
        product_id_bunjang_re = re.compile('(?<=products\/)[0-9]+')
        product_id_bunjang = product_id_bunjang_re.findall(User_url)[0]
        User_url_api = 'https://api.bunjang.co.kr/api/1/product/' + str(product_id_bunjang) + '/detail_info.json?version=4'

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)
        
        #js
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script_text = json.loads(str(script))
       
        try:
            Title_key = result_dict['item_info']['name']
        except:
            try:
                Title_key = dict_result_script_text['name']
            except:
                Title_key = Title_key
                
        try:
            Description_key = result_dict['item_info']['description']
        except:
            try:
                Description_key = dict_result_script_text['description']
            except:
                Description_key = Description_key
                
        try:
            Thumbnail_image_key = result_dict['item_info']['product_image']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key
            
    elif 'cjonstyle' in User_url:
        Title_key_temp = Title_key
        Title_key = Description_key
        Description_key = Title_key_temp       

    elif 'kcar' in User_url:
        try:
            product_id_kcar_re = re.compile('(?<=CarCd=)\w+')
            product_id_kcar = product_id_kcar_re.findall(User_url)[0]
        except:
            product_id_kcar_re = re.compile('(?<=CarCd=)(.+)[(?=\&)]?')
            product_id_kcar = product_id_kcar_re.findall(User_url)[0]

        User_url_api = 'https://mapi.kcar.com/bc/car-info-detail?i_sCarCd=' + str(product_id_kcar)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        print("User_url_api", User_url_api)

        dict_result_script_api = json.loads(res_api.text)

        #Title

        try:
            Title_key = dict_result_script_api['data']['rvo']['carWhlNm']
        except:
            try:
                Title_key = dict_result_script_api['data']['rvo']['modelNm']
            except:
                Title_key = Title_key
        #Desc.
        try:
            Description_key = dict_result_script_api['data']['rvo']['simcDesc']
        except:
            try:
                Description_key = dict_result_script_api['data']['rvo']['carDtlDesc']
            except:
                try:
                    Description_key = dict_result_script_api['data']['rvo']['keyPntCnts']
                except:
                    Description_key = Description_key
        # Thumb
        try:
            Thumbnail_image_key = dict_result_script_api['data']['rvo']['elanPath']
        except:
            Thumbnail_image_key = dict_result_script_api['data']['photoList'][0]['elanPath']

    elif 'nsmall' in User_url: #hnsmall은 앞에서 걸어야 함
        product_id_nsmall_re = re.compile('(?<=product\/)[0-9]+')
        product_id_nsmall = product_id_nsmall_re.findall(User_url)[0]
        User_url_nsmall_api = 'https://mwapi.nsmall.com/webapp/wcs/stores/servlet/DetailProductViewReal'

        headers = {
        'authority': 'mwapi.nsmall.com',
        'method': 'POST',
        # 'path': '/webapp/wcs/stores/servlet/DetailProductViewReal',
        # 'scheme': 'https',
        # 'accept': 'application/json, text/plain, */*',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'content-length': '110',
        # 'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=oSaPrHIIdNVZzXZRyOJJ8KH5SCw%3d%0a%3b2022%2d07%2d18+10%3a17%3a36%2e554%5f1658107056545%2d687992%5f13001%5f1549272167%2c%2d9%2cKRW%5f13001; WC_AUTHENTICATION_1549272167=1549272167%2cibU9QHx7Awccd8err%2fxgbtm%2bPaA%3d; WC_ACTIVEPOINTER=%2d9%2c13001; WC_USERACTIVITY_1549272167=1549272167%2c13001%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2c86EHl%2bYZCaIQnr37dzawxXHxVmTIUYIO%2b6gmfkcnjG0MG%2fU8lH6zAn7%2fEk58EVzKzpGjxI2fFpnO%0aXpKhu9hZ2p9qq4FFXGCAjXVcozS8Pr3XCUJJ%2fKPf59bDuHfQC%2fAtzdHpJ2bwdLOkYvEIaI4zHw%3d%3d; WMONID=j65WmRhaJMb; _qg_fts=1658107057; QGUserId=3536195775064691; _qg_pushrequest=true; goodsTodayCookie=32128684!N; goodsTodayCatIdCookie=32128684!&catalogId=18151&mCategoryId=18151&cate1Code=200302&cate2Code=20767&cate3Code=1811561; _qg_cm=1; RB_PCID=1658107058207701329; _gid=GA1.2.831579550.1658107059; _fbp=fb.1.1658107059581.1853397954; EG_GUID=99428539-52b2-4fc8-a99d-2707b400c307; JSESSIONID=00028-sI5N5cyficE4UWo_bU7oy:1991y6hny; ipAuth=-2117978956; co_cd=110; accpt_path_cd=100; shoppingRefer=http://mwapi.nsmall.com/; a1_gid=Aew+gWHEHeIAC9Tc; appier_utmz=%7B%7D; _atrk_siteuid=xCs6ca_BK2BoCv2-; _atrk_ssid=eXUGUUcMg7VEA-b9IMaGIj; _atrk_sessidx=1; appier_pv_counterc91ce3e5a69b64f=0; appier_page_isView_c91ce3e5a69b64f=643494110593788a4b90a96ae14ea6467b5950849cd304bc762689a54e232546; appier_pv_counter0876aad651ed64f=0; appier_page_isView_0876aad651ed64f=643494110593788a4b90a96ae14ea6467b5950849cd304bc762689a54e232546; wcs_bt=s_4c84f6106481:1658107871; gapageInfo=home; __utma=41019966.790199591.1658107059.1658107872.1658107872.1; __utmz=41019966.1658107872.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=41019966; __utmt_UA-92946860-1=1; __utmb=41019966.1.10.1658107872; au_id=990a94931fea3366425f7e7617ddfb5b35b-3d7c; dl_uid=bc5ca977d30eb8fa09d41ffd8846be7; cto_bundle=UQgTlF80YmM4UU1SaEFBWWFydUMwa1RXRm9jZjN2TkwxQTMlMkJ0RTRZJTJCdUglMkJTdUMycCUyRndPZVJYMGlYOWRwQzBXZTIyU0xoZ0hWZVlFVUthb1FNRktOMmIlMkJKMyUyQmlaVGZVd2NvTXlrRlVnekZOb3k1REt0RTdaOVo1ZGNiM0lMQW5CZjQ4b1JmQTdqMDJQd25zRlNRJTJCOFVYZ3VBUSUzRCUzRA; _uni_id=2a1cc137-0ef8-4a7e-9de4-6e90fd191e07; check_uni_send=0; _ga_J7E3QT1NRY=GS1.1.1658107874.1.0.1658107874.0; _ga=GA1.2.790199591.1658107059; _gat_gp=1; _gat_UA-92946860-8=1; RB_SSID=Qdg4m5ZyhS; airbridge_session=%7B%22id%22%3A%22a7fe42ad-92a8-42a2-8c3e-7dcbbf9f42ae%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1658107058956%2C%22end%22%3A1658108058990%7D',
        # 'origin': 'https://mw.nsmall.com',
        # 'referer': 'https://mw.nsmall.com/',
        # 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-site',
        'user-agent' : 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        payload = {
        'partNumber': product_id_nsmall #product_id
        # 'cocd': '110',
        # 'imgSizeType': 'Q',
        # 'accptPath': '500',
        # 'accptPathCd': '500',
        # 'req_co_cd': '110',
        # 'userId': '',
        # 'catalogId': '97001'
        }

        res = requests.post(User_url_nsmall_api, headers=headers, data =  payload, timeout = 10) 
        soup = BeautifulSoup(res.content,"html.parser")
        dict_post_api = json.loads(soup.text)
        
        Title_key = dict_post_api['msg']['goods'][0]['info']['productName']
        Description_key = dict_post_api['msg']['goods'][0]['info']['productName']
        Thumbnail_image_key = dict_post_api['msg']['goods'][0]['info']['photoList'][0]['photoPath']
        
    elif 'sivillage' in User_url:
        if 'event' in User_url:
            try:
                Title_key = soup.select_one('h3').get_text()
            except:
                Title_key = Title_key
        else:
            
            try:
                Title_key = soup.select_one('p.detail__info-description-1').text
            except:
                try:
                    Title_key = soup.select_one('meta[property="eg:itemName"]')['content']
                except:
                    try:
                        sv_name_re = re.compile('(?<=\'name\':)(.*?)(?=,)')
                        Title_key= sv_name_re.findall(str(soup))[0]
                    except:
                        try:
                            Title_key = soup.select_one('h2.tit_article').text
                        except:
                            Title_key = Title_key
        try:
            sv_desc_re = re.compile('(?<=\'variant\':)(.*?)(?=,)')
            Description_key = sv_desc_re.findall(str(soup))[0]
        except:
            try:
                Description_key = soup.select_one('p.detail__info-code').text
            except:
                try:
                    Description_key = soup.select_one('p.txt_excerpt').text
                except:
                    Description_key = Description_key

        try:
            sv_img_re = re.compile('(?<=img:)(.*?)(?=,)')
            Thumbnail_image_key = sv_img_re.findall(str(soup))[0].strip("' ")
        except:
            try:
                Thumbnail_image_key = soup.select_one('div.detail__vi-slide.swiper-slide img')['src']
            except:
                try:
                    Thumbnail_image_key = soup.select_one('div.swiper-zoom-container img')['src']
                except:
                    try:
                        Thumbnail_image_key = soup.select_one('div.image img')['src']
                    except:
                        Thumbnail_image_key = Thumbnail_image_key    

    elif 'ssfshop' in User_url:
        
        try:
            Thumbnail_image_key = soup.select_one('.poster img')['src']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
        if 'live_commerce' in User_url:
            Thumbnail_image_key = 'https://m.ssfshop.com/' + Thumbnail_image_key
            
        if 'community/style' in User_url: #ssf diver 
            ssfsdiver_re = re.compile('(?<=community\/style\/).+')
            ssfsdiver_style_no = ssfsdiver_re.findall(User_url)[0]
            User_url_api = 'https://m.ssfshop.com/community/api/v1/style/getStyle?styleNo=' + ssfsdiver_style_no

            res_api = requests.get(User_url_api, timeout=3, headers=headers) 

            soup_api = BeautifulSoup(res_api.text, 'html.parser')
            dict_result_script_api = json.loads(str(soup_api))

            Thumbnail_image_key = 'https://img.ssfshop.com' + dict_result_script_api['data']['styles'][ssfsdiver_style_no]['styleImgList'][0]
            Description_key = dict_result_script_api['data']['styles'][ssfsdiver_style_no]['contents']
            
    elif '11st' in User_url:
        if 'live11' in User_url:
            try:
                product_id_11st_live = re.sub(r'[^0-9]', '', User_url[-6:]) 
                User_url_api = 'https://live11-vod.11st.co.kr/v1/broadcasts/' + product_id_11st_live + '/vod-info'
                res_api = requests.get(User_url_api, timeout=3, headers=headers) 

                soup_api = BeautifulSoup(res_api.text, 'html.parser')
                dict_result_script_api = json.loads(str(soup_api))
                Title_key = dict_result_script_api['settingInfo']['settings'][0]['title']
                Description_key = dict_result_script_api['settingInfo']['settings'][0]['popupBody']
                Thumbnail_image_key = dict_result_script_api['broadcastInfo']['shareImageUrl']
            except:
                Title_key = Title_key
                Description_key = Description_key
                Thumbnail_image_key = Thumbnail_image_key

    elif 'gsshop' in User_url:
        script_re = re.compile('(?<=renderJson = ).+')
        script_text1 = script_re.findall(str(soup))
        script_text = str(script_text1[0].strip().replace(';', ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['prd']['exposPrdNm']
        except:
            try:
                Title_key = dict_result_script_text['prd']['prdNm']
            except:
                Title_key = Title_key

        try:
            Description_key = dict_result_script_text['prd']['exposPmoNm']
        except:
            Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['prd']['imgInfo'][0]['imgUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['prd']['prdImgL1']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['prd']['videoImgUrl']
                except:
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'grip.show' in User_url:
        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
             Title_key =  Title_key 


    elif 'cartier' in User_url:
        script_re = re.compile('(?<=json">\n).+')
        script_text = script_re.findall(str(soup))[0]
        dict_result_script_text = json.loads(script_text)
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image'][0]
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'land.naver' in User_url:
        if 'complex' in User_url: #complex
            try:
                script_re = re.compile('(?<=hscpNm).+')
                Title_key = script_re.findall(str(soup))[0].strip(" :,'")
            except:
                Title_key = Title_key
            try:
                script_re = re.compile('(?<=cortarNm).+')
                Description_key = script_re.findall(str(soup))[0].strip(" :,'")
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key1 = soup.select_one('div.detail_photo_inner > button')['style']
                Thumbnail_image_key = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\-@\.&+#:\/?=_]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+', Thumbnail_image_key1)[0].strip(")")
            except:
                Thumbnail_image_key = Thumbnail_image_key

        else: # detail_deal(article)         
            script_re = re.compile('(?<=window.App=)(.*?)(?=<\/script><script src)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)
            try:
                Title_key = dict_result_script_text['state']['article']['article']['articleName']
            except:
                try:
                    Title_key = dict_result_script_text['state']['article']['dealerTelInfo']['atclNm']
                except:
                    try:
                        Title_key = soup.select_one('strong.header_head_title').text
                    except:
                        try:
                            Title_key = soup.select_one('strong.detail_sale_title').text
                        except:
                                Title_key = Title_key
            try:
                Description_key = dict_result_script_text['state']['article']['article']['exposureAddress']
            except:
                try:
                    Description_key = dict_result_script_text['state']['article']['location']['detailAddress']
                except:
                    try:
                        Description_key = soup.select_one('em.detail_info_branch').text
                    except:
                        Description_key = Description_key              
            try:
                Thumbnail_image_key1 = soup.select_one('div.detail_photo_inner > button')['style']
                Thumbnail_image_key = re.findall('http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$\-@\.&+#:\/?=_]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+', Thumbnail_image_key1)[0].strip(")")
            except:
                Thumbnail_image_key = Thumbnail_image_key
                    
    elif Distributor_key in ['naver']:
        naver_shopping_keywords = ['catalog', 'brand', 'store', 'smartstore']
        if any(naver_shopping_keyword in User_url for naver_shopping_keyword in naver_shopping_keywords) == True:
            script_re = re.compile('(?<=json">).*(?=<\/script>)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)

            try:
                Title_key = dict_result_script_text['name']
            except:
                try:
                    Title_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['catalog_Catalog']['productName']
                except:
                    try:
                        Title_key = dict_result_script_text['props']['pageProps']['catalog']['productName']
                    except:
                        try:
                            Title_key = dict_result_script_text['props']['pageProps']['ogTag']['title']
                        except:
                            Title_key = Title_key
            try:
                Thumbnail_image_key = dict_result_script_text['image']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['props']['pageProps']['ogTag']['image']
                except:
                    Thumbnail_image_key =Thumbnail_image_key

            try:
                Description_key = dict_result_script_text['description']
            except:
                try:
                    Description_key = dict_result_script_text['props']['pageProps']['ogTag']['description']
                except:
                    Description_key = Description_key

    elif 'wconcept' in User_url:
        try:
            script_re = re.compile('(?<=content_name: ).*(?=\,)')
            Title_key = script_re.findall(str(soup))[0]
        except:
            try:
                Title_key = dict_result_script_text['itemName']
            except:
                try:
                    Title_key = soup.select_one('meta[property="og:description"]')['content']
                except:
                    try:
                        Title_key = soup.select_one('span.product_name').text
                    except:
                        try:
                            Title_key = soup.select_one('meta[property="eg:itemName"]')['content']
                        except:
                            try:
                                Title_key = soup.select_one('input#hidItemName')['value']
                            except:
                                Title_key, Description_key = Description_key, Title_key

        try:
            Description_key = soup.select_one('input#hidAddCatFix')['value'].replace("^"," ")
        except:
            Description_key = Description_key                    
                    
    elif 'thehandsome' in User_url:
        try:  
            script_re = re.compile('(?<=productName :).*(?=\,)')
            Title_key = script_re.findall(str(soup))[0]   
        except:
            try:
                Title_key = soup.select_one('meta[property="og:title"]')['content']
            except:
                try:
                    Title_key = soup.select_one('meta[property="recopick:title"]')['content']
                except:
                    Title_key = Title_key

        try:
            Description_key = soup.select_one('div.prod-detail-con-box').text
        except:
            Description_key = Description_key

        try:
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
        except:
            try:
                Thumbnail_image_key = soup.select_one('meta[property="recopick:image"]')['content']
            except:
                Thumbnail_image_key = Thumbnail_image_key                

    elif 'dailyhotel' in User_url:

        try:
            product_id_re = re.compile('(?<=stays\/)[0-9]{2,10}[(?=?)]?')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://www.dailyhotel.com/newdelhi/goodnight/api/v9/hotel/' + product_id            
        except:
            product_id_re = re.compile('(?<=activity\/)[0-9]{2,10}[(?=?)]?')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://www.dailyhotel.com/newdelhi/goodnight/api/v1/activity/deals/' + product_id            

        print(User_url_api)
        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)

        try:
            Title_key = result_dict['data']['name']
        except:
            try:
                Title_key = result_dict['data']['title']
            except:               
                try:
                    Title_key = soup.select_one('title').text
                except:
                    try:
                        Title_key = soup.select_one('div.detail-title').text
                    except:
                        Title_key = Title_key
                        
        try:
            Description_key = result_dict['data']['address']
        except:
            try:
                Description_key = result_dict['data']['details'][0]['contents'][0]
            except:
                try:
                    Description_key = result_dict['data']['storeInfo']['address']
                except:
                    try:
                        Description_key = soup.select_one('p.comment').text
                    except:
                        try:
                            Description_key = soup.select_one('ul.lists').text
                        except:
                            Description_key = Description_key        
                                
        try:
            Thumbnail_image_key = result_dict['data']['images'][-1]['url']
        except:
            try:
                Thumbnail_image_key = result_dict['data']['basicImages'][0]['imagePath']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'dior' in User_url:
        try:
            script_re = re.compile('(?<=description\"\/><script type=\"application\/ld\+json\">).*(?=<\/script><link as)')
            script_text = script_re.findall(str(soup))[0].strip()
            dict_result_script_text = json.loads(script_text)
        except:
            try:
                script_re = re.compile('(?<=application\/ld\+json\">).*(?=<\/main>)', re.DOTALL)
                script_text = script_re.findall(str(soup))[0].replace("</script>", "").strip()
                dict_result_script_text = json.loads(script_text)        
            except:
                try:
                    script_re = re.compile('(?<=application\/ld\+json\">).*(?=<\/script><link rel)')
                    script_text = script_re.findall(str(soup))[0].strip()
                    dict_result_script_text = json.loads(script_text)
                except:
                    try:
                        script_re = re.compile('(?<=application\/ld\+json\">).*(?=<\/script>)', re.DOTALL)
                        script_text = script_re.findall(str(soup))[0].strip()
                        dict_result_script_text = json.loads(script_text)       
                    except:
                        script_re = re.compile('(?<=var meta = ).*(?=;)')
                        script_text = script_re.findall(str(soup))[0].strip()
                        dict_result_script_text = json.loads(script_text)
        try:
            Title_key = dict_result_script_text['name']
        except:
            try:
                Title_key = dict_result_script_text['product']['variants'][0]['name']
            except:
                Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            try:
                Description_key = dict_result_script_text['product']['type']
            except:
                Description_key = Description_key
        try:
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
            
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['image']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['image'][0]
                except:
                    Thumbnail_image_key = Thumbnail_image_key
                
    elif 'myrealtrip' in User_url:
        script_bs = soup.select_one('script[data-component-name="Offer"]').text
        dict_result_script_text = json.loads(str(script_bs))   

        try:
            Title_key = dict_result_script_text['offerInfo']['title']
        except:
            try:
                Title_key = soup.select_one('div.loading_title').text
            except:
                Title_key = Title_key

        try:
            Description_key = dict_result_script_text['offerInfo']['subtitle']
        except:
            try:
                Description_key = dict_result_script_text['offerInfo']['introduction']
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['photos'][0]
        except:
            try:
                Thumbnail_image_key = 'https://d2yoing0loi5gh.cloudfront.net/assets/og-image-35b4b66874396ae2fc8991b926c1f0c09f27f25f9c0a23f15e5e96c73c2c9992.png' #마이리얼트립 디폴트 이미지'
            except:
                Thumbnail_image_key =Thumbnail_image_key
                
    elif 'homeplus' in User_url:
        if 'my' in User_url:
            try:
                Title_key = soup.select_one('h2.visual_tit').get_text()
            except:
                try: 
                    Title_key = soup.select_one('p.title').text
                except:
                    Title_key = Title_key          
            
            try:
                Thumbnail_image_key = soup.select_one('div.digigtal_visual_cont img')['src']
            except:
                Thumbnail_image_key = Thumbnail_image_key        
            
        else:
            script_text = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(script_text)
            try:
                Title_key = dict_result_script_text['@graph'][0]['name']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_text['@graph'][0]['description']
            except:
                Description_key = Description_key 

    elif 'kurly' in User_url:
        script_text = soup.select_one('script[type="application/json"]').text
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['name']
        except:
            try:
                Title_key = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['masterProductName']
            except:
                try:
                    Title_key = dict_result_script_text['props']['pageProps']['product']['name']
                except:
                    Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['props']['pageProps']['product']['mainImageUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['props']['pageProps']['product']['shareImageUrl']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['props']['pageProps']['product']['originalImageUrl']
                except:
                    Thumbnail_image_key = Thumbnail_image_key
                    
    elif 'mangoplate' in User_url:
        script_text = soup.select_one('script[type="application/json"]').text
        dict_result_script_text = json.loads(script_text)
        try:
            Title_key = dict_result_script_text['title']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['picture_url']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'balaan' in User_url:
        product_id_balaan_re = re.compile('(?<=goodsno=)[0-9]+')
        product_id_balaan = product_id_balaan_re.findall(User_url)[0]
        User_url_api = 'https://api.balaan.co.kr/v1/goods/recent?goodsnoString=' + str(product_id_balaan)
        print('User_url_api??', User_url_api)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        result_dict = json.loads(res_api.text)
        try:
            Title_key = result_dict['data'][product_id_balaan]['goodsnm']
        except:
            try:
                Title_key = result_dict['data'][product_id_balaan]['origin']
            except:
                Title_key = Title_key
        try:
            Thumbnail_image_key = result_dict['data'][product_id_balaan]['img_i']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'burberry' in User_url:            
        script_re = re.compile('(?<=PRELOADED_STATE__ = ).+(?=;)', re.DOTALL)
        script_text = script_re.findall(str(soup))[0]
        dict_result_script_text = json.loads(script_text)
        
        product_id_re = re.compile('(?<=burberry.com).+')
        product_id = product_id_re.findall(User_url)[0]  
        try:
            Title_key = dict_result_script_text['db']['pages'][product_id]['data']['name']
        except:
            try:
                Title_key = dict_result_script_text['db']['pages'][product_id]['data']['content']['title']
            except:
                try:
                    Title_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['name']
                except:
                    Title_key = Title_key

        try:
            Description_key = dict_result_script_text['db']['pages'][product_id]['data']['content']['description']
        except:
            try:
                Description_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['description']
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = dict_result_script_text['db']['pages'][product_id]['data']['galleryItems'][0]['image']['imageDefault']
        except:
            try:
                Thumbnail_image_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'brandi' in User_url:  
        script = soup.select_one('script[type="text/javascript"]').text.replace('window.__INITIAL_STATE__ = ','').replace('window.__IS_INITIAL_STATE__ = true;','').replace(';','').strip()
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['product']['product']['name']
        except:
             Title_key =Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['product']['product']['image_thumbnail_url']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'chanel' in User_url:  
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script= json.loads(str(script))

        try:
            Title_key = dict_result_script['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script['image']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'pulmuone' in User_url: 
        product_id_pulmuone_re = re.compile('(?<=goods=)[0-9]+')
        product_id_pulmuone = product_id_pulmuone_re.findall(User_url)[0]
        User_url_pulmuone_api = 'https://shop.pulmuone.co.kr/goods/goods/getGoodsPageInfo'

        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Host': 'shop.pulmuone.co.kr',
        'Connection': 'alive',
        # 'scheme': 'https',
        # 'accept': 'application/json, text/plain, */*',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'content-length': '110',
        # 'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'WC_SESSION_ESTABLISHED=true; WC_PERSISTENT=oSaPrHIIdNVZzXZRyOJJ8KH5SCw%3d%0a%3b2022%2d07%2d18+10%3a17%3a36%2e554%5f1658107056545%2d687992%5f13001%5f1549272167%2c%2d9%2cKRW%5f13001; WC_AUTHENTICATION_1549272167=1549272167%2cibU9QHx7Awccd8err%2fxgbtm%2bPaA%3d; WC_ACTIVEPOINTER=%2d9%2c13001; WC_USERACTIVITY_1549272167=1549272167%2c13001%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2cnull%2c86EHl%2bYZCaIQnr37dzawxXHxVmTIUYIO%2b6gmfkcnjG0MG%2fU8lH6zAn7%2fEk58EVzKzpGjxI2fFpnO%0aXpKhu9hZ2p9qq4FFXGCAjXVcozS8Pr3XCUJJ%2fKPf59bDuHfQC%2fAtzdHpJ2bwdLOkYvEIaI4zHw%3d%3d; WMONID=j65WmRhaJMb; _qg_fts=1658107057; QGUserId=3536195775064691; _qg_pushrequest=true; goodsTodayCookie=32128684!N; goodsTodayCatIdCookie=32128684!&catalogId=18151&mCategoryId=18151&cate1Code=200302&cate2Code=20767&cate3Code=1811561; _qg_cm=1; RB_PCID=1658107058207701329; _gid=GA1.2.831579550.1658107059; _fbp=fb.1.1658107059581.1853397954; EG_GUID=99428539-52b2-4fc8-a99d-2707b400c307; JSESSIONID=00028-sI5N5cyficE4UWo_bU7oy:1991y6hny; ipAuth=-2117978956; co_cd=110; accpt_path_cd=100; shoppingRefer=http://mwapi.nsmall.com/; a1_gid=Aew+gWHEHeIAC9Tc; appier_utmz=%7B%7D; _atrk_siteuid=xCs6ca_BK2BoCv2-; _atrk_ssid=eXUGUUcMg7VEA-b9IMaGIj; _atrk_sessidx=1; appier_pv_counterc91ce3e5a69b64f=0; appier_page_isView_c91ce3e5a69b64f=643494110593788a4b90a96ae14ea6467b5950849cd304bc762689a54e232546; appier_pv_counter0876aad651ed64f=0; appier_page_isView_0876aad651ed64f=643494110593788a4b90a96ae14ea6467b5950849cd304bc762689a54e232546; wcs_bt=s_4c84f6106481:1658107871; gapageInfo=home; __utma=41019966.790199591.1658107059.1658107872.1658107872.1; __utmz=41019966.1658107872.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=41019966; __utmt_UA-92946860-1=1; __utmb=41019966.1.10.1658107872; au_id=990a94931fea3366425f7e7617ddfb5b35b-3d7c; dl_uid=bc5ca977d30eb8fa09d41ffd8846be7; cto_bundle=UQgTlF80YmM4UU1SaEFBWWFydUMwa1RXRm9jZjN2TkwxQTMlMkJ0RTRZJTJCdUglMkJTdUMycCUyRndPZVJYMGlYOWRwQzBXZTIyU0xoZ0hWZVlFVUthb1FNRktOMmIlMkJKMyUyQmlaVGZVd2NvTXlrRlVnekZOb3k1REt0RTdaOVo1ZGNiM0lMQW5CZjQ4b1JmQTdqMDJQd25zRlNRJTJCOFVYZ3VBUSUzRCUzRA; _uni_id=2a1cc137-0ef8-4a7e-9de4-6e90fd191e07; check_uni_send=0; _ga_J7E3QT1NRY=GS1.1.1658107874.1.0.1658107874.0; _ga=GA1.2.790199591.1658107059; _gat_gp=1; _gat_UA-92946860-8=1; RB_SSID=Qdg4m5ZyhS; airbridge_session=%7B%22id%22%3A%22a7fe42ad-92a8-42a2-8c3e-7dcbbf9f42ae%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1658107058956%2C%22end%22%3A1658108058990%7D',
        # 'origin': 'https://mw.nsmall.com',
        # 'referer': 'https://mw.nsmall.com/',
        # 'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-site',
        'user-agent' : 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        payload = {
        'ilGoodsId': product_id_pulmuone #product_id
        # 'cocd': '110',
        # 'imgSizeType': 'Q',
        # 'accptPath': '500',
        # 'accptPathCd': '500',
        # 'req_co_cd': '110',
        # 'userId': '',
        # 'catalogId': '97001'
        }

        res = requests.post(User_url_pulmuone_api, headers=headers, data =  payload, timeout = 10) 
        soup = BeautifulSoup(res.content,"html.parser")
        dict_post_api = json.loads(soup.text)
        
        try:
            Title_key = dict_post_api['data']['goodsName']
        except:
            try:
                Title_key = soup.select_one('meta[property="og:description"]')['content']
            except:
                Title_key = Title_key
        try:
            Description_key = dict_post_api['data']['goodsDesc']
        except:
            try:
                Description_key = soup.select_one('meta[name="keywords"]')['content']
            except:
                Description_key = Description_key
                
        try:
            Thumbnail_image_key = 'https://s.pulmuone.app/' + dict_post_api['data']['goodsImage'][0]['bigImage']        
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'seoulstore' in User_url:
        if 'articles' in User_url:
            product_id_seoulstore_re = re.compile('(?<=articles\/)[0-9]+')
            product_id_seoulstore = product_id_seoulstore_re.findall(User_url)[0]
            User_url_seoulstore_api = 'https://www.seoulstore.com/api/do/getArticle'

            headers = {
            'authority': 'www.seoulstore.com',
            'method': 'POST',
            'path': '/api/do/getArticle',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '41',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'cookie': 'uuid=9f1c4af0-1154-11ed-a610-45e0413e2e4e; _fbp=fb.1.1659329068402.1133576827; _dtrBrwsId=HYQP5czGL3Z6rTLH1X_zj; _ga=GA1.2.1520780270.1659329069; _gid=GA1.2.415129831.1660038801; _pk_ref.10003.bfc8=%5B%22%22%2C%22%22%2C1660095550%2C%22http%3A%2F%2Flocalhost%3A8888%2F%22%5D; _pk_ses.10003.bfc8=1; cto_bundle=jm7fnF96dWUxJTJGYUdXQ0tFTUgzYVRJV1huYlZnQ1NFcWNMVmFmNWdPJTJGUXB1dGpWV1A3bTFXNUw5SXBlYVdnTU4wR3E0Z2pGQ1M1YnJkVUN2QnBPTnNDelNNRjFoWGpKYWpEVk1hMjh5YTl1eHpEWHoxOE1NT3dNNDVEdWZiSG5Pd25JTk1GdHcydEhqWW84UVRVdkpFUDR5dERRJTNEJTNE; _dc_gtm_UA-61220221-4=1; _pk_id.10003.bfc8=e642d31d9f3920dd.1659329068.4.1660095957.1660095550.; wcs_bt=s_2d9af6c410c4:1660095957',
            'origin': 'https://www.seoulstore.com',
            'referer': 'https://www.seoulstore.com/articles/' + str(product_id_seoulstore) + '/news',
        #     'user-agent' : 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
            }
            payload = {
            'id': product_id_seoulstore, #product_id
            'method': 'getArticle'
            }
            res = requests.post(User_url_seoulstore_api, headers=headers, data =  payload, timeout = 10) 
            soup = BeautifulSoup(res.content,"html.parser")
            dict_post_api = json.loads(soup.text)
            

            try:
                Title_key = dict_post_api['subject']
            except:
                Title_key = Title_key
            
            try:
                Thumbnail_image_key = dict_post_api['boardFile'][0]
            except:
                Thumbnail_image_key = Thumbnail_image_key
        
        
        else:
            product_id_seoulstore_re = re.compile('(?<=products\/)[0-9]+')
            product_id_seoulstore = product_id_seoulstore_re.findall(User_url)[0]
            User_url_seoulstore_api = 'https://www.seoulstore.com/api/do/getProduct'

            headers = {
            'authority': 'www.seoulstore.com',
            'method': 'POST',
            'path': '/api/do/getProduct',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '41',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'cookie': 'uuid=9f1c4af0-1154-11ed-a610-45e0413e2e4e; _fbp=fb.1.1659329068402.1133576827; _dtrBrwsId=HYQP5czGL3Z6rTLH1X_zj; _ga=GA1.2.1520780270.1659329069; _gid=GA1.2.415129831.1660038801; _pk_ref.10003.bfc8=%5B%22%22%2C%22%22%2C1660095550%2C%22http%3A%2F%2Flocalhost%3A8888%2F%22%5D; _pk_ses.10003.bfc8=1; cto_bundle=jm7fnF96dWUxJTJGYUdXQ0tFTUgzYVRJV1huYlZnQ1NFcWNMVmFmNWdPJTJGUXB1dGpWV1A3bTFXNUw5SXBlYVdnTU4wR3E0Z2pGQ1M1YnJkVUN2QnBPTnNDelNNRjFoWGpKYWpEVk1hMjh5YTl1eHpEWHoxOE1NT3dNNDVEdWZiSG5Pd25JTk1GdHcydEhqWW84UVRVdkpFUDR5dERRJTNEJTNE; _dc_gtm_UA-61220221-4=1; _pk_id.10003.bfc8=e642d31d9f3920dd.1659329068.4.1660095957.1660095550.; wcs_bt=s_2d9af6c410c4:1660095957',
            'origin': 'https://www.seoulstore.com',
            'referer': 'https://www.seoulstore.com/products/' + str(product_id_seoulstore) + '/detail?ecommerceListName=ranking_all',
        #     'user-agent' : 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
            }
            payload = {
            'id': product_id_seoulstore, #product_id
            'method': 'getProduct'
            }
            res = requests.post(User_url_seoulstore_api, headers=headers, data =  payload, timeout = 10) 
            soup = BeautifulSoup(res.content,"html.parser")
            dict_post_api = json.loads(soup.text)



            try:
                Title_key = dict_post_api['descriptions']['name']
            except:
                try:
                    Title_key = dict_post_api['name']
                except:
                    Title_key = Title_key
            try:
                Description_key = dict_post_api['siteProductTags'][0]
            except:
                try:
                    Description_key = dict_post_api['channelName']
                except:
                    Description_key = Description_key
            try:
                Thumbnail_image_key = dict_post_api['images']['add'][0]
            except:
                try:
                    Thumbnail_image_key = dict_post_api['images']['list']
                except:
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'skyscanner' in User_url:
        try: # 호텔
            Thumbnail_image_key = soup.select_one('link[as="image"]')['href']
        except:
            Thumbnail_image_key = 'https://www.skyscanner.co.kr/sttc/blackbird/opengraph_solid_logo.png'

    elif 'styleshare' in User_url:  
        product_id_re = re.compile('(?<=goods\/)[0-9]+')
        product_id = product_id_re.findall(User_url)[0]
        User_url_api = 'https://shop-gateway.styleshare.kr/display/api/v1/goods/' + str(product_id)

        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
        result_dict = json.loads(res_api.text)
        try:
            Title_key = result_dict['name']
        except:
            Title_key = Title_key
            
    elif 'adidas' in User_url:  
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image'][0]
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'lfmall' in User_url:
        try:
            script_re = re.compile('(?<=image: \').*(?=\?)')
            Thumbnail_image_key = script_re.findall(str(soup))[0]                    
        except:    
            Thumbnail_image_key = Thumbnail_image_key             
            
    elif 'amazon' in User_url:  
        try: # referer 포함된 requests
            time.sleep(1)
#             headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)', 'Referer': 'https://www.naver.com/'}
#             res = requests.get(User_url, timeout=3, headers=headers) 
            soup = BeautifulSoup(res.text, 'html.parser')
            print('amazon referer 포함 requests 전송')
        except: # selenium
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('disable-gpu')
            options.add_argument('User-Agent: facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)')
            options.add_argument('lang = ko_KR')

            driver = webdriver.Chrome(chromedriver, options=options)
            driver.get(User_url)
            res = driver.page_source
            soup = BeautifulSoup(res, 'html.parser')
            script_re = re.compile('(?<=jQuery.parseJSON\(\').+(?=\'\);)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)
            driver.quit()
        try:
            Title_key = soup.select_one('meta[name="title"]')['content']
        except:
            try:
                Title_key = dict_result_script_text['title']
            except:
                Title_key = Title_key

        try:
            Description_key = soup.select_one('meta[name="description"]')['content']
        except:
            try:
                Description_key = dict_result_script_text['title']
            except:
                Description_key = Description_key

        try:
            Thumbnail_image_key = soup.select_one('div.imgTagWrapper img')['src']
        except:
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'amoremall' in User_url: 
        script = soup.select_one('script[type="application/json"]').text
        dict_result_script_text = json.loads(str(script))

        try:
            Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['onlineProdName']
        except:
            try:
                Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['prodName']
            except:
                try:
                    Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['products'][0]['prodName']
                except:
                    try:
                        Title_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productMeta']['title']
                    except:
                        Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['products'][0]['prodImages'][0]['imgUrl']
        except:
            try:
                Thumbnail_image_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['onlineProdImages'][0]['imgUrl']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productMeta']['image']
                except:
                    Thumbnail_image_key = Thumbnail_image_key

        try:
            Description_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['linePromoDesc']
        except:
            try:
                Description_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productMeta']['desc']
            except:
                Description_key = Description_key
                
    elif 'afreecatv' in User_url:
        if 'ogqmarket' in User_url:
            try:
                Title_key = soup.select_one('div.category').text + ' ' + soup.select_one('div.title').text
            except:
                Title_key = Title_key            
        else:
            script = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(str(script))
           
            try:
                Title_key = dict_result_script_text['name']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_text['description']
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key = dict_result_script_text['thumbnailUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key

    elif 'aladin' in User_url: 
        script = soup.select_one('script[type="application/ld+json"]').text
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_text['description']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_text['image']
        except:
            Thumbnail_image_key= Thumbnail_image_key

    elif 'albamon' in User_url:
        if len(Thumbnail_image_key)<28 :
            Thumbnail_image_key = 'https://mc.albamon.kr' + Thumbnail_image_key
            
    elif 'aboutpet' in User_url:
        if 'goods' in User_url:
            User_url = User_url.replace('goodsDetailShare', 'indexGoodsDetail')
            res = requests.get(User_url, headers=headers) 
            soup = BeautifulSoup(res.content, 'html.parser')
            
            script_re = re.compile('(?<=\"name\": ).*(?=,)')
            Title_key = script_re.findall(str(soup))[0].strip('"')

            script_re = re.compile('(?<=category\":).*(?=,)')
            Description_key = script_re.findall(str(soup))[0].strip('"')

            script_re = re.compile('(?<=var shareImg \= ).*(?=;)')
            Thumbnail_image_key = script_re.findall(str(soup))[0].strip("'")

        elif 'event' in User_url:
            
            script_re = re.compile('(?<=exhibitionName :).+(?=,)')
            Title_key1 = script_re.findall(str(soup))[0]
            Title_key = re.sub('\'','',Title_key1)
            
            Thumbnail_image_key = soup.select_one('img.img.mo')['src']
        else:
            Title_key = Title_key
            Description_key = Description_key
            Thumbnail_image_key = Thumbnail_image_key
            
    elif 'a-bly' in User_url:
            product_id_alby_re = re.compile('(?<=goods\/)[0-9]+')
            product_id_alby = product_id_alby_re.findall(User_url)[0]

            User_url_api = 'https://api.a-bly.com/webview/goods/' + str(product_id_alby)
            headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)', 'Referer': 'https://www.naver.com/'}
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 

            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")

            result_dict = json.loads(res_api.text)
            try:
                Title_key = result_dict['goods']['name']
            except:
                Title_key = Title_key
                
    elif 'encar' in User_url:
        product_id_encar_re = re.compile('(?<=carid=).+')
        product_id_encar = product_id_encar_re.findall(User_url)[0]

        User_url_api = 'http://www.encar.com/dc/dc_cardetailview.do?method=ajaxInspectView&rgsid=' + str(product_id_encar)+ '&sdFlag=N'
        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
     
        result_dict = json.loads(res_api.text)
        try:
            Title_manufacturerNm = result_dict[0]['inspect']['carSaleDto']['manufacturerNm']
            Title_modelNm = result_dict[0]['inspect']['carSaleDto']['modelNm']
            Title_badgeNm = result_dict[0]['inspect']['carSaleDto']['badgeNm']
            if Title_badgeNm == None:
                Title_badgeNm = ''
            Title_badgeDetailNm = result_dict[0]['inspect']['carSaleDto']['badgeDetailNm']
            if Title_badgeDetailNm == None:
                Title_badgeDetailNm = ''
                
            Title_key = Title_manufacturerNm + ' ' + Title_modelNm + ' ' + Title_badgeNm + ' ' + Title_badgeDetailNm
        except:
            Title_key = Title_key     

    elif 'yes24' in User_url:
        if 'Expectation' in User_url:
            Title_key = Description_key
            
        else:
            script = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(str(script))
            
            try:
                Title_key = dict_result_script_text['name']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_text['description']
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key = dict_result_script_text['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key
            
    elif 'ohou' in User_url:
        script = soup.select_one('div[data-react-class="App"]')['data-react-props']
        dict_result_script_text = json.loads(str(script))
        try:
            Title_key = dict_result_script_text['additional_data'][1]['data']['production']['name']
        except:
            Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_text['additional_data'][1]['data']['production']['image_url']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif Distributor_key in ['auction']:  
        if 'mobile.' in User_url:
            mobile_action_re = re.compile('(?<=var scheme_url = ).+(?=\;)')
            mobile_action = mobile_action_re.findall(str(soup))[0].strip("'")
            User_url = str(mobile_action)

            res = requests.get(User_url, timeout=3, headers=headers) 
            soup = BeautifulSoup(res.text, 'html.parser')

            script_re = re.compile('(?<=Request.Item= ).+(?=,)') 
            script_text1 = script_re.findall(str(soup))[0] + str("}")
            script_text = script_text1.replace("\'", '\"')
            dict_result_script_text = json.loads(script_text)

            try:
                Title_key = dict_result_script_text['itemName']
            except:
                Title_key = Title_key
                
        elif 'ticket.' in User_url:
            script = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(str(script))
            try:
                Title_key = dict_result_script_text['name']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key = dict_result_script_text['image'][0]
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
            
        elif 'itempage' in User_url:
            script_re = re.compile('(?<=Request.Item= ).+(?=,)') 
            script_text1 = script_re.findall(str(soup))[0] + str("}")
            script_text = script_text1.replace("\'", '\"')
            dict_result_script_text = json.loads(script_text)

            try:
                Title_key = dict_result_script_text['itemName']
            except:
                Title_key = Title_key
        else:
            script_re1 = re.compile('(?<=DetailLayer\.GetGroupList = function\(element, mItemNo, sItemNo, itemIndex\)).+(?=success: function\(res)', re.DOTALL)
            script_text1 = script_re1.findall(str(soup))[0]
            script_re2 = re.compile('(?<=data: \"\{\'groupList\': \'\" \+ \').+(?=\' \+ )')
            script_text2 = script_re2.findall(script_text1)[0]
            dict_result_script_text = json.loads(script_text2)[0]

            try:
                Title_key = dict_result_script_text['ItemName']
            except:
                Title_key = Title_key

            try:
                Thumbnail_image_key = dict_result_script_text['ThumbImageUrl']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['GalleryImageUrl']
                except:
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'elandmall' in User_url:

        try:
            Title_key = soup.select_one('meta[recopick:title"]')['content']
        except: 
            try:
                Title_key = soup.select_one('meta[property="og:description"]')['content'] 
            except:
                Title_key = Title_key

    elif 'book.interpark' in User_url:
        if 'product' in User_url:
            try:
                Title_key =  soup.select_one('h2').get_text()
            except:
                Title_key = Title_key 


    elif 'interpark' in User_url:
        if 'ticket' in User_url:
            product_id_ticketip_re = re.compile('(?<=goods\/)\d+')
            product_id_ticketip = product_id_ticketip_re.findall(User_url)[0]
            User_url_api = 'https://api-ticketfront.interpark.com/v1/goods/' + str(product_id_ticketip) + '/summary?goodsCode=22004761&priceGrade=&seatGrade='
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)
            try:
                Title_key = result_dict['data']['goodsName']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key = result_dict['data']['goodsLargeImageUrl']
            except: 
                Thumbnail_image_key = Thumbnail_image_key
                
        elif 'voucher' in User_url:
            product_voucherip_re = re.compile('(?<=goods\/).+')
            product_voucherip = product_voucherip_re.findall(User_url)[0]
            User_url_api = 'https://travel.interpark.com/api/voucher/v1/goods/getGoodsDetail/' + str(product_voucherip) + '?mobileYn=N'
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)
            try:
                Title_key = result_dict['data']['goodsNm']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key = result_dict['data']['imageList'][0]['dspImgUrl']
            except: 
                Thumbnail_image_key = Thumbnail_image_key

        elif 'live' in User_url:
            try:
                Thumbnail_image_key = 'https:'+ soup.select_one('div.prdImg > img')['src']
            except:
                try:
                    Thumbnail_image_key = 'https:' + soup.select_one('meta[property="og:image"]')['content']
                except: 
                    Thumbnail_image_key = Thumbnail_image_key

        elif 'product'in User_url:
            script_re = re.compile('(?<=is\.product\.info\.init\()(.*?)(?=, __EGS_DATAOBJ)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)
            try:
                Title_key = dict_result_script_text['prdNm']
            except:
                try:
                    Title_key = soup.select_one('meta[property="rb:itemName"]')['content']
                except:
                    Title_key = Title_key
            try:
                Thumbnail_image_key = dict_result_script_text['mainImg']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_text['icnImg']
                except:
                    try:
                        Thumbnail_image_url = soup.select_one('meta[property="rb:itemImage"]')['content']              
                        Thumbnail_image_key = 'http:' + Thumbnail_image_url 
                    except:
                        Thumbnail_image_key = Thumbnail_image_key
            try:
                Description_key = dict_result_script_text['brandNm']
            except:
                Description_key = Description_key

    elif 'cabinService' in User_url:
        if 'jejuair' in User_url:
            try: 
                Title_key = soup.select_one('div.page-title').get_text()
            except:
                Title_key= Title_key 

    elif 'zigbang' in User_url:
        try: 
             Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
             Title_key = Title_key         
        try: 
            Description_key= soup.select_one('meta[property="og:description"]')['content']     
        except:
             Description_key = Description_key

    elif 'jinair' in User_url:
        try:
            jinair_content= soup.find('h4',{'class':'info_title'})
            Title_key = jinair_content.text.split('\n')[2]
            Thumbnail_image_ad = soup.select_one('#_TRK_PN_ID')['src']  
            Thumbnail_image_key = 'https://jinistore.jinair.com/'+ (Thumbnail_image_ad)
        except:
            Title_key = Title_key 
            Thumbnail_image_key = Thumbnail_image_key

    elif 'ggumim' in User_url:
        try: 
            content_ggumim = soup.find_all('script', {'type':'application/json'})[0]
            content_ggumim_re = json.loads(content_ggumim.text)

            Title_key = content_ggumim_re['props']['pageProps']['qnaSolutionPageData']['title']
            Thumbnail_image_key = content_ggumim_re['props']['pageProps']['qnaSolutionPageData']['mainImage']
        except:
            Title_key  = Title_key 
            Description_key = Description_key
            Thumbnail_image_key = Thumbnail_image_key

        if 'furniture' in User_url:
            try: 
                content_ggumim = soup.find_all('script', {'type':'application/json'})[0]
                content_ggumim_re = json.loads(content_ggumim.text)

                Title_key = content_ggumim_re['props']['initialState']['app']['share']['title']
                Description_key = content_ggumim_re['props']['initialState']['app']['share']['Description']
                Thumbnail_image_key = content_ggumim_re['props']['initialState']['app']['share']['imageUrl']
            except:
                try:
                    Title_key = content_ggumim_re['props']['initialProps']['pageProps']['furnitureViewData']['furnitureName']
                except:
                    try:
                        Title_key = content_ggumim_re['furniture']['name']
                    except:
                        Title_key  = Title_key 
                        Description_key = Description_key
                        Thumbnail_image_key = Thumbnail_image_key

    elif 'tv.kakao' in User_url or 'entertain.daum' in User_url:
        if 'VIDEOSUS' in User_url:
            kakao_id_re = re.compile('(?<=cliplink/)\d+')
            kakao_id = kakao_id_re.findall(User_url)[0]
            User_url_api = 'https://tv.kakao.com/vapi/playlist/v2/main/404089/videos?videoId=' + str(kakao_id) + '&sort=order&size=20'
            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers)   
            result_dict = json.loads(res_api.text)
        # 타이틀
            try:
                Title_key = result_dict['list'][0]['programTitle']
            except:
                Title_key = Title_key
        #디스크립션                
            try:
                Description_key = result_dict['list'][0]['episodeTitle']
            except:
                Description_key = Description_key
        #썸네일                
            try:
                Thumbnail_image_key = result_dict['list'][0]['thumbnailUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key

        elif 'cliplink' in User_url or 'entertain.daum' in User_url:
            kakao_id_re = re.compile('[0-9]+$')
            kakao_id = kakao_id_re.findall(User_url)[0]
            User_url_api = 'https://play-tv.kakao.com/api/v1/ft/playmeta/cliplink/' + str(kakao_id) + '?fields=@html5vod&service=kakao_tv&type=VOD'
            res_api = requests.get(User_url_api, timeout=3, headers = headers)   
            result_dict = json.loads(res_api.text)
            try:
                Title_key = result_dict['kakaoLink']['templateArgs']['${title}']
            except:
                try: 
                    Title_key = result_dict['clipLink']['clip']['title']
                except: 
                    try:
                        Title_key = result_dict['clipLink']['displayTitle']
                    except:
                        Title_key = Title_key          
            try:
                Description_key = result_dict['clipLink']['channel']['description']
            except:
                Description_key = Description_key             
            try:
                Thumbnail_image_key = result_dict['kakaoLink']['templateArgs']['${thumbnailUrl}']
            except:
                try: 
                    Thumbnail_image_key = result_dict['clipLink']['clip']['thumbnailUrl']
                except: 
                    Thumbnail_image_key = Thumbnail_image_key
                    
        elif 'episodes' in User_url:
            kakao_id_re = re.compile('[0-9]+')
            kakao_id = kakao_id_re.findall(User_url)[0]
            User_url_api = 'https://tv.kakao.com/vapi/channel/v2/detail/' + str(kakao_id) + '/home?at=web'
            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers)   
            result_dict = json.loads(res_api.text)
            try:
                Title_key = result_dict['title']
            except:
                try: 
                    Title_key = result_dict['channelShare']['templateArgs']['${title}']
                except: 
                    Title_key = Title_key               
            try:
                Description_key = result_dict['channelShare']['templateArgs']['$${synopsis}']
            except:
                Description_key = Description_key                
            try:
                Thumbnail_image_key = result_dict['channelShare']['templateArgs']['${thumbnailUrl}']
            except:
                try: 
                    Thumbnail_image_key = result_dict['channelCover']['coverImageUrl']
                except: 
                    Thumbnail_image_key = Thumbnail_image_key
                    
        else:
            script = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(str(script))
            try:
                Title_key = dict_result_script_text['name']
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_text['description']
            except:
                Description_key = Description_key
            try:
                Thumbnail_image_key = dict_result_script_text['thumbnailUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'map.kakao' in User_url:
        try:
            Title_key = Title_key + str(" ,") + Description_key
        except:
            pass
        
    elif 'twayair' in User_url:
        try: 
             Title_key = soup.select_one('#content > div.section.t3 > div > div.grid_view_head.evt > h3').text
        except:
             Title_key = Title_key 

    elif 'costco' in User_url:
        if 'campaign' in User_url:
            try:
                Title_key = soup.select_one('div.event_coupon img')['alt']
            except:
                try:
                    Title_key = soup.select_one('div.onlinevoucher_event_title').text
                except:
                    Title_key = Title_key
            try:
                Thumbnail_image_key = soup.select_one('meta[name="thumbnail"]')['content']
            except:
                Thumbnail_image_key = Thumbnail_image_key
        else:
            script = soup.select_one('script#schemaorg_product').text
            dict_result_script_text = json.loads(str(script))
            try:
                Title_key = dict_result_script_text['name']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key = dict_result_script_text['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key   
            try:
                Description_key = dict_result_script_text['description']
            except:
                Description_key = Description_key

    elif 'topten10mall' in User_url:

        try:
            Thumbnail_image_url = soup.select_one('meta[property="eg:itemImage"]')['content']
            product_id_topten_re = re.compile('(?<=/goods/)\w{13}')
            product_id_topten = product_id_topten_re.findall(Thumbnail_image_url)[0]
            Thumbnail_image_key = 'https://imgp.topten10mall.com/ssts/image/goods/'+ str(product_id_topten) +'_M?AR=0&RS=740x1010&appopen=new'
        except:
            Thumbnail_image_key = Thumbnail_image_key

        if 'event' in User_url:
            Title_key = soup.select_one('h3.text-small').text
        else:
            Title_key = Title_key

    elif 'pet-friends' in User_url:
        try: 
            content_petf = soup.find_all('script', {'type':'application/json'})[0]
            content_petf_re = json.loads(content_petf.text)

            Title_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaProductName']
            Description_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['description']
            Thumbnail_image_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['eigeneMetaData']['itemImage']
        except:
            try: 
                Title_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['productName']
            except:
                try:
                    Title_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['title']
                except:  
                    Description_key = Description_key
                    Thumbnail_image_key = Thumbnail_image_key

    elif 'houseapp' in User_url: 
        try:
            if 'plan' in User_url: 
                Title_key = soup.select_one('meta[property="og:title"]')['content']+ " " + soup.select_one('meta[property="og:description"]')['content']
                Description_key = soup.select_one('meta[property="og:description"]')['content']
                Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content'] 
            
            elif 'link' in User_url: 
                product_id_houseapp_re = re.compile('(?<=goods\/)\d+')
                product_id_houseapp = product_id_houseapp_re.findall(User_url)[0]
                User_url_new = 'https://store.houseapp.co.kr/goods/detail.do?goodsNo=' + str(product_id_houseapp) +'&goodsNo='+ str(product_id_houseapp) + '&popup=up'
                
                res_new = requests.get(User_url_new, timeout=3, headers = headers) 
                soup_re = BeautifulSoup(res_new.content,'html.parser')

                Title_key = soup_re.select_one('meta[property="og:title"]')['content']
                Description_key = soup_re.select_one('meta[property="og:description"]')['content']
                Thumbnail_image_key = soup_re.select_one('meta[property="og:image"]')['content']   
            else:
                Title_key = Title_key
                Description_key = soup.select_one('meta[property="og:description"]')['content']
                Thumbnail_image_key= Thumbnail_image_key
        except:
                Title_key = Title_key
                Description_key = Description_key
                Thumbnail_image_key= Thumbnail_image_key

    elif 'hanssem' in User_url:
        if 'homeIdea' in User_url:
            id_hanssem_re = re.compile('(?<=seq=)[0-9]+')
            id_hanssem =id_hanssem_re.findall(User_url)[0]

            User_url_hanssem_api = 'https://mall.hanssem.com/m/homeIdea/contents/selectDetailMaster.do'
       
            headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'authority': 'mall.hanssem.com',
            'method': 'POST',
            'scheme': 'https',
            'ajax': 'true',
            'path': '/m/homeIdea/contents/selectDetailMaster.do',
            'accept-language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '58',
            'content-type': 'application/json; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'origin': 'https://mall.hanssem.com',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://mall.hanssem.com/m/homeIdea/contents/homeIdeaDetail.do?seq=' + str(id_hanssem),
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36' 
            }

            payload = {'Seq': id_hanssem, 
                       'RowNum': '1', 
                       'PageRow': '10', 
                       'ContentsTypeCd': ' '}

            res = requests.post(User_url_hanssem_api, headers=headers, json = payload, timeout = 10)
            print(res.status_code)
            soup = BeautifulSoup(res.content,"html.parser")

            dict_post_api = json.loads(soup.text)
            
            try:
                Title_key = dict_post_api['MASTER']['Title']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key = dict_post_api['MASTER']['vrImgUrl']
            except:
                Thumbnail_image_key = Thumbnail_image_key 
                
        else:
            Title_key= Title_key
            Thumbnail_image_key = Thumbnail_image_key

    elif 'spooncast' in User_url:
        try:
            live_id_re = re.compile('(?<=live\/)[0-9]+')
            live_id = live_id_re.findall(User_url)[0]  
            User_url_api = 'https://kr-api.spooncast.net/lives/' + live_id          
        except:
            product_id_re = re.compile('(?<=products\/)[0-9]+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://kr-store-api.spooncast.net/v1/store/products/' + product_id              
        res_api = requests.get(User_url_api, timeout=3, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)


        try:
            Title_key = result_dict['results'][0]['title']
        except:
            try:
                Title_key = result_dict['title'] 
            except:
                Title_key = Title_key
        try:
            Description_key = result_dict['description']
        except:
            Description_key = Description_key
            
    elif 'boribori' in User_url:
        if 'product' in User_url:
            try:
                product_id_re = re.compile('(?<=productNo=).+')
                product_id = product_id_re.findall(User_url)[0]  
            except:
                product_id_re = re.compile('(?<=product\/)[0-9]+')
                product_id = product_id_re.findall(User_url)[0]          
            User_url_api = 'https://apix.halfclub.com/product/products/withoutPrice/' + str(product_id)+ '?_=&countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2'                      

            print(User_url_api)
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 

            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")

            result_dict = json.loads(res_api.text)

            try:
                Title_key = result_dict['data']['prdNm']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key_url = result_dict['data']['productImage']['basicExtNm']
                Thumbnail_image_key = 'https://cdn2.boribori.co.kr/rimg/500/'+ Thumbnail_image_key_url
            except:
                Thumbnail_image_key = Thumbnail_image_key
          
        elif 'deal' in User_url:
            product_id_re = re.compile('(?<=PrdNo=)\d+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://apix.halfclub.com/product/deal/' + str(product_id)+ '?countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2&ts=1660814208352'

            print(User_url_api)
            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
    
            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")
    
            result_dict = json.loads(res_api.text)
    
            try:
                Title_key = result_dict['data']['prdNm']
            except:
                Title_key = Title_key
            try:
                Thumbnail_image_key_url = result_dict['data']['productImage']['basicExtNm']
                Thumbnail_image_key = 'https://cdn2.boribori.co.kr/rimg/500//'+ Thumbnail_image_key_url
            except:
                Thumbnail_image_key = Thumbnail_image_key  
                
        elif 'magazine' in User_url:
            product_id_re = re.compile('(?<=cmntySeq=)\d+')
            product_id = product_id_re.findall(User_url)[0]  
            User_url_api = 'https://cf-api.halfclub.com/community/community/magazine/info?cmntySeq=' + str(product_id)+ '&siteCode=2'

            print(User_url_api)
            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
    
            if res_api.status_code != 200:
                print("User_url_api 접속 오류입니다")
    
            result_dict = json.loads(res_api.text)
    
            try:
                Title_key = result_dict['data']['title']
            except:
                Title_key = Title_key
                
        else:
            try:
                product_id_re = re.compile('(?<=plan\/).+')
                product_id = product_id_re.findall(User_url)[0]  
                User_url_api = 'https://apix.halfclub.com/display/plans/' + str(product_id)+ '?apiFlag=true&countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&prdFlag=false&siteCd=2'

                print(User_url_api)
                res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                if res_api.status_code != 200:
                    print("User_url_api 접속 오류입니다")

                result_dict = json.loads(res_api.text)

                try:
                    Title_key = result_dict['data'][0]['planNm']
                except:
                    Title_key = Title_key  
            except:
                pass

    elif 'sonohotelsresorts' in User_url:
        try:
            product_id_sonohotel_re = re.compile('(?<=detail\/).+')
            product_id_sonohotel = product_id_sonohotel_re.findall(User_url)[0]
            User_url_sonohotel_api = 'https://m.sonohotelsresorts.com/api/v1/hp/eventInfo/event-detail'
            
            payload = {
            'board_no': str(product_id_sonohotel), #product_id
            'mem_no': ""
            }
        except:
            product_id_sonohotel_re = re.compile('(?<=package\/).+')
            product_id_sonohotel = product_id_sonohotel_re.findall(User_url)[0]
            User_url_sonohotel_api = 'https://m.sonohotelsresorts.com/api/v1/ms/package/detail'
            
            payload = {
            'pkg_sid': str(product_id_sonohotel), #product_id
            }
            
        res = requests.post(User_url_sonohotel_api, json = payload, timeout = 10) 
        result_dict = json.loads(res.text)
        
        try:
            Title_key = result_dict ['result']['resDetail']['fEvtTitle']
        except:
            try:
                Title_key = result_dict ['result'][0]['PKG_TITLE']
            except:
                Title_key = Title_key 
    
        try:
            Description_key = result_dict ['result']['resDetail']['fEvtClass']
        except:
            try:
                Description_key = result_dict['result'][0]['PKG_COM']
            except:
                Description_key = Description_key 
    
        try:
            Thumbnail_image_url = result_dict ['result']['resDetail']['fEvtImgUrl']
            Thumbnail_image_key = 'https://m.sonohotelsresorts.com/upload/image/evt/dmEvt_202207190456206101'+ Thumbnail_image_url
    
        except:
            Thumbnail_image_key = Thumbnail_image_key  

    elif 'cuchenmall' in User_url:
        res = requests.get(User_url, timeout=5, headers = headers, verify = False) 
        soup = BeautifulSoup(res.text, 'html.parser')
        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            try:
                Title_key = soup.select_one('div:nth-child(2) > h2').text
            except:
                try:
                    Title_key = soup.select_one('div.winner_view_tit > h2').text    
                except:
                    Title_key = Title_key
        try:
            Description_key = soup.select_one('meta[property="og:description"]')['content']  
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
        except:
            try:
                script_re = re.compile('(?<=product_image_URL1 =).+(?=;)')
                Thumbnail_image1 =  script_re.findall(str(soup))[1]
                Thumbnail_image_key = re.sub('\'',' ', Thumbnail_image1)     
            except:
                Thumbnail_image_key = Thumbnail_image_key 
    
    elif 'coupangplay' in User_url: 
        if 'app.link' in User_url:
            product_id_link = soup.select_one('link[rel = "alternate"]')
            product_id_re = re.compile('(?<=title_id=).+(?=&amp;_)')
            product_id = product_id_re.findall(str(product_id_link))[0]
        else:
            product_id_re = re.compile('(?<=titles\/).+(?=\?live)')
            product_id = product_id_re.findall(str(User_url))[0]

        User_url_api = 'https://discover.coupangstreaming.com/v1/discover/titles/' + str(product_id)
        print(User_url_api)

        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        soup_api = BeautifulSoup(res_api.text, 'html.parser')
        dict_result_script_api = json.loads(str(soup_api))

        try:
            Title_key = dict_result_script_api['data']['title']
        except:
            try:
                Title_key = dict_result_script_api['data']['title_canonical']
            except:
                Title_key = Title_key
        try:
            Thumbnail_image_key = dict_result_script_api['data']['images']['background']['url']
        except:
            try:
                Thumbnail_image_key = dict_result_script_api['data']['images']['hero']['url']
            except:
                try:
                    Thumbnail_image_key = dict_result_script_api['data']['images']['poster']['url']
                except:
                    Thumbnail_image_key = Thumbnail_image_key
        try:
            Description_key = dict_result_script_api['data']['short_description']
        except:
            try:
                Description_key = dict_result_script_api['data']['description']
            except:
                Description_key = Description_key
            
    elif Distributor_key in ['wavve']:
        if 'vod' in User_url:
            vod_id_wavve_re = re.compile('(?<=contentid=).+')
            vod_id_wavve = vod_id_wavve_re.findall(User_url)[0]
            
            User_url_api = 'https://apis.wavve.com/fz/vod/contents/' + str(vod_id_wavve)+'?apikey=0&credential=none&device=pc&drm=wm&partner=pooq&pooqzone=none&region=kor&targetage=all'
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 

            result_dict = json.loads(res_api.text)
      
            try:
                Title_key = result_dict['programtitle'] + ' ' + result_dict['episodenumber']+'회' 
            except:
                Title_key = Title_key      
            try:
                Description_key= result_dict['programsynopsis']
            except:
                Description_key = Description_key
                
            try:
                Thumbnail_image_key = result_dict['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                     
        elif 'movie' in User_url:
            movie_id_wavve_re = re.compile('(?<=movieid=).+')
            movie_id_wavve = movie_id_wavve_re.findall(User_url)[0]
            
            User_url_api = 'https://apis.wavve.com/fz/movie/contents/' + str(movie_id_wavve)+'?apikey=0&credential=none&device=pc&drm=wm&partner=pooq&pooqzone=none&region=kor&targetage=all'
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            
            
            result_dict = json.loads(res_api.text)
      
            try:
                Title_key = result_dict['title'] 
            except:
                Title_key = Title_key     
            try:
                Description_key= result_dict['synopsis']
            except:
                Description_key = Description_key
                
            try:
                Thumbnail_image_key = result_dict['image']
            except:
                Thumbnail_image_key = Thumbnail_image_key
                
    elif 'work.go' in User_url: 
        job_id_worknet_re = re.compile('(?<=AuthNo=)[0-9]+')
        job_id_worknet =job_id_worknet_re.findall(User_url)[0]
        typeNm_worknet_re = re.compile('(?<=typeNm=)\w+')
        typeNm_worknet =typeNm_worknet_re.findall(User_url)[0]
        
        User_url_worknet_api = 'https://m.work.go.kr/regionJobsWorknet/selectJobDetailMulti.do'

        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'm.work.go.kr',
        'Connection': 'Keep-Alive',
        'content-type': 'application/json;charset=UTF-8',
        # 'cookie' : 'PCID=16595005699130942493404; WMONID=-EwLJaUrDU3; SSCSID=MSVC21&&0SrnCXJmw8Q7RegqKNWOcNC3X2MwlDm4rb79Ec90d4l8iBAYQmzW!-862503489!1661733532262; MOBILESERVICESESSION=0SrnCXJmw8Q7RegqKNWOcNC3X2MwlDm4rb79Ec90d4l8iBAYQmzW!-862503489'
        'origin': 'https://m.work.go.kr',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36' 
        }

        payload = {
        'srchWantedAuthNo': job_id_worknet, #product_id
        'srchInfotypeNm': typeNm_worknet,
        'preUrl': '/main.do',
        'retUrl': User_url
        }

        res = requests.post(User_url_worknet_api, headers=headers, json =  payload, timeout = 10) 
        soup = BeautifulSoup(res.content,"html.parser")
 
        dict_post_api = json.loads(soup.text)
 
        
        try:
            Title_key = dict_post_api['data'][0]['openEmpInfo']['empBusiNm']+ dict_post_api['data'][0]['openEmpInfo']['empWantedTitle']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_post_api['data'][0]['metaDescription']
        except:
            Description_key = Description_key
            
    elif 'hotels' in User_url:
        try:
            hotels_url = soup.select_one('link[rel="canonical"]')['href']

            res_canonical = requests.get(hotels_url, timeout=3, headers=headers) 

            soup = BeautifulSoup(res_canonical.text, 'html.parser')

            Thumbnail_image_key = soup.find_all('img', attrs = {'class':'uitk-image-media'})[1]['src'] 
        except:           
            Thumbnail_image_key = Thumbnail_image_key   
            
    elif 'hiver'in User_url:
        if 'onelink' in User_url:
            try: 
                product_id_hiver_re = re.compile('(?<=id=)\d+')
                product_id_hiver = product_id_hiver_re.findall(User_url)[0]
                User_url_api = 'https://www.hiver.co.kr/products/b/' + str(product_id_hiver) 
                res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                soup = BeautifulSoup(res_api.content, 'html.parser')
            except:
                pass
        content_hiver = soup.find_all('script', {'type':'application/json'})[0]

        content_hiver_re = json.loads(content_hiver.text)
  
        try:
            Title_key = content_hiver_re['data']['name']
        except: 
            Title_key = Title_key

        try:
            Thumbnail_image_key = content_hiver_re['data']['image_thumbnail_url']
        except:
            Thumbnail_image_key =Thumbnail_image_key 
                                          
    elif 'tiffany'in User_url: 
        try: 
            Thumbnail_image_key = "http:"+ soup.select_one('meta[property="og:image"]')['content']

        except:
            Thumbnail_image_key = Thumbnail_image_key 
            
    elif 'tmon' in User_url: 
        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            Title_key = Title_key
            
    elif 'halfclub' in User_url:
        if 'plan' in User_url:
            product_id_re = re.compile('(?<=plan\/).+')
            product_id = product_id_re.findall(User_url)[0]  
               
            User_url_api = 'https://apix.halfclub.com/display/plans/' + str(product_id)+ '?apiFlag=true&countryCd=001&deviceCd=001&langCd=001&mandM=halfclub&prdFlag=false&siteCd=1'                      

            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 

            result_dict = json.loads(res_api.text)

            try:
                Title_key = result_dict['data'][0]['planNm']
            except:
                Title_key = Title_key
                
        elif 'productNo' in User_url:
            product_id_re = re.compile('(?<=productNo=).+')
            product_id = product_id_re.findall(User_url)[0]  
               
            User_url_api = 'https://apix.halfclub.com/product/products/withoutPrice/' + str(product_id)+ '?_=&countryCd=001&deviceCd=001&langCd=001&mandM=halfclub&siteCd=1'                      

            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)

            try:
                Title_key = result_dict['data']['prdNm']
                Thumbnail_image_key =  'http://cdn2.halfclub.com/rimg/500/'+ result_dict['data']['productImage']['basicExtNm']
            except:
                Title_key = Title_key  
                Thumbnail_image_key = Thumbnail_image_key
                
                
        elif 'deal' in User_url:
            product_id_re = re.compile('(?<=PrdNo=)\d+')
            product_id = product_id_re.findall(User_url)[0]  
               
            User_url_api = 'https://apix.halfclub.com/product/deal/' + str(product_id)+ '?countryCd=001&deviceCd=001&langCd=001&mandM=halfclub&siteCd=1&ts='                      

            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)

            try:
                Title_key = result_dict['data']['prdNm']
                Thumbnail_image_key =  'http://cdn2.halfclub.com/rimg/500/'+ result_dict['data']['productImage']['basicExtNm']
            except:
                Title_key = Title_key  
                Thumbnail_image_key = Thumbnail_image_key 
        else:
            Title_key = Title_key  
            Thumbnail_image_key = Thumbnail_image_key 
            
    elif 'ticketlink' in User_url:
        if 'event' in User_url:
            id_ticketlink_re = re.compile('(?<=event\/).+')
            id_ticketlink = id_ticketlink_re.findall(User_url)[0]

            User_url_api = 'https://mapi.ticketlink.co.kr/mapi/sports/category/event/' + str(id_ticketlink)
            
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)
           
            try:
                Title_key = result_dict['data']['title']
            except:
                Title_key =Title_key 
                
    elif 'triple' in User_url:
        content_triple_re = soup.find_all('script', {'type':'application/json'})[0]
        content_triple = json.loads(content_triple_re.text)
        try:    
            Thumbnail_image_key = content_triple['props']['pageProps']['product']['images'][0]['sizes']['smallSquare']['url']
        except:
            Thumbnail_image_key = Thumbnail_image_key 

    elif 'shop.tworld' in User_url:
        product_id_tdirectshop_re = re.compile('(?<=detail\?).+')
        product_id_tdirectshop = product_id_tdirectshop_re.findall(User_url)[0]

        User_url_api = 'https://shop.tworld.co.kr/api/wireless/childProductList?' + str(product_id_tdirectshop)
        print(User_url_api)
        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        script_api = BeautifulSoup(res_api.text, 'html.parser').text
        dict_result_script_api = json.loads(script_api)

        try:
            Title_key = dict_result_script_api['childList'][0]['productGrpNm']
        except:
            try:
                Title_key = dict_result_script_api['childList'][0]['modelName']
            except:
                Title_key = Title_key
        try:
            Thumbnail_image_key = 'https://cdnw.shop.tworld.co.kr/pimg/phone/' + dict_result_script_api['childList'][0]['mimage1']
        except:
            try:
                Thumbnail_image_key = soup.select_one('div.viewer-img > img')['src']
            except:
                Thumbnail_image_key = Thumbnail_image_key
     
                
    
    
    elif Distributor_key in ['booking']:
        script_re = re.compile('(?<=primaryPhoto\":).*(?=,\"ranking)')
        script_text= script_re.findall(str(soup))[0] 
        dict_script_text = json.loads(script_text)
        try:
            Thumbnail_image_key = dict_script_text['small']    
        except:
            Thumbnail_image_key = Thumbnail_image_key 

    elif 'lotteon' in User_url:
        product_id_lotteon1_re = re.compile('(?<=sitmNo=).+(?=&mall_no)')
        product_id_lotteon1 =product_id_lotteon1_re.findall(User_url)[0]
        product_id_lotteon2_re = re.compile('(?<=sitmNo=).+')
        product_id_lotteon2 = product_id_lotteon2_re.findall(User_url)[0]

        User_url_api = 'https://pbf.lotteon.com/product/v2/detail/search/base/sitm/' + str(product_id_lotteon1) + '?sitmNo=' + str(product_id_lotteon2) + '&isNotContainOptMapping=true'

        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        script_api = BeautifulSoup(res_api.text, 'html.parser').text
        dict_result_script_api = json.loads(script_api)

        try:
            Title_key = dict_result_script_api['data']['basicInfo']['pdNm']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_api['data']['basicInfo']['categoryBestText']
        except:
            Description_key = Description_key
        try:
            Thumbnail_image_key = dict_result_script_api['data']['imgInfo']['imageList'][0]['origImgFileNm']
        except:
            Thumbnail_image_key = Thumbnail_image_key

    elif 'shoppinghow' in User_url:
        product_id_shoppinghow_re = re.compile('(?<=product\/).[0-9]+')
        product_id_shoppinghow = product_id_shoppinghow_re.findall(User_url)[0]

        User_url_api = 'https://shoppinghow.kakao.com/siso/p/api/product/malllist?modelId=' + str(product_id_shoppinghow)

        res_api = requests.get(User_url_api, timeout=3, headers=headers) 
        script_api = BeautifulSoup(res_api.text, 'html.parser').text
        dict_result_script_api = json.loads(script_api)

        print(User_url_api)
        try:
            Title_key = dict_result_script_api['mallList'][0]['name']
        except:
            Title_key = Title_key
        try:
            Description_key = dict_result_script_api['mallList'][0]['cpName']
        except:
            Description_key = Description_key

    elif 'daum' in User_url:
        if 'finance' in User_url:
            product_id_finance_daum_re = re.compile('(?<=quotes\/).[0-9]+')
            product_id_finance_daum = product_id_finance_daum_re.findall(User_url)[0]

            User_url_api = 'https://finance.daum.net/api/quotes/' + str(product_id_finance_daum) + '?changeStatistics=true&chartSlideImage=true&isMobile=true'
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36', 'Referer': 'https://www.naver.com/'}
            res_api = requests.get(User_url_api, timeout=3, headers=headers) 
            script_api = BeautifulSoup(res_api.text, 'html.parser').text
            dict_result_script_api = json.loads(script_api)

            try:
                Title_key = dict_result_script_api['name'] + ' | 다음 금융'
            except:
                Title_key = Title_key
            try:
                Description_key = dict_result_script_api['companySummary']
            except:
                try:
                    Description_key = dict_result_script_api['sectorName']
                except:
                    Description_key = Description_key
                    
        elif 'gallery' in User_url:
            try:
                image_daumcdn = soup.select_one('meta[property="og:image"]')['content']
                image_daumcdn_re = re.compile('(?<=fname=).+')
                Thumbnail_image_key = image_daumcdn_re.findall(str(image_daumcdn))[0]
            except:
                pass

    elif 'kbland' in User_url: 
        kbland_id_re = re.compile('(?<=c\/|p\/)\d+')
        kbland_id = kbland_id_re.findall(User_url)[0]
        
        kbland_type_re = re.compile('(?<=ctype=)\d+')
        kbland_type = kbland_type_re.findall(User_url)[0]
        try:
            User_url_api = 'https://api.kbland.kr/land-complex/complex/main?%EB%8B%A8%EC%A7%80%EA%B8%B0%EB%B3%B8%EC%9D%BC%EB%A0%A8%EB%B2%88%ED%98%B8='+kbland_id+'&%EB%A7%A4%EB%AC%BC%EC%A2%85%EB%B3%84%EA%B5%AC%EB%B6%84='+ kbland_type
            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
            result_dict = json.loads(res_api.text)
            Title_key = result_dict['dataBody']['data']['단지명']
        except:
            try:
                User_url_api = 'https://api.kbland.kr/land-property/property/bascInfo?%EB%A7%A4%EB%AC%BC%EC%9D%BC%EB%A0%A8%EB%B2%88%ED%98%B8='+kbland_id+'&%EB%A7%A4%EB%AC%BC%EB%85%B8%EC%B6%9C%EC%9A%94%EC%B2%AD=Y'
                res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                result_dict = json.loads(res_api.text)
                Title_key = result_dict['dataBody']['data']['bascInfo']['매물명']                
            except:    
                Title_key = Title_key
            
        try:
            pic_url_api = 'https://api.kbland.kr/land-complex/complex/phtoList?%EB%8B%A8%EC%A7%80%EA%B8%B0%EB%B3%B8%EC%9D%BC%EB%A0%A8%EB%B2%88%ED%98%B8='+kbland_id
            pic_res_api = requests.get(pic_url_api, timeout=3, headers = headers) 
            pic_result_dict = json.loads(pic_res_api.text)
            Thumbnail_image_key = pic_result_dict['dataBody']['data'][0]['전체이미지경로_1920']
        except:
            Thumbnail_image_key = Thumbnail_image_key       

    elif 'gap.com'in User_url: 
        try:                    
            content_gap_re = soup.find_all('script', {'type':'application/ld+json'})[0]
            content_gap = json.loads(content_gap_re.text)
            Thumbnail_image_key = content_gap[0]['offers'][0]['itemOffered']['image']    
        except:
            Thumbnail_image_key = Thumbnail_image_key
                                  
    elif 'theory'in User_url: 
        try:
            Thumbnail_image_key = soup.select_one('img[itemprop="image"]')['src']               
        except:
            Thumbnail_image_key = Thumbnail_image_key    
            
    elif 'peterpanz'in User_url: 
        try:
            Title_key = Title_key_og
        except:
            Title_key = Title_key
            
    elif 'sooldamhwa'in User_url:    
        script_text = soup.select_one('script[type="application/json"]').text
        dict_result = json.loads(script_text)
        try:
            Title_key = dict_result['props']['pageProps']['metaTags']['title']
        except:
            try:
                Title_key = dict_result['props']['pageProps']['initialState']['damhwaMarket']['product']['name']
            except:
                Title_key = Title_key
        try:
            Description_key = dict_result['props']['pageProps']['initialState']['damhwaMarket']['product']['damhwaNote']
        except:
            try:
                Description_key = dict_result['props']['pageProps']['metaTags']['description']
            except:
                try:
                    Description_key = dict_result['props']['pageProps']['initialState']['damhwaMarket']['product']['subText']
                except:
                    Description_key = Description_key
                
#3요소소
            
##코리아센터 (메이크샵)공통 -------------------------------------------------------------------------
    
    elif 'branduid'in User_url:
        
        name_makeshop = re.compile('http.*kr|http.*com')
        url_name_makeshop = name_makeshop.findall(User_url)[0]
        
        try:
            script_re = re.compile('(?<=var product_name =).+(?=;)')
            Title_key_re = script_re.findall(str(soup))[0]
            Title_key = Title_key_re.replace("'",'')
        except:
            Title_key = Title_key 
            
        try:
            Thumbnail_image_tempo = soup.find('div','product-info').find('img')['src']
        except:
            try:
                Thumbnail_image_tempo = soup.find('div','shopdetailInfoTop').find('img')['src']
            except:
                script_re = re.compile('(?<=imageUrl : ").+(?=" \+ "\?random)')
                Thumbnail_image_tempo =  script_re.findall(str(soup))[0]
         
        if Thumbnail_image_tempo.startswith('/shopimages') == True:
            Thumbnail_image_key = url_name_makeshop + Thumbnail_image_tempo
        else:
            Thumbnail_image_key = Thumbnail_image_tempo

     
    
#NHN 고도샵 공통 -------------------------------------------------------------------------
    
    elif 'goods_view'in User_url:
        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            try:
                Title_key = soup.select_one('meta[name="twitter:title"]')['content']
            except:
                Title_key = Title_key     
                
                
#카페24 공통 -----------------------                              
                
    elif (cafe24_url != None) or ('detail.html' in User_url):  
        try:
            Title_key_1 = soup.select('meta[property="og:title"]')[0]['content']
            if len(Title_key_1) < 4 :                
                Title_key = soup.select('meta[property="og:title"]')[1]['content']
            else:
                Title_key = Title_key_1 
        except:
            Title_key = Title_key
            
        try:
            Thumbnail_image_key = soup.select('meta[property="og:image"]')[1]['content']
        except:
            try:
                Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
            except:
                try:
                    Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content'] 
                except:
                    try:
                        Thumbnail_image_key = soup.select_one('meta[property="recopick:image"]')['content'] 
                    except:
                        try:
                            Thumbnail_image_key = soup.select_one('meta[name="twitter:image"]')['content'] 
                        except:          
                            Thumbnail_image_key = Thumbnail_image_key             
                            
#가비아 퍼스트몰 공통 -------------------------------------------------------------------------
    
    elif 'view?no'in User_url:
        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            Title_key = Title_key 

        try:
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
        except:
            Thumbnail_image_key = Thumbnail_image_key      
            
except:
    Title_key = Title_key
    Description_key = Description_key
    Thumbnail_image_key = Thumbnail_image_key

# Duration_key 설정
if Type_key == '동영상':
    if Distributor_key == "youtube":
        try:
            Duration_key = soup.select_one(
                'meta[itemprop="duration"]')['content']
            Duration_key = Duration_key.replace(
                "PT", "").replace("M", "분 ").replace("S", "초")
        except:
            Duration_key = "해당 링크에서 직접 보기"
    elif Distributor_key == "naver":
        try: # naver.com/vod 
            script_re = re.compile('(?<=vod = ).+(?=;)')
            script_text = script_re.findall(str(soup))[0]
            dict_result_script_text = json.loads(script_text)

            Title_key = dict_result_script_text['title']

            Thumbnail_image_key = dict_result_script_text['thumbnail']

            Description_key = dict_result_script_text['searchData']

            try:
                Duration_key = dict_result_script_text['playTime']
            except:
                try:
                    Duration_key = str(dict_result_script_text['playTimeMinute']) + '분' + str(dict_result_script_text['playTimeSecond']) +'초'
                except:
                    try:
                        Duration_key = str(dict_result_script_text['playTimeToSecond']) + '초'
                    except:
                        Duration_key = "해당 링크에서 직접 보기"

        except: # tv.naver.com
            try:
                Duration_key = soup.select_one('em.time').text
            except:
                try:
                    Duration_key = soup.select_one('meta[property="naver:video:play_time"]')['content']
                except:
                    Duration_key = "해당 링크에서 직접 보기"
                    
    elif Distributor_key == "afreecatv":
        try:
            script = soup.select_one('script[type="application/ld+json"]').text
            dict_result_script_text = json.loads(str(script))

            Duration_key = dict_result_script_text['duration']
            Duration_key = int(re.sub(r'(\D)', '', Duration_key))
            Duration_key_minute, Duration_key_second= divmod(Duration_key, 60)

            Duration_key = str(Duration_key_minute) + '분 ' + str(Duration_key_second) + '초'
        except:
            Duration_key = "해당 링크에서 직접 보기"

    elif Distributor_key == "coupangplay":
        try:
            Duration_key = dict_result_script_api['data']['running_time_friendly'].replace("h", "시간").replace("m", "분 ").replace("s", "초")
        except:
            try:
                Duration_key = str(round(int(dict_result_script_api['data']['running_time'])/60)) + '분'
            except:
                Duration_key = "해당 링크에서 직접 보기"
                
    elif Distributor_key == "kakao" or Distributor_key == "daum":
        try:
            Duration_key = result_dict['clipLink']['clip']['duration']
            Duration_key1, Duration_key2 = divmod(int(Duration_key), 60)
            Duration_key = str(Duration_key1) +'분 ' + str(Duration_key2) + '초' 
        except:
            try:    
                Duration_key = dict_result_script_text['duration']
                Duration_key = Duration_key.replace("PT", "").replace("H", "시간").replace("M", "분").replace("S", "초") 
            except:
                Duration_key = "해당 링크에서 직접 보기"
    else:
        pass

try:
    Duration.append(Duration_key)
    print("Duration 리스트 값은, ", Duration) 
except:
    pass
   
# Title_key 자체의 Trash_keyword 제거
try:
    font_trash_word_re = re.compile('\<font.*?\>')
    font_trash_word = font_trash_word_re.findall(Title_key)[0]
except:
    pass
Title_key_trash_words = keyword_data['Trash_keyword']['Title']['Kor'] + keyword_data['Trash_keyword']['Title']['Eng']

for Title_key_trash_word in Title_key_trash_words:
    Title_key = Title_key.replace(Title_key_trash_word, " ")
    
# 기본 3개 리스트 input

#Title_key 디폴트 값

if Title_key == '해당 링크에서 직접 보기' or 'denied' in Title_key or 'Denied' in Title_key:
    try:
        Title_key_default_re = re.compile('(?<=\/\/)(.*?)(?=\/)')
        Title_key_default = Title_key_default_re.findall(User_url)[0]
        # .replace('https', '').replace('http', '').replace('m.', '').replace('www', '').replace(':', '').replace('kr.', '').strip(' /.')

        Title_key = Title_key_default
    except:
        Title_key = User_url
Title.append(Title_key.strip())    

# Desc. trash_word 제거
desc_trash_words = keyword_data['Trash_keyword']['Destributor']['Kor'] + keyword_data['Trash_keyword']['Destributor']['Eng']
for desc_trash_word in desc_trash_words:
    Description_key = Description_key.replace(desc_trash_word, "")
    
Description.append(Description_key.strip())

# Thumbnail_image  input
Thumbnail_image_extention_list = keyword_data['Condition_keyword']['Thumbnail_image_extention_list']['Kor'] + keyword_data['Condition_keyword']['Thumbnail_image_extention_list']['Eng']

if any(Thumbnail_image_extention in Thumbnail_image_key for Thumbnail_image_extention in Thumbnail_image_extention_list) == True:
    pass
else:
    Thumbnail_image_key = '해당 링크에서 직접 보기'
    
if Thumbnail_image_key.startswith("//"):
    Thumbnail_image_key = Thumbnail_image_key[2:]
elif Thumbnail_image_key.startswith(" //"):
    Thumbnail_image_key = Thumbnail_image_key[3:]
elif Thumbnail_image_key.startswith("/"):
    Thumbnail_image_key = Thumbnail_image_key[1:]
elif Thumbnail_image_key.startswith(" /"):
    Thumbnail_image_key = Thumbnail_image_key[2:]

if 'https' not in Thumbnail_image_key and 'http' not in Thumbnail_image_key:
    Thumbnail_image_key = 'https://' + Thumbnail_image_key
try:
    res = requests.get(Thumbnail_image_key, timeout=5, headers=headers) 
except:
    Thumbnail_image_key = 'https://lh3.googleusercontent.com/drive-viewer/AJc5JmQtu9w8WEBCv2de0MiHFyUdDp8Lk9sGAkHTl_b0d0bMbJzfU0wriDr9WGWLNE_hcoR8-USSsvA=w1920-h902'

Thumbnail_image.append(Thumbnail_image_key.strip())
del Thumbnail_image[0]

print('최종 Title 리스트 값은, ', Title)
print('최종 Description 리스트 값은, ', Description)
print('최종 Thumbnail_image 리스트 값은, ', Thumbnail_image)
print("최종 User_url", User_url)

#설명 6번
# lprice & mall 파악

#Type = 위시 중 아래 3가지로 구분

#1. Lower_price, Searched까지 다 찾는 것(Ex. 11번가 - 구체적 상품 페이지): Type == 위시 구분된 것
#2. Lower_price만 찾고 Searched는 안 찾는 것(Ex. 부동산, 자동차, 숙박, 항공, 공연티켓, 여행상품): no searched 셋팅 / Lower_price_key 안 잡는 경우: 룸/상품 등 조건이 많은 경우
#3. Lower_price, Searched 다 안 찾는 것(Ex. 11번가 - 기획전 페이지): Lower_price == "비교가를 찾을 수 없어요" or "-" 

if Type_key == '위시':
    print("현재 가격 스크래핑 시작")
    
    #no_Lower_price_keywords셋팅_최저가 찾는 의미가 없는 것(Ex. 숙박, 항공, 공연티켓 등)
    no_Lower_price_keywords = keyword_data['Condition_keyword']['no_Lower_price_keywords']['Kor'] + keyword_data['Condition_keyword']['no_Lower_price_keywords']['Eng']
    # 'car' -> 'cartier'와 같은 경우, 이를 피하기 위해 끝나는 마침표를 꼭 찍어줄 것
    if any(no_Lower_price_keyword in User_url for no_Lower_price_keyword in no_Lower_price_keywords) == False:
        try:
            # 개별 site 최저가 크롤링 설정
            # 11번가
            if '11st.' in User_url:
                # FB 헤더값 설정 시 미충족 html
#                 headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
#                 res = requests.get(User_url, timeout=3, headers=headers) 
#                 soup = BeautifulSoup(res.text, 'html.parser')
                try:
                    Lower_price_key = soup.select_one('div.b_product_info_price.b_product_info_price_style2 strong > span.value').text
                except:
                    try:
                        Lower_price_key = soup.select_one('div.b_product_info_price.b_product_info_price_style2 span.value').text
                    except:   
                        try:
                            Lower_price_key = soup.select_one('#priceLayer > div.price > span > b').text
                        except:
                            try:
                                product_id_11st_re = re.compile('(?<=products\/pa\/)[0-9]+|(?<=products\/)[0-9]+')

                                product_id_11st = product_id_11st_re.findall(User_url)[0]
                                User_url_api = 'https://www.11st.co.kr/products/v1/pc/products/' + str(product_id_11st) + '/detail'
                                res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                                result_dict = json.loads(res_api.text)

                                Lower_price_key = result_dict['price']['finalDscPrice']
                            except:
                                try:
                                    if 'live11' in User_url:
                                        Lower_price_key = dict_result_script_api['settingInfo']['settings'][1]['products'][0]['finalDscPrice']
                                    else:
                                        pass
                                except:
                                    Lower_price_key = Lower_price_key
            # 쿠팡
            elif 'coupang' in User_url:

                if 'trip.coupang' in User_url: # 쿠팡 트립

                    script_text1 = soup.select_one('script#travel-detail-product-data').get_text()
                    dict_result_script_text = json.loads(script_text1)
                    Lower_price_key = dict_result_script_text['product']['representativeVendorItem']['price']['totalSalesPrice']

                else: # 쿠팡 일반
                    script_re = re.compile('(?<=exports.sdp =).+')
                    script_text1 = script_re.findall(str(soup))
                    script_text = str(script_text1[0].strip().replace(';', ""))
                    dict_result_script_text = json.loads(script_text)

                    Lower_price_key2 = dict_result_script_text['apiUrlMap']['addToCartUrl']
                    Lower_price_key_re = re.compile('(?<=price=)[0-9,]+')
                    Lower_price_key1 = Lower_price_key_re.findall(str(Lower_price_key2))
                    for Lower_price_key in Lower_price_key1:
                        Lower_price_key = Lower_price_key

            # 무신사
            elif 'musinsa' in User_url: #'무신사 회원가' 중 가장 비싼 가격을 선택
                if 'musinsaapp' in User_url:
                    time.sleep(0.3)
#                     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
#                     res = requests.get(User_url, timeout=3, headers=headers) 
#                     soup = BeautifulSoup(res.content, 'html.parser')                
                try:
                    script_re = re.compile('(?<=stateAll = ).+')
                    script_text = script_re.findall(str(soup))[0]
                    dict_result_script_text = json.loads(script_text)
                    Lower_price_key = dict_result_script_text['productInfo']['price']                 
                except:
                    try:
                        Lower_price_key = soup.select_one('#goods_price').text            
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['productInfo']['normal_price'] 
                        except:
                            Lower_price_key = Lower_price_key

            elif 'bunjang' in User_url:
                try:
                    Lower_price_key = result_dict['item_info']['price']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['offers']['price']  
                    except:
                        Lower_price_key = Lower_price_key

                if result_dict['item_info']['status'] == "3":
                    Lower_price_key = "품절인가봐요!"

            #에이블리
            elif 'a-bly' in User_url:
                try:
                    Lower_price_key = result_dict['goods']['representative_option']['member_level_price']
                except:
                    try:
                        Lower_price_key = result_dict['goods']['representative_option']['price']
                    except:
                        Lower_price_key = result_dict['goods']['representative_option']['original_price']

            # 지그재그
            elif 'zigzag' in User_url:

                # product_id regex

                product_id_re = re.compile('(?<=p\/)[0-9]+')
                product_id1 = product_id_re.findall(User_url)

                # store url 확인

                for product_id in product_id1:
                    User_url_rd = 'https://store.zigzag.kr/catalog/products/' + str(product_id)

                res_rd = requests.get(User_url_rd, timeout=3, headers=headers)

                if res_rd.status_code != 200:
                    print("User_url_api 접속 오류입니다")

                # store. zigzag 링크 - js 스크래핑

                soup_rd = BeautifulSoup(res_rd.text, 'html.parser')

                script_rd = soup_rd.select_one('#__NEXT_DATA__')
                script_rd = script_rd.text

                dict_result_rd = json.loads(script_rd)

                Lower_price_key = dict_result_rd['props']['pageProps']['product']['product_price']['final_price']

            elif 'brandi' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['product']['product']['sale_price']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['product']['product']['original_sale_price']
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['product']['product']['original_price_info']['sale_price']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['product']['product']['original_price_info']['expect_sale_price']
                            except:
                                try:
                                    Lower_price_key = soup.select_one('p.price').text
                                except:
                                    Lower_price_key = Lower_price_key
                                    
    #이베이
            elif 'ebay.com' in User_url:
                try:
                    script_re = re.compile('(?<=\"priceAmountValue\":).*?}')
                    dict_script_re = script_re.findall(str(soup))[0]
                    dict_result_script = json.loads(dict_script_re)           
                    Lower_price_key = dict_result_script.get('value')               
                except:
                      Lower_price_key = Lower_price_key     
                        
            # 지마켓
            elif 'gmarket' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['Order']['Price']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['Discount']['DcPrice']
                    except:
                        try:
                            Lower_price_key = soup.select_one('strong.price_real').text
                        except:
                            Lower_price_key = Lower_price_key

            elif 'oliveyoung' in User_url:
                try:
                    Lower_price_key = result_dict['salePrc']
                except:
                    try:
                        Lower_price_key = result_dict['supPrc']
                    except:  
                        try:
                            Lower_price_key = soup.select_one('span.price-2').text
                        except:
                            Lower_price_key = Lower_price_key

            elif 'daangn' in User_url:

                try:
                    Lower_price_key = soup.select_one('#article-price').text
                except:
                    Lower_price_key = Lower_price_key

            elif 'wemakeprice' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['prodMain']['sale']['benefitPrice']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['prodMain']['sale']['salePrice']
                    except:
                        try:
                            script_re = re.compile('(?<=benefitPrice\":)[0-9]+')
                            Lower_price_key = script_re.findall(str(soup))[0]
                        except:
                            try:
                                script_re = re.compile('(?<=salePrice\":)[0-9]+')
                                Lower_price_key = script_re.findall(str(soup))[0]
                            except:
                                Lower_price_key = Lower_price_key
                if Lower_price_key == '0': #렌탈료 가능성 높음
                    Lower_price_key = '해당 링크에서 직접 보기'
            elif '29cm' in User_url:            
                try:
                    Lower_price_key = soup.select_one('span.css-4bcxzt.ent7twr4').text
                except:
                    Lower_price_key = Lower_price_key

            elif 'cjonstyle' in User_url:
                product_id_cjon_re = re.compile('(?<=item\/)[0-9]+|(?<=mocode\/)M[0-9]+')
                product_id_cjon1 = product_id_cjon_re.findall(User_url)
                
                channelcode_cj_re = re.compile('(?<=channelCode=)[0-9]+')
                channelcode_cj = channelcode_cj_re.findall(User_url)[0]
                
                try:
                    
                    for product_id_cjon in product_id_cjon1:

                        User_url_api = 'https://base.cjonstyle.com/c/rest/item/' + str(product_id_cjon) + '/buyInfo.json?channelCode='+  str(channelcode_cj)
                        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                        result_dict = json.loads(res_api.text)

                        try:
                            Lower_price_key = result_dict['result']['cardPromotions'][0]['salePrice']
                        except:
                            try:
                                Lower_price_key = result_dict['result']['itemSummaryInfo']['clpSlPrc']
                            except:
                                try:
                                    Lower_price_key = result_dict['result']['itemSummaryInfo']['slPrc']
                                except:
                                    Lower_price_key = Lower_price_key 
                                    
                    
                except:
                    for product_id_cjon in product_id_cjon1:

                        try:
                            User_url_api = 'https://display.cjonstyle.com/c/rest/item/' + str(product_id_cjon) + '/itemInfo.json?channelCode='+ str(channelcode_cj)
                            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                            
                        except:

                            User_url_api = 'https://display.cjonstyle.com/c/rest/mocode/' + str(product_id_cjon) + '/mocodeInfo.json?channelCode='+ str(channelcode_cj)
                            res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                            
                        if res_api.status_code != 200:
                            print("User_url_api 접속 오류입니다")
                        print("확인중", User_url_api)
                        result_dict = json.loads(res_api.text)

                        try:
                            Lower_price_key = result_dict['result']['detailInfo']['clpSlPrc']
                        except:
                            try:
                                Lower_price_key = result_dict['result']['detailInfo']['slPrc']
                            except:
                                try:
                                    Lower_price_key = result_dict['result']['itemSummaryInfo']['clpSlPrc']
                                except:
                                    try:
                                        Lower_price_key = result_dict['result']['itemSummaryInfo']['salePrice']
                                    except:
                                        Lower_price_key = result_dict['result']['moCode']['representItem']['itemPriceManager']['salePrice']
#공구마켓
            elif 'market09' in User_url: 
                try:
                    Lower_price_key= soup.select_one('meta[property="og:description"]')['content'].strip()
                except:
                    Lower_price_key= Lower_price_key
                    
                    
#그립(grip)
            elif 'grip.show' in User_url: 
            
                product_id_re = re.compile('(?<=product\/).+(?=\?)')
                product_id = product_id_re.findall(User_url)[0]

                User_url_api = 'https://api.grip.show/w/prd/' + str(product_id) 
                
                res_api = requests.get(User_url_api, timeout=3, headers=headers) 
                soup = BeautifulSoup(res_api.content, 'html.parser')  
                             
                try:
                    script_re = re.compile('(?<=sellingPrice =).+(?=;)')
                    Lower_price_key = script_re.findall(str(soup))[0]                  
                except:
                    try:
                        script_re = re.compile('(?<=liveSellingPrice = ).+(?=;)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        Lower_price_key= Lower_price_key
                        
                        
#샵사이다
            elif 'shopcider' in User_url:
          
                try:
                    content_shopcider = soup.find_all('script', {'type':'application/ld+json'})[0]
                    content_shopcider_re = json.loads(content_shopcider.text)
                    Lower_price_key = content_shopcider_re['offers']['price']
                except:
                    Lower_price_key = Lower_price_key                                    
    
# H 패션몰
            elif 'hfashionmall' in User_url:          
                try:
                    Lower_price_key = soup.select_one('#minPrice')['value']
                except:
                    try:
                        Lower_price_key = soup.select_one('#maxPrice')['value']
                    except:
                        try:
                            Lower_price_key = soup.select_one('p.coupon > span.num').text
                        except:
                            try:
                                Lower_price_key = soup.select_one('div.item-price > p.price > span').text
                            except:
                                try:
                                    Lower_price_key = soup.select_one('meta[property="recopick:price"]')['content']
                                except:
                                    Lower_price_key = soup.select_one('input#lastSalePrc')['value']
            # ikea
            elif 'ikea' in User_url:       
                product_id_ikea_re = re.compile('[0-9]{7,}')
                product_id_ikea1 = product_id_ikea_re.findall(User_url)

                product_id_ikea = product_id_ikea1[0]
                product_id_ikea_back_threedigits = product_id_ikea[-3:]

                try:
                    User_url_api = 'https://www.ikea.com/kr/ko/products/'+ str(product_id_ikea_back_threedigits) + '/' + str(product_id_ikea) + '.json'
                    print(User_url_api)

                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                    result_dict = json.loads(res_api.text)

                    Lower_price_key = result_dict['priceNumeral']
                except:
                    try:
                        Lower_price_key = result_dict['price']
                    except:
                        try:
                            Lower_price_key = result_dict['revampPrice']['integer']
                        except:
                            Lower_price_key = soup.select_one('.pip-price__integer').text

            elif 'kcar.' in User_url:  
                try:
                    Lower_price_org = dict_result_script_api['data']['rvo']['wklyDcPrc']                           
                    if Lower_price_org is None :
                        Lower_price_key = dict_result_script_api['data']['rvo']['salprc']
                    else: 
                        Lower_price_key = Lower_price_org
                        
                    Lower_price_key = f"{int(Lower_price_key):,}만원"
                            
                except:
                    Lower_price_key = Lower_price_key
                
            elif 'kream' in User_url:
                try:
                    script_re = re.compile('(?<=\"lowPrice\":)\d+')
                    Lower_price_key = script_re.findall(str(soup))[0]                    
                except:    
                    Lower_price_key = Lower_price_key                      

            elif 'kbchachacha' in User_url:  
                try:
                    Lower_price_key = soup.select_one('strong.cost-highlight').text.strip()
                except:
                    try:
                        Lower_price_key = soup.select_one('div.car-intro__cost.ui-inview').text.strip()
                    except:
                        Lower_price_key = Lower_price_key

            elif 'lfmall' in User_url:  
                try:
                    Lower_price_key = soup.select_one('span.current_price').text
                except:
                    try:
                        product_id_lfmall_re = re.compile('(?<=PROD_CD=)[0-9A-Z]+')

                        product_id_lfmall1 = product_id_lfmall_re.findall(User_url)

                        for product_id_lfmall in product_id_lfmall1:
                            User_url_api = 'https://mapi.lfmall.co.kr/api/products/detail/detailOptionItems?productId=' + str(product_id_lfmall)

                        res_api = requests.get(User_url_api, timeout=5, headers = headers) 
                        print(User_url_api)
                        if res_api.status_code != 200:
                            print("User_url_api 접속 오류입니다")

                        result_dict = json.loads(res_api.text)

                        Lower_price_key = int(result_dict['results']['productDetailOption']['productDetailOptionItems'][0]['salePrice'])
                    except:
                        Lower_price_key = Lower_price_key

            elif '.nsmall' in User_url: 
                try:
                    Lower_price_key = dict_post_api['msg']['goods'][0]['info']['orginSalePrice']
                except:
                    try:
                        Lower_price_key = dict_post_api['msg']['goods'][0]['info']['salePrice']
                    except:
                        try:
                            Lower_price_key = dict_post_api['msg']['goods'][0]['info']['applyPrice']
                        except:
                            Lower_price_key = Lower_price_key

            elif 'sivillage' in User_url: 
                try:
                    Lower_price_key = soup.select_one('div.detail__info-price-current.subsc_unchk').text
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="eg:salePrice"]')['content']
                    except:
                        try:
                            sv_price_re = re.compile('(?<=\'price\':)(.*?)(?=,)')
                            Lower_price_key = sv_price_re.findall(str(soup))[0]
                        except:
                            Lower_price_key = Lower_price_key

            elif 'ssfshop' in User_url: 
                try:
                    Lower_price_key = soup.select_one('form#goodsForm input[name="lastSalePrc"]')['value']
                except:
                    try:
                        Lower_price_key = soup.select_one('#godPrice').text
                    except:
                        try:
                            Lower_price_key_re = re.compile('(?<=,salePrice: ).+')
                            Lower_price_key = Lower_price_key_re.findall(str(soup))[0]      
                        except:
                            try:
                                Lower_price_key = soup.select_one('p.prd-price span.current').text
                            except:
                                Lower_price_key = Lower_price_key

            elif 'ssg.' in User_url: 
                # final url 잡기
                try:
                    ssg_itemId__re = re.compile('(?<=temId%3D)(.*?)(?=%)')
                    ssg_itemId = ssg_itemId__re.findall(User_url)[0]
                    User_url = 'https://www.ssg.com/item/dealItemView.ssg?itemId=' + ssg_itemId
                except:
                    User_url = User_url

                print("SSG final URL은? ", User_url)

                headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
                res = requests.get(User_url, headers=headers) 
                soup = BeautifulSoup(res.content, 'html.parser')

                try:
                    Lower_price_key = soup.select_one('em.ssg_price').text
                except:
                    try:
                        price_re = re.compile('(?<=price = ).+(?=)')
                        Lower_price_key = price_re.findall(str(soup))[0]
                    except:
                        try:
                            price_re = re.compile('(?<=\'value\': ).+(?=,)')
                            Lower_price_key = price_re.findall(str(soup))[0]
                        except:
                            Lower_price_key = Lower_price_key

            elif 'gsshop' in User_url: 
                try:
                    Lower_price_key = dict_result_script_text['pmo']['rentConslInfo']['exposeRentConslCostMin']                
                except:
                    try:
                        Lower_price_key = dict_result_script_text['pmo']['prc']['minPrc']
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['pmo']['gsPrc']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['pmo']['prc']['flgdPrc']
                            except:
                                Lower_price_key =Lower_price_key

            elif 'cartier' in User_url: 
                try:
                    Lower_price_key = dict_result_script_text['offers']['price']
                except:
                    try:
                        Lower_price_key = soup.select_one('span.value').text    
                    except:
                        Lower_price_key =Lower_price_key

            elif 'joongna' in User_url:
           
                try:
                    script = soup.select('script[type="application/ld+json"]')[1].text
                    result_dict = json.loads(str(script))

                    Lower_price_key = result_dict['offers'][0]['price']
                except:
                    Lower_price_key = Lower_price_key                        
                        
            elif Distributor_key in ['naver']:
                if 'land.naver' in User_url:
                    try:
                        Lower_price_key = soup.select_one('div.complex_price_wrap').text.replace("\n", " ")
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['state']['article']['addition']['sameAddrMinPrc']
                            if Lower_price_key == "0":
                                Lower_price_key = dict_result_script_text['state']['article']['dealerTelInfo']['leasePrc']
                                if Lower_price_key == "0":
                                    Lower_price_key = str(dict_result_script_text['state']['article']['price']['dealPrice'])
                                    if Lower_price_key == "0":
                                        Lower_price_key = soup.select_one('strong.detail_deal_price').text 
                                        if Lower_price_key == "0":
                                            Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['state']['article']['dealerTelInfo']['leasePrc']
                                if Lower_price_key == "0":
                                    Lower_price_key = str(dict_result_script_text['state']['article']['price']['dealPrice'])
                                    if Lower_price_key == "0":
                                        Lower_price_key = soup.select_one('strong.detail_deal_price').text 
                                        if Lower_price_key == "0":
                                            Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])
                            except:
                                try:
                                    Lower_price_key = str(dict_result_script_text['state']['article']['price']['dealPrice'])
                                    if Lower_price_key == "0":
                                        Lower_price_key = soup.select_one('strong.detail_deal_price').text 
                                        if Lower_price_key == "0":
                                            Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])                      
                                except:
                                    try:
                                        Lower_price_key = soup.select_one('strong.detail_deal_price').text #가격비교 안할꺼니 한글명 단위 -> 숫자 치환 안함
                                        if Lower_price_key == "0":
                                            Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])         
                                    except:
                                        try:
                                            Lower_price_key = str(dict_result_script_text['state']['article']['price']['warrantPrice'])
                                        except:
                                            Lower_price_key = Lower_price_key   
                                            
                    roomtype_naver = dict_result_script_text['state']['article']['article']['tradeTypeName']
                    # 가격 단위 수정
                  #  Lower_price_key_last = Lower_price_key[-1]
                    if 'complex' in User_url:
                        try:
                            Lower_price_key = str(Lower_price_key) 
                        except:
                            Lower_price_key = Lower_price_key  
                    else:        
                        try:
                            Lower_price_key = roomtype_naver + ' ' + str(Lower_price_key) 
                        except:
                            Lower_price_key = Lower_price_key   
                            
                elif 'book' in User_url:
                    try:
                        Lower_price_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['BookCatalog']['statistics']['paperBook']['lowPrice']
                    except:
                        Lower_price_key = Lower_price_key
                        
                elif 'joonggonara' in User_url:
                    try:
                        Lower_price_key = dict_result_script_api['result']['saleInfo']['price']
                    except:
                        Lower_price_key = Lower_price_key      
                


                else: #일반 쇼핑(catalog, brand, smartstore, store...etc.)
                    try:
                        Lower_price_key = dict_result_script_text['offers']['price']
                    except:
                        try:
                            Lower_price_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][1]['state']['data']['catalog_Catalog']['lowestPrice']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][3]['state']['data']['pages'][0]['products'][0]['mobilePrice']
                            except:
                                try:
                                    Lower_price_key = dict_result_script_text['props']['pageProps']['catalog']['lowestPrice']
                                except:
                                    try:
                                        Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['info']['lowestPrice']
                                    except:
                                        try:
                                            Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['recommend']['comparision']['baseItem']['mobileLowPrice']
                                        except:
                                            try:
                                                Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['recommend']['comparision']['baseItem']['lowPrice']
                                            except:
                                                try:
                                                    Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['products'][0]['productsPage']['products'][0]['pcPrice']
                                                except:
                                                    try:
                                                        Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['catalog']['products'][0]['productsPage']['products'][0]['mobilePrice']
                                                    except:
                                                        Lower_price_key = Lower_price_key

            elif 'wconcept' in User_url:
                try:
                    script_re = re.compile('(?<=value: ).*(?=\,)')
                    Lower_price_key = script_re.findall(str(soup))[0]    
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="eg:salePrice"]')['content']
                    except:
                        try:
                            Lower_price_key = soup.select_one('input[name="saleprice"]')['value']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['af_sale_price']
                            except:
                                Lower_price_key = Lower_price_key            

            elif 'thehandsome' in User_url:                            
                try:    
                    script_re = re.compile('(?<=dcPrice :).*(?=\,)')
                    Lower_price_key = script_re.findall(str(soup))[0]        
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="recopick:sale_price"]')['content']
                    except:
                        try:
                            Lower_price_key = soup.select_one('input#productPrice')['value']
                        except:
                            try:
                                script_re = re.compile('(?<=price :).*(?=\,)')
                                Lower_price_key = script_re.findall(str(soup))[0]   
                            except:
                                try:
                                    Lower_price_key = soup.select_one('meta[property="recopick:price"]')['content']
                                except:
                                    Lower_price_key = Lower_price_key

            elif 'dior' in User_url:                                    
                try:
                    Lower_price_key = dict_result_script_text['offers'][0]['price']   
                except:
                    try:
                        Lower_price_key = dict_result_script_text['offers']['price']            
                    except:
                        try:
                            Lower_price_key = str(dict_result_script_text['product']['variants'][0]['price'])[:-2]
                        except:
                            try:
                                Lower_price_key = soup.select_one('input#selected-variant-price')['value']
                            except:
                                Lower_price_key = Lower_price_key

            elif 'lotteimall' in User_url:
                try:
                    Lower_price_key = soup.select_one('p.price_fin').text
                except:
                    try:
                        Lower_price_key = soup.select_one('span.sale_price').text
                    except:
                        try:
                            Lower_price_key = soup.select_one('input#final_sale_prc')['value']
                        except:
                            try:
                                Lower_price_key = soup.select_one('input#sale_price')['value']
#                             except: #오류가 잦음
#                                 try:
#                                     script_re = re.compile('(?<=sel_item_sale_prc = ).*(?=;)')
#                                     Lower_price_key2 = script_re.findall(str(soup))
#                                     for Lower_price_key1 in Lower_price_key2:
#                                         if Lower_price_key1 != 0:
#                                             Lower_price_key = Lower_price_key1
#                                         else:
#                                             Lower_price_key = Lower_price_key1
                            except:
                                Lower_price_key = Lower_price_key

            elif 'louisvuitton' in User_url:
                try:
                    script_re = re.compile('(?<=\"price\":)[^,]+(?=,)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                    try:
                        script_re = re.compile('(?<=\"productPrice\":)[^a-z]+(?=,)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key

            elif 'myrealtrip' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['offer']['price']['main']
                except:
                    Lower_price_key = Lower_price_key

            elif 'homeplus' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['@graph'][0]['offers']['price']
                except:
                    try:
                        Lower_price_key = soup.select_one('span.info_txt > em').text
                    except:
                        Lower_price_key = Lower_price_key   

            elif 'kurly' in User_url:
                Lower_price_key1 = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['discountedPrice']
                Lower_price_key2 = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['retailPrice']
                Lower_price_key3 = dict_result_script_text['props']['pageProps']['product']['dealProducts'][0]['basePrice']
                Lower_price_key4 = dict_result_script_text['props']['pageProps']['product']['discountedPrice']
                Lower_price_key5 = dict_result_script_text['props']['pageProps']['product']['retailPrice']
                Lower_price_key6 = dict_result_script_text['props']['pageProps']['product']['basePrice']

                Lower_price_key_int_list = []
                Lower_price_key_all_list = [Lower_price_key1, Lower_price_key2, Lower_price_key3, Lower_price_key4, Lower_price_key5, Lower_price_key6]
                for Lower_price_key_temp in Lower_price_key_all_list:
                    if type(Lower_price_key_temp) == int:
                        Lower_price_key_int_list.append(Lower_price_key_temp)  
                Lower_price_key = min(Lower_price_key_int_list)            

            elif 'mangoplate' in User_url:
                if 'eat_deals' in User_url:
                    try:
                        Lower_price_key = dict_result_script_text['sales_price']   
                    except:
                        try:
                            Lower_price_key = soup.select_one('span.EatDealInfo__SalesPrice').text
                        except:
                            Lower_price_key = Lower_price_key

            elif 'mustit' in User_url:                        
                try:
                    script_re = re.compile('(?<=MAX_BENEFIT\",price:)[0-9]+(?=,)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                    try:
                        Lower_price_key = soup.select_one('span.font-bold').text
                    except:
                        Lower_price_key = Lower_price_key

            elif 'balaan' in User_url:
                try:
                    Lower_price_key = result_dict['data'][product_id_balaan]['member_price']
                except:
                    try:
                        Lower_price_key = result_dict['data'][product_id_balaan]['price']
                    except:
                        try:
                            Lower_price_key = soup.select_one('span#price').text
                        except:
                            Lower_price_key = Lower_price_key

            elif 'burberry' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['db']['pages'][product_id]['data']['price']['current']['value']
                except:
                    try:
                        Lower_price_key = json.loads(dict_result_script_text['db']['pages'][product_id]['seo']['schemas']['product'])['offers']['price']
                    except:
                        Lower_price_key = Lower_price_key

            elif 'chanel.' in User_url:

                script_re = re.compile('(?<=Load = Object.assign\().+(?=, {})')
                script_text = script_re.findall(str(soup))[0]
                dict_result_script_text = json.loads(script_text)  
                try:  
                    Lower_price_key_org = dict_result_script_text['ecommerce']['detail']['products'][0]['price']
                    Lower_price_key = re.findall('\d.+(?<=\.)',Lower_price_key_org)[0]

                except:
                    try:
                        Lower_price_key = soup.select_one('p.product-details__price').text
                    except:
                        Lower_price_key = Lower_price_key

            elif 'pulmuone' in User_url:
                try:
                    Lower_price_key = dict_post_api['data']['salePrice']                
                except:
                    try:                    
                        Lower_price_key = dict_post_api['data']['discountPrice']
                    except:
                        try:
                            Lower_price_key = dict_post_api['data']['buyerPaymentExpectedPrice']    
                        except:
                            try:
                                Lower_price_key = dict_post_api['data']['recommendedPrice']
                            except:
                                Lower_price_key = Lower_price_key

            elif 'seoulstore' in User_url:                        
                try:
                    Lower_price_key = dict_post_api['discountPrice']
                except:
                    try:
                        Lower_price_key = dict_post_api['sellingPrice']
                    except:
                        try:
                            Lower_price_key = dict_post_api['sortPrice']
                        except:
                            try:
                                Lower_price_key = dict_post_api['salePrice']  
                            except:
                                Lower_price_key = Lower_price_key

            elif 'styleshare' in User_url:  
                try:
                    Lower_price_key = result_dict['lowestCouponInfo']['couponPrice']
                except:
                    try:
                        Lower_price_key = result_dict['price']
                    except:
                        try:
                            Lower_price_key = result_dict['optionInfo']['options'][0]['price']
                        except:
                            Lower_price_key = Lower_price_key

            elif 'adidas' in User_url:                          
                try:
                    Lower_price_key = dict_result_script_text['offers']['price']
                except:
                    Lower_price_key = Lower_price_key

            elif 'amazon.' in User_url:                  
                try:
                    Lower_price_key = soup.select_one('input#twister-plus-price-data-price')['value']
                except:
                    Lower_price_key = Lower_price_key
            elif 'idus' in User_url:              
                try:
                    Lower_price_key= soup.select_one('.sold-price').text
                except:
                    Lower_price_key = Lower_price_key

            elif 'amoremall' in User_url: 
                try:
                    Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['availablePrice']['minFinalOnlinePrice']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['props']['pageProps']['initialState']['productDetail']['productInfo']['products'][0]['availablePrice']['finalOnlinePrice']
                    except:
                        try:
                            Lower_price_key = soup.select_one('#__next > section > section.container > section > section.container > section > div > div:nth-child(1) > div.summary > div.priceArea > span.price > strong').text
                        except:
                            Lower_price_key = Lower_price_key

            elif 'aladin' in User_url:     
                try:
                    Lower_price_key = dict_result_script_text['workExample'][0]['potentialAction']['expectsAcceptanceOf']['Price']
                except:
                    try:
                        script_re = re.compile('(?<=\"price\":)[\0-9]+(?=,)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key
                        
            elif 'aboutpet' in User_url:
                if 'event' in User_url:
                    Lower_price_key = "해당링크에서직접보기"
                else:
                    script_re = re.compile('(?<=price\":).+')
                    Lower_price_key = script_re.findall(str(soup))[0].strip('"')  

            elif 'encar' in User_url:
                try:
                    product_id_encar_re = re.compile('(?<=carid=).+')
                    product_id_encar = product_id_encar_re.findall(User_url)[0]
        
                    User_url_api = 'http://www.encar.com/dc/dc_cardetailview.do?method=ajaxInspectView&rgsid=' + str(product_id_encar)+ '&sdFlag=N'
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 
             
                    result_dict = json.loads(res_api.text)
                
                    Lower_price_key1 = result_dict[0]['inspect']['carSaleDto']['price']
                    Lower_price_key = f'{Lower_price_key1:,}' + '만원'
                except:
                    try:
                        script_re = re.compile('(?<=price\":)\d+')
                        Lower_price_key1 = script_re.findall(str(soup))[0]
                        Lower_price_key = f'{int(Lower_price_key1):,}' + '만원'

                    except:
                        Lower_price_key = Lower_price_key 
                        
            elif 'yes24' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['offers']['price']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['workExample'][0]['potentialAction']['expectsAcceptanceOf']['Price']
                    except: 
                        Lower_price_key = Lower_price_key
                                
            elif 'style24' in User_url:
                try:
                    script_re = re.compile('(?<=value:)[^a-z]+(?=,)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                      Lower_price_key = Lower_price_key
                                
            elif 'ohou.' in User_url:
                
                try:
                    Lower_price_key = soup.select_one('span.production-selling-header__price__coupon > span.number').text
                except:
                    try:
                        product_id_ohou_re = re.compile('(?<=productions\/).+\d')
                        product_id_ohou = product_id_ohou_re.findall(User_url)[0]
                        User_url_api = 'https://ohou.se/store/category.json?v=2&category=0_22_21&affect_type=%20ProductSaleDetail&affect_id=' + str(product_id_ohou) + '&page=1&per=24'
            
                        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                        result_dict = json.loads(res_api.text)

                        Lower_price_key1 = result_dict['mds_productions']['productions'][0]['selling_cost']
                        Lower_price_key1 = int(Lower_price_key1)
                        Lower_price_key2 = result_dict['mds_productions']['productions'][0]['selling_price']
                        Lower_price_key2 = int(Lower_price_key2) 
                        Lower_price_key3 = dict_result_script_text['additional_data'][1]['data']['production']['selling_price']
                        Lower_price_key3 = int(Lower_price_key3) 
                   
                        Lower_price_key = min(Lower_price_key1, Lower_price_key2, Lower_price_key3)
                    except:
                        Lower_price_key = Lower_price_key
                            
            elif 'auction.' in User_url:
                try:
                    Lower_price_key = dict_result_script_text['DiscountPrice']
                except:
                    try:
                        Lower_price_key = dict_result_script_text['Price']
                    except:
                        try:
                            Lower_price_key = result_dict['response']['items'][0]['productListDetail'][0]['sellingPrice']
                        except:
                            try:
                                Lower_price_key = dict_result_script_text['itemPrice']['SellingPrice']
                            except:
                                Lower_price_key = Lower_price_key
                 
            elif 'elandmall' in User_url:                   
                try:
                    Lower_price_key = soup.select_one('#goods_info > div.gd_prc > dl > dd.cpn > span.cp > b').text
                except:
                    try:
                        Lower_price_key = soup.select_one('#goods_info > div.gd_prc > dl > dd > span.sp > b').text
                    except:
                        try:
                            Lower_price_key = soup.select_one('meta[property="recopick:sale_price"]')['content'] 
                        except:
                            Lower_price_key = Lower_price_key 
                    
            elif 'interpark' in User_url:
             # 티켓은 좌석별 가격 상이하여 최저가 제외
                if 'live' in User_url:
                    try:
                        Lower_price_key = soup.select_one('div.discountPrice > span.num').text 
                    except:
                        try:
                            Lower_price_key = soup.select_one('div.originalPrice > span.num').text  
                        except:
                            Lower_price_key = Lower_price_key   

                elif 'voucher' in User_url:
                    product_voucherip_re = re.compile('(?<=goods\/).+')
                    product_voucherip = product_voucherip_re.findall(User_url)[0]
                    User_url_api = 'https://travel.interpark.com/api/voucher/v1/goods/getGoodsDetail/' + str(product_voucherip) + '?mobileYn=N'
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                    result_dict = json.loads(res_api.text)
                    try:
                        Lower_price_key = result_dict['data']['mainPricePromotion']
                    except:
                        try:
                             Lower_price_key = result_dict['data']['mainPrice']
                        except:
                             Lower_price_key = Lower_price_key  
                else:
                    print('test 인터파크')
                    try:
                        Lower_price_key = dict_result_script_text['productInfoPriceDto']['dcPrice']
                    except:
                        Lower_price_key = dict_result_script_text['productInfoPriceDto']['dcPriceBasic']
                            
            elif 'ysl.' in User_url:               
                try:                    
                    Lower_price_key = soup.select_one('p.c-price__value--current').text.strip()
                except:
                    try: 
                        Lower_price_key = soup.select_one('meta[itemprop="price"]')['content']
                    except:
                        Lower_price_key = Lower_price_key     
                    
            elif 'jinair' in User_url:
                try:
                    Lower_price_key= soup.select_one('p.info_sale').text
                except:
                    Lower_price_key = Lower_price_key 
                    
            elif 'ggumim' in User_url:
                try: 
                    content_ggumim = soup.find_all('script', {'type':'application/json'})[0]
                    content_ggumim_re = json.loads(content_ggumim.text)
                    Lower_price_key = content_ggumim_re['props']['initialProps']['pageProps']['furnitureViewData']['couponPrice']

                except:
                    try:
                        Lower_price_key = content_ggumim_re['props']['initialState']['app']['share']['priceDiscount']
                    except:
                        try:
                            Lower_price_key = content_ggumim_re['props']['initialState']['app']['share']['priceOriginal']
                        except:
                            try:
                                Lower_price_key = content_ggumim_re['furniture']['priceDiscount'] 
                            except:
                                try:
                                    Lower_price_key = content_ggumim_re['furniture']['priceOriginal'] 
                                except:
                                    Lower_price_key = Lower_price_key  
                   
            elif 'kolonmall' in User_url:
                if 'TimeDeal' in User_url:
                    Lower_price_key = "타임딜"
                else:
                    try:
                        kolon_re = re.compile('(?<=value :).+')
                        Lower_price_key = kolon_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key
                    
            elif 'trenbe'in User_url:  
                try:
                    product_id_trenbe_re = re.compile('\d{7,8}') #이부분만 수정
                    product_id_trenbe = product_id_trenbe_re.findall(User_url)[0]
                    User_url_api = 'https://service.trenbe.com/product/detail?goodsno=' + str(product_id_trenbe) + '&useActive=false'
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    result_dict = json.loads(res_api.text)

                    Lower_price_key = result_dict['product']['finalPrice']

                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'tiffany'in User_url: 
                try: 
                    content_tiffany = soup.find_all('script', {'type':'application/ld+json'})[1]
                    content_tiffany_re = json.loads(content_tiffany.text)
                    Lower_price_key = content_tiffany_re['offers']['price']
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'fashionplus'in User_url: 

                try:                    
                    content_fashionplus = soup.find_all('script', {'type':'application/ld+json'})[0]
                    content_fashionplus_re = json.loads(content_fashionplus.text)
                    Lower_price_key = content_fashionplus_re['offers']['price']    
                    if Lower_price_key == '0' :
                        Lower_price_key = '품절입니다'
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'pet-friends' in User_url:
                try: 
                    content_petf = soup.find_all('script', {'type':'application/json'})[0]
                    content_petf_re = json.loads(content_petf.text)

                    Lower_price_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['eigeneMetaData']['salePrice']
                except:
                    try:
                        Lower_price_key = content_petf_reThumbnail_image_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['discountApplyPrice']
                    except:
                        try:
                            Lower_price_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['sellingPrice']
                        except:
                            try:
                                Lower_price_key = content_petf_re['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['productDetail']['metaData']['eigeneMetaData']['originalPrice']
                            except: 
                                Lower_price_key =  Lower_price_key
                                
            elif 'prada'in User_url:
                try:                    
                    Lower_price_key = soup.select_one('div.info-card-component__basic-info-price').text.strip()
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'houseapp'in User_url:
                try:
                    Lower_price_key= Description_key.split(' ')[1]
                except: 
                    Lower_price_key =  Lower_price_key
                    
            elif 'hiver'in User_url:

                if 'onelink' in User_url:
                    try: 
                        product_id_hiver_re = re.compile('(?<=id=)\d+')
                        product_id_hiver = product_id_hiver_re.findall(User_url)[0]
                        User_url_api = 'https://www.hiver.co.kr/products/b/' + str(product_id_hiver) 
                        res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                        soup = BeautifulSoup(res_api.content, 'html.parser')
                    except:
                        pass

                content_hiver = soup.find_all('script', {'type':'application/json'})[0]

                content_hiver_re = json.loads(content_hiver.text)
                try:
                    Lower_price_key = content_hiver_re['data']['original_price_info']['expect_sale_price']
                except: 
                    try:
                        Lower_price_key = content_hiver_re['data']['original_price_info']['sale_price']
                    except:
                        try: 
                            Lower_price_key = content_hiver_re['data']['original_sale_price']
                        except:
                            try:
                                Lower_price_key = content_hiver_re['data']['sale_price']
                            except:
                                Lower_price_key = Lower_price_key
                                
            elif 'hanssem'in User_url:
                try:                    
                    Lower_price_key = soup.select_one('div.prd-prc-cur').text
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'homeplus'in User_url:
                try:     
                    product_id_hplus_re = re.compile('(?<=itemNo=)\d+')
                    product_id_hplus = product_id_hplus_re.findall(User_url)[0]
                    User_url_api = 'https://mfront.homeplus.co.kr/item/getItemDetail.json?itemNo=' + str(product_id_hplus) + '&storeType=HYPER'
                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    result_dict = json.loads(res_api.text)

                    Lower_price_key_dc = result_dict['data']['item']['sale']['dcPrice']


                    if Lower_price_key_dc == 0 :
                        Lower_price_key = result_dict['data']['item']['sale']['salePrice']

                    else:
                        Lower_price_key = Lower_price_key_dc 

                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'boribori' in User_url:   
                try:
                    product_id_re = re.compile('(?<=productNo=).+')
                    product_id = product_id_re.findall(User_url)[0]  
                    User_url_api = 'https://cf-api.halfclub.com/product/products/productPrice/' + str(product_id)+ '?_=1660813364279&countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2' 
                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)
                    try:                                               #두가격 중 최저값으로 가져오는 조건 추가함
                        Lower_price_key1 = result_dict['data']['price']
                        Lower_price_key2 = result_dict['data']['selPrc'] 
                        Lower_price_key = min(Lower_price_key1, Lower_price_key2) 
                    except:
                        try:
                            Lower_price_key = result_dict['data']['selPrc'] 
                        except:
                            try: 
                                Lower_price_key = result_dict['data']['normPrc']
                            except:
                                Lower_price_key = Lower_price_key

                except:
                    product_id_re = re.compile('(?<=PrdNo=)\d+')
                    product_id = product_id_re.findall(User_url)[0]  
                    User_url_api = 'https://apix.halfclub.com/product/deal/' + str(product_id)+ '?countryCd=001&deviceCd=001&langCd=001&mandM=b_boribori&siteCd=2&ts=1660814208352'

                    print(User_url_api)

                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)
                    try: 
                        Lower_price_key = result_dict['data']['productPrice']['price']
                    except:
                        Lower_price_key = Lower_price_key

#             elif 'fitpetmall' in User_url: 
#                 script_text = soup.select_one('script[type="application/json"]').text
#                 dict_result = json.loads(script_text)
#                 fitpet_id = dict_result['props']['pageProps']['data']['product']['id']
#                 print("확인중",fitpet_id)
                
    
#                 User_url_fitpetmall_api = 'https://api.fitpetmall.com/mall/graphql'

#                 headers = {
#                 'Accept': '*/*',
#                 'authority': 'api.fitpetmall.com',
#                 'accept-encoding': 'gzip, deflate, br',
#                 'content-type': 'application/json',
#                 'referer': User_url,
#                 'origin': 'https://www.fitpetmall.com',
#                 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36' 
#                 }

#                 payload = {
#                 'operationName': 'productBenefits',
#                 'variables': {'id': fitpet_id},
#                 'query':'query productBenefits($id: ID!, $productPromotion: ID) {\n  product(id: $id, productPromotion: $productPromotion) {\n    id\n    productPromotionCustomerPrice\n    maxDiscountCoupon {\n      id\n      couponGroup {\n        name\n        discountType\n        discountAmount\n        discountRate\n        maxDiscountAmount\n        couponType\n        issueType\n        __typename\n      }\n      __typename\n    }\n    reviewMileage\n    orderConfirmMileage\n    reviewMileageRate\n    orderConfirmMileageRate\n    __typename\n  }\n}\n'    
#                 }

#                 res = requests.post(User_url_fitpetmall_api, headers=headers, json =  payload, timeout = 10) 
#                 soup = BeautifulSoup(res.content,"html.parser")
 
#                 dict_post_api = json.loads(soup.text)
 
    
#                 try:
#                     Lower_price_key = dict_post_api['data']['productQnas']['edges'][0]['node']['productOption']['productPromotionCustomerPrice']
#                 except:
#                     try:
#                         Lower_price_key = dict_post_api['data']['productQnas']['edges'][0]['node']['productOption']['customerPrice']
#                     except:
#                         try:
#                             Lower_price_key = dict_post_api['data']['productQnas']['edges'][0]['node']['productOption']['price']
#                         except:
#                             Lower_price_key = Lower_price_key
                        
                        
            elif 'dailyhotel' in User_url: 
                try:
                    product_id_re = re.compile('(?<=activity\/)[0-9]{2,10}[(?=?)]?')
                    product_id = product_id_re.findall(User_url)[0]
                    User_url_api = 'https://www.dailyhotel.com/newdelhi/goodnight/api/v1/activity/deals/' + product_id

                    print(User_url_api)
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    if res_api.status_code != 200:
                        print("User_url_api 접속 오류입니다")

                    result_dict = json.loads(res_api.text)
                    try:
                        Lower_price_key = result_dict['data']['daOptionGroups'][0]['daOptions'][0]['discount']
                    except:
                        Lower_price_key = result_dict['data']['daOptionGroups'][0]['daOptions'][0]['price']
                except:
                      Lower_price_key = Lower_price_key
                        
            elif 'sonohotelsresorts' in User_url: 
                try:
                    Lower_price_key = result_dict ['result'][0]['PKG_PRICE']
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'costco' in User_url:                     
                try:
                    Lower_price_key = dict_result_script_text['offers']['price']
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="product:price:amount"]')['content']
                    except:
                        Lower_price_key = Lower_price_key
                        
            elif 'cuchenmall' in User_url:
                try:
                    script_re = re.compile('(?<=product_discount_price =)[^a-z]+(?=;)')
                    Lower_price_key = script_re.findall(str(soup))[1]
                except:
                    try: 
                        script_re = re.compile('(?<=product_price =)[^a-z]+(?=;)')
                        Lower_price_key = script_re.findall(str(soup))[1]
                    except:
                        Lower_price_key = Lower_price_key

            elif 'hogangnono' in User_url:  
                try:
                    script_text = soup.select_one('script[type="application/json"]').text
                    dict_script_text = json.loads(eval(script_text))
                               
                    Lower_price_sell = dict_script_text['AptStore']['detail']['currentArea']['real_trade_price']
                    Lower_price_rent = dict_script_text['AptStore']['detail']['currentArea']['real_rent_price']    

    
                    Lower_price_list = [Lower_price_sell, Lower_price_rent]

                    Lower_price_list_cal = []
    
                    for Lower_price_be in Lower_price_list:
                        if Lower_price_be <= 0 :
                            Lower_price_key_re = ''   

                        elif Lower_price_be >= 10000: # 1억 이상
                            Lower_price_key1 = f"{int(Lower_price_be // 10000):,}억"
                            Lower_price_key2 = Lower_price_be % 10000
                            if Lower_price_key2 > 0:
                                Lower_price_key_re = Lower_price_key1 + str(Lower_price_key2)
                            else:
                                 Lower_price_key_re = Lower_price_key1
                        elif Lower_price_be >= 1: # 1만 이상
                            Lower_price_key_re = str(Lower_price_be)                    

                        Lower_price_list_cal.append(Lower_price_key_re)

                    id_hogang_re = re.compile('(?<=apt\/).+')
                    id_hogang = id_hogang_re.findall(User_url)[0]
 
                    itemlist_hogang = id_hogang.split('/')
                    print(itemlist_hogang)
                    if itemlist_hogang[1] == '0':
                        Lower_price_key = '매매' + ' ' + Lower_price_list_cal[0] 
                    else:
                        Lower_price_key = '전월세' + ' '+ Lower_price_list_cal[1]
            
                except:
                    Lower_price_key = "해당 링크에서 직접 보기"
                    
            elif 'zigbang'in User_url:  
             
                script_text = soup.select_one('script[type="application/json"]').text
                dict_result_script_text = json.loads(script_text)
                
                try:
                    Lower_price_min = dict_result_script_text['props']['pageProps']['SSRData']['danjisOffer']['price']['min']
                except:
                    try:
                        Lower_price_min = dict_result_script_text['props']['pageProps']['SSRData']['danjisRoomTypes']['minSalesPrice']
                    except:
                         Lower_price_min = 0
                try:
                    Lower_price_max = dict_result_script_text['props']['pageProps']['SSRData']['danjisOffer']['price']['max']
                except:
                    try:               
                        Lower_price_max = dict_result_script_text['props']['pageProps']['SSRData']['danjisRoomTypes']['maxSalesPrice']
                    except:
                        Lower_price_max = 0
                 
                item_id_zigbang_re = re.compile('(?<=\/)[0-9]+')
                item_id_zigbang = item_id_zigbang_re.findall(User_url)[0]
                
                if 'store' in User_url:
                    User_url_api = ' https://apis.zigbang.com/v2/store/article/stores/' + str(item_id_zigbang)
                else:
                    User_url_api = 'https://apis.zigbang.com/v2/items/' + str(item_id_zigbang)

                res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                result_dict = json.loads(res_api.text)
            
                try:
                    Lower_price_sell = result_dict['item']['매매금액']
                    if Lower_price_sell == None:
                        Lower_price_sell = 0
                except:
                    Lower_price_sell = 0
                try:    
                    Lower_price_deposit = result_dict['item']['보증금액']
                    if Lower_price_deposit == None:
                        Lower_price_deposit = 0
                except:  
                     Lower_price_deposit = 0
                try:    
                    Lower_price_month = result_dict['item']['월세금액']
                    if Lower_price_month == None:
                        Lower_price_month = 0
                except:
                    Lower_price_month = 0
                    
                try:    
                    Lower_price_admin = result_dict['item']['관리금액']
                    if Lower_price_admin == None:
                        Lower_price_admin = 0
                except:
                    Lower_price_admin = 0                    
                
                Lower_price_rent = int(Lower_price_month) + int(Lower_price_admin)
                
                Lower_price_name = ['최소', '최대', '매매', '보증금', '월세', '관리비', '임대비']   
                Lower_price_list = [Lower_price_min, Lower_price_max, Lower_price_sell, Lower_price_deposit, Lower_price_month, Lower_price_admin, Lower_price_rent]
                Lower_price_list_re = []
    
                for Lower_price_be in Lower_price_list:
                    if Lower_price_be <= 0 :
                        Lower_price_key_re = ''   
                    
                    elif Lower_price_be >= 10000: # 1억 이상
                        Lower_price_key1 = f"{int(Lower_price_be // 10000):,}억"
                        Lower_price_key2 = Lower_price_be % 10000
                        if Lower_price_key2 > 0:
                            Lower_price_key_re = Lower_price_key1 + str(Lower_price_key2)
                        else:
                             Lower_price_key_re = Lower_price_key1
                    elif Lower_price_be >= 1: # 1만 이상
                        Lower_price_key_re = str(Lower_price_be)
                
    
                    Lower_price_list_re.append(Lower_price_key_re)
    
                Lower_price_dict = dict(zip(Lower_price_name, Lower_price_list_re))
               
                try:   
                    if 'apt' in User_url:
                        if dict_result_script_text['props']['pageProps']['SSRData']['danjis']['분양세대수'] == None :
                            Lower_price_key = '매매' + ' ' + Lower_price_dict['최소']+ '~' +  Lower_price_dict['최대']
                        else:
                            Lower_price_key = '분양가' + ' ' +  Lower_price_dict['최소']+ '~' +  Lower_price_dict['최대']
                    elif (result_dict['item']['sales_type']) == '월세' or (result_dict['item']['sales_type']) == '임대':
                        if 'store' in User_url: 
                            Lower_price_key = '월세' + ' ' +  Lower_price_dict['보증금'] + "/" +  Lower_price_dict['임대비'] + '(관리비포함)'
                        else:
                            Lower_price_key = '월세'+ ' ' +Lower_price_dict['보증금'] + "/" +  Lower_price_dict['월세']
                    else:
                        Lower_price_key = result_dict['item']['sales_type']+ ' ' +  Lower_price_dict['매매'] +  Lower_price_dict['보증금']  
                except:
                    Lower_price_key = Lower_price_key 
                    
            elif 'innisfree' in User_url:
                try:
                    Lower_price_key = soup.select_one('meta[property="eg:salePrice"]')['content']
                    Lower_price_key = re.search('\d+?\.',Lower_price_key).group()
                  
                except:
                    try:
                        Lower_price_key = soup.select_one('meta[property="eg:originalPric"]')['content']
                        Lower_price_key = re.search('\d+?\.',Lower_price_key).group()   
                    except:
                        Lower_price_key = Lower_price_key
                        
            elif 'hmall' in User_url:               
                try:                    
                    Lower_price_key = soup.select_one('meta[property="product:sale_price:amount"]')['content']
                except:
                    try: 
                        Lower_price_key = soup.select_one('meta[property="product:price:amount"]')['content']
                    except:
                        Lower_price_key = Lower_price_key  
                        
            elif 'halfclub'in User_url:                 
                if 'deal' in User_url:
                    product_id_re = re.compile('(?<=PrdNo=)\d+')
                    product_id = product_id_re.findall(User_url)[0]  
    
                    User_url_api = 'https://apix.halfclub.com/product/deal/' + str(product_id)+ '?countryCd=001&deviceCd=001&langCd=001&mandM=halfclub&siteCd=1&ts='                      

                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                    result_dict = json.loads(res_api.text)

                    try:
                        Lower_price_key = result_dict['data']['productPrice']['price']
                        
                    except:
                        Lower_price_key = Lower_price_key  
                        
                elif 'product' in User_url:
                    product_id_re = re.compile('(?<=productNo=).+')
                    product_id = product_id_re.findall(User_url)[0]  
                        
                    User_url_api = 'https://apix.halfclub.com/product/products/productPrice/' + str(product_id)+ '?_=&countryCd=001&deviceCd=001&langCd=001&mandM=halfclub&siteCd=1'                      
        
                    
                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 
                    result_dict = json.loads(res_api.text)
        
                    try:
                        Lower_price_key = result_dict['data']['price']
                        
                    except:
                        try:
                            Lower_price_key = result_dict['data']['selPrc']
                        except:
                            try:
                                Lower_price_key = result_dict['data']['normPrc']
                            except:
                                 Lower_price_key = Lower_price_key  
                else:
                    Lower_price_key = Lower_price_key    
                    
            elif 'tmon' in User_url:                 
                try:
                    Lower_price_key = soup.select_one('meta[property="og:price"]')['content'] 
                except:
                    Lower_price_key = Lower_price_key    
                    
                    
            elif '.trip.com' in User_url:
                try:
                    script_re = re.compile('(?<=\"notFormatPrice\":)[^a-z]+(?=,)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                    try: 
                        script_re = re.compile('(?<=\"minPrice\":)[^a-z]+(?=,)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        try:
                            script_re = re.compile('(?<=\"minPriceStr\":)[^a-z]+(?=,)')
                            Lower_price_key = script_re.findall(str(soup))[0]
                        except:
                            Lower_price_key = Lower_price_key 
                            
            elif 'hnsmall' in User_url:                 
                try:
                    Lower_price_key = soup.select_one('div.goods-benefit-detail.final > dl > dd > strong').text  
                except:
                    try:
                        Lower_price_key = soup.select_one('div.goods-benefit-detail > dl > dd > strong').text 
                    except:
                        try:
                            Lower_price_key = soup.select_one('meta[property="product:price:amount"]')['content']
                        except:
                            try:
                                Lower_price_key = soup.select_one('meta[property="rb:salePrice"]')['content']
                            except:
                                try:
                                    Lower_price_key = soup.select_one('meta[property="rb:originalPrice"]')['content']
                                except:
                                    Lower_price_key = Lower_price_key   
                                    
            elif '10000recipe' in User_url:
                if 'shop' in User_url:
                    try:
                        Lower_price_key = soup.select_one('.price_sale_p').text
                    except:
                        try:
                            Lower_price_key = soup.select_one('.price').text
                        except:
                            try:
                                Lower_price_key = soup.select_one('meta[property="product:price:amount"]')['content']
                            except:
                                Lower_price_key = Lower_price_key
                else:
                    Lower_price_key = Lower_price_key        

            elif'dabang' in User_url: 
                if 'sign'in User_url:
                    product_id_dabang_re = re.compile('(?<=sign\/).+')
                    product_id_dabang = product_id_dabang_re.findall(User_url)[0]
                    User_url_api = 'https://www.dabangapp.com/api/3/sign-room/detail?api_version=&call_type=&room_id=' + product_id_dabang

                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    result_dict = json.loads(res_api.text)
                    try:
                        Lower_price_key = result_dict['room']['selling_type_str'] + ' ' + result_dict['room']['price_str'] 
                    except:
                        Lower_price_key = Lower_price_key
                 
                else:    
                    roomtype_list = ['월세','전세','매매']
                    roomtype = [rt for rt in roomtype_list if rt in Title_key] 

                    product_id_dabang_re = re.compile('(?<=room\/).+')
                    product_id_dabang = product_id_dabang_re.findall(User_url)[0]
                    User_url_api = 'https://www.dabangapp.com/api/3/room/detail3?api_version=&call_type=&room_id=' + product_id_dabang

                    res_api = requests.get(User_url_api, timeout=3, headers = headers) 

                    result_dict = json.loads(res_api.text)
                    try:
                        Lower_price_key = roomtype[0] + ' ' + result_dict['room']['price_title'] 
                    except:
                        Lower_price_key = Lower_price_key
                    
            elif 'spooncast' in User_url:
                try:
                    Lower_price_key  = str(result_dict['sale_spoon'])+ '스푼'
                except:
                    try:
                        Lower_price_key  = str(result_dict['origin_sale_spoon'])+ '스푼' 
                    except:
                        Lower_price_key = Lower_price_key 
                        
            elif 'shop.tworld' in User_url:
                try:
                    Lower_price_key = dict_result_script_api['childList'][0]['productPrice']
                except:
                    try:
                        Lower_price_re = re.compile('(?<=vo\.productPrice = ).+(?=;)')
                        Lower_price_key = Lower_price_re.findall(str(soup))[0].strip('"')
                    except:
                        Lower_price_key = Lower_price_key
                        
            elif 'lotteon' in User_url:     
                try:
                    Lower_price_key = dict_result_script_api['data']['priceInfo']['slPrc']
                except:
                    try:
                        product_id_lotteon3_re = re.compile('(?<=slPrc\":)[0-9]+')
                        Lower_price_key = product_id_lotteon3_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key

            elif 'shoppinghow' in User_url:    
                try:
                    Lower_price_key = dict_result_script_api['mallList'][0]['price']
                except:
                    Lower_price_key = Lower_price_key
                    
            elif 'aliexpress' in User_url:  
                try:
                    script_re = re.compile('(?<=formatedActivityPrice\":)[^a-z]+(?=,)')
                    Lower_price_key = script_re.findall(str(soup))[0]
                except:
                    try:
                        script_re = re.compile('(?<=formatedPrice\":)[^a-z]+(?=,)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        Lower_price_key = Lower_price_key
        
            elif 'kbland' in User_url: 

                price_url_api = 'https://api.kbland.kr/land-property/property/bascInfo?%EB%A7%A4%EB%AC%BC%EC%9D%BC%EB%A0%A8%EB%B2%88%ED%98%B8='+kbland_id
                price_res_api = requests.get(price_url_api, timeout=3, headers = headers) 
                price_result_dict = json.loads(price_res_api.text)
    
                price_type_key  = price_result_dict['dataBody']['data']['bascInfo']['매물거래명']
#                 area_type_key_org = price_result_dict['dataBody']['data']['bascInfo']['전용면적']
#                 area_type_key = area_type_key_org[:-3]
                try:
                    Lower_price_sell = price_result_dict['dataBody']['data']['bascInfo']['매매가']
                    if Lower_price_sell == None:
                        Lower_price_sell = 0
                except:
                    Lower_price_sell = 0
                try:    
                    Lower_price_deposit = price_result_dict['dataBody']['data']['bascInfo']['월세보증금']
                    if Lower_price_deposit == None:
                        Lower_price_deposit = 0
                except:  
                     Lower_price_deposit = 0
                try:    
                    Lower_price_month = price_result_dict['dataBody']['data']['bascInfo']['월세가']
                    if Lower_price_month == None:
                        Lower_price_month = 0
                except:
                    Lower_price_month = 0
                    
                try:    
                    Lower_price_rent = price_result_dict['dataBody']['data']['bascInfo']['전세가']
                    if Lower_price_rent == None:
                        Lower_price_rent = 0
                except:
                    Lower_price_rent = 0                    
                
                Lower_price_name = ['매매', '보증금', '월세', '전세']   
                Lower_price_list = [Lower_price_sell, Lower_price_deposit, Lower_price_month, Lower_price_rent]
                Lower_price_list_re = []
    
                for Lower_price_be in Lower_price_list:
                    if Lower_price_be <= 0 :
                        Lower_price_key_re = ''   
                    
                    elif Lower_price_be >= 10000: # 1억 이상
                        Lower_price_key1 = f"{int(Lower_price_be // 10000):,}억"
                        Lower_price_key2 = Lower_price_be % 10000
                        if Lower_price_key2 > 0:
                            Lower_price_key_re = Lower_price_key1 + str(Lower_price_key2)
                        else:
                             Lower_price_key_re = Lower_price_key1
                    elif Lower_price_be >= 1: # 1만 이상
                        Lower_price_key_re = str(Lower_price_be)
                
    
                    Lower_price_list_re.append(Lower_price_key_re)
    
                Lower_price_dict = dict(zip(Lower_price_name, Lower_price_list_re))
               
                try:   
                    if price_type_key == '월세':
                        Lower_price_key = price_type_key + ' ' + Lower_price_dict['보증금'] + "/" +  Lower_price_dict['월세']
                    else:
                        Lower_price_key = price_type_key + ' ' + Lower_price_dict['매매'] + Lower_price_dict['전세']
                   
                except:
                    Lower_price_key = Lower_price_key 
                                       
            elif 'gap.com'in User_url: 

                try:                                        
                    Lower_price_key = content_gap[0]['offers'][0]['price']    
                    if Lower_price_key == '0' :
                        Lower_price_key = '품절입니다'
                except:
                    Lower_price_key = Lower_price_key
                    
            elif'peterpanz' in User_url: 
                try:
                    script_re = re.compile('(?<=houseContractType = \')\w+(?=\';)')
                    houseContractType = script_re.findall(str(soup))[0]
                    
                    script_re = re.compile('(?<=houseDeposit = \')\d+(?=\';)')
                    houseDeposit = int(script_re.findall(str(soup))[0])//10000

                    script_re = re.compile('(?<=houseMonthlyFee = \')\d+(?=\';)')
                    houseMonthlyFee = int(script_re.findall(str(soup))[0])//10000
                    
                    Lower_price_list = [houseDeposit, houseMonthlyFee]
                    
                    Lower_price_list_cal = []
    
                    for Lower_price_be in Lower_price_list:
                        if Lower_price_be <= 0 :
                            Lower_price_key_re = ''   

                        elif Lower_price_be >= 10000: # 1억 이상
                            Lower_price_key1 = f"{(Lower_price_be // 10000):,}억"
                            Lower_price_key2 = Lower_price_be % 10000
                            if Lower_price_key2 > 0:
                                Lower_price_key_re = Lower_price_key1 + str(Lower_price_key2)
                            else:
                                 Lower_price_key_re = Lower_price_key1
                        elif Lower_price_be >= 1: # 1만 이상
                            Lower_price_key_re = Lower_price_be                   

                        Lower_price_list_cal.append(Lower_price_key_re)
                                        
                    if houseContractType == '전세' or houseContractType == '매매':                    
                        Lower_price_key = houseContractType + ' ' + str(Lower_price_list_cal[0]) 
                    else:                
                        Lower_price_key = houseContractType + ' ' + str(Lower_price_list_cal[0]) + '/' + str(Lower_price_list_cal[1])
            
                except:
                    Lower_price_key = Lower_price_key  

            elif'sooldamhwa' in User_url: 
                try:
                    Lower_price_key =  dict_result['props']['pageProps']['initialState']['damhwaMarket']['product']['discountPrice']
                except:
                    try:
                        Lower_price_key =  dict_result['props']['pageProps']['initialState']['damhwaMarket']['product']['originPrice']
                    except:
                        Lower_price_key = Lower_price_key
                        
            elif'samsung.com' in User_url: 
                Lower_price_key = soup.select_one('div.compare-itm-price').text


    #최저가가
# 코리아센터 호스팅 가격 코드 -------------------------------------

            elif 'branduid'in User_url: 
                if "sto_state:'SALE'" in str(soup):
                    try:
                        script_re = re.compile('(?<=var product_price =).+(?=;)')
                        Lower_price_key = script_re.findall(str(soup))[0]
                    except:
                        try:
                            script_re = re.compile('(?<=var prd_sellprice    =).+(?=;)')
                            Lower_price_key = script_re.findall(str(soup))[0]
                        except:
                            Lower_price_key = Lower_price_key                 
                        
                else:   
                    Lower_price_key =  '품절인가봐요'
                    
# NHN 고도몰 가격 코드 -------------------------------------

            elif 'goods_view'in User_url:
                try:
                    Lower_price_key = soup.select_one('.price_sale_p').text  #만개의스토어 첫구매가
                except:
                    try:
                        Lower_price_key = soup.select_one('dd.coupon_price > strong').text  #자코모소파 쿠폰가
                    except:
                        try:
                            script_re = re.compile('(?<=discountPrice:).+(?=,)')
                            Lower_price_key = script_re.findall(str(soup))[0].strip()
                            if Lower_price_key  == '0':
                                try:
                                    Lower_price_key  = soup.find('input',{'name':'set_coupon_dc_price'}).get('value')
                                except:
                                    try:
                                        Lower_price_key  = soup.find('input',{'name':'set_goods_price'}).get('value')
                                    except:
                                        Lower_price_key = Lower_price_key 
                        except:
                            Lower_price_key = Lower_price_key 
                            
# 카페24 가격 코드 ------------------------                        

            elif (cafe24_url != None) or ('detail.html' in User_url):
                if "var is_soldout_icon = 'T'" in str(soup):
                    Lower_price_key =  '품절인가봐요'
                else:                    
                    try:
                        Lower_price_key = soup.select_one('meta[property="product:sale_price:amount"]')['content']
                    except:
                        try:
                            script_re = re.compile('(?<=var product_sale_price =).+(?=;)')
                            Lower_price_key = script_re.findall(str(soup))[0]
                        except: 
                            try:
                                Lower_price_key= soup.select_one('meta[property="product:price:amount"]')['content']
                            except:
                                Lower_price_key = Lower_price_key  
                                
# 가비아 퍼스트몰 가격 코드 ------------------------    

            elif 'view?no'in  User_url:   
                if 'text_soldout' in str(soup):
                    Lower_price_key =  '품절인가봐요'
                else:                    
                    try:
                        Lower_price_key = soup.select_one('meta[property=":price:amount"]')['content']
                    except:
                        try:
                            script_re = re.compile('(?<=gl_goods_price = ).+(?=;)')
                            Lower_price_key = script_re.findall(str(soup))[1]
                        except:
                            Lower_price_key = Lower_price_key

            # Hosting 주요 4개사 및 일반 최저가 태그 지정
            else:
                print('해당 플랫폼 최저가 미지정 -> 호스팅 4사 최저가 태그 탐색')
                try:# cafe24
                    Lower_price_key = soup.select_one('meta[property="product:sale_price:amount"]')['content']
                except:
                    try:# NHN커머스
                        Lower_price_key  = soup.find('input',{'name':'set_coupon_dc_price'}).get('value')
                    except:
                        try:# 코리아센터  
                            script_re = re.compile('(?<=var product_price =).+(?=;)')
                            Lower_price_key = script_re.findall(str(soup))[0]
                        except: #가비아몰
                            try:
                                Lower_price_key = soup.select_one('meta[property=":price:amount"]')['content']
                            except:
                                try:
                                    script_re = re.compile('(?<=var prd_sellprice    =).+(?=;)')# 코리아센터 
                                    Lower_price_key = script_re.findall(str(soup))[0]
                                except:    
                                    print('최저가 기본 태그탐색 필요')
                                    Lower_price_key = Lower_price_key
        except: 
            print('최저가 기본 태그 탐색')
            Lower_price_key_content_tag_list = ['meta[property="product:sale_price:amount"]', 'meta[property="og:price"]', 'meta[property="og:price:amount"]',
                                               'meta[property="recopick:price"]', 'meta[property="recopick:sale_price"]', 'meta[itemprop="price"]',
                                               'meta[property="eg:salePrice"]', 'meta[property="eg:originalPric"]', 'meta[property="rb:salePrice"]',
                                               'meta[property="rb:originalPrice"]', 'meta[property="product:price:amount"]', 'meta[property=":price:amount"]',
                                               'meta[property="rb:salePrice"]']
            Lower_price_key_basic_tag_list = ['span.price', 'div.b_product_info_price.b_product_info_price_style2 strong > span.value', '#priceLayer > div.price > span > b',
                                             '#goods_price', 'p.price', 'strong.price_real',
                                             'span.price-2', '#article-price', 'span.css-4bcxzt.ent7twr4',
                                             'div.item-price > p.price > span', 'div.car_price_info span', 'strong.cost-highlight',
                                             'div.car-intro__cost.ui-inview', 'span.current_price', 'div.detail__info-price-current.subsc_unchk',
                                             '#godPrice', 'p.prd-price span.current', 'em.ssg_price',
                                             'span.value', 'div.complex_price_wrap', 'strong.detail_deal_price',
                                             'p.price_fin', 'span.sale_price', 'span.info_txt > em',
                                             'span.EatDealInfo__SalesPrice', 'span.font-bold', 'span#price',
                                             'p.product-details__price', '.sold-price', '#__next > section > section.container > section > section.container > section > div > div:nth-child(1) > div.summary > div.priceArea > span.price > strong',
                                             'span.production-selling-header__price__coupon > span.number', '#goods_info > div.gd_prc > dl > dd.cpn > span.cp > b', '#goods_info > div.gd_prc > dl > dd > span.sp > b',
                                             'div.discountPrice > span.num', 'div.originalPrice > span.num', 'p.c-price__value--current',
                                             'p.info_sale', 'div.info-card-component__basic-info-price', 'div.prd-prc-cur',
                                             'div.goods-benefit-detail.final > dl > dd > strong', 'div.goods-benefit-detail > dl > dd > strong', '.price',
                                             '.price_sale_p', 'dd.coupon_price > strong']
            Lower_price_key_value_tag_list = ['input[name="price"]', 'input[name="price_wh"]', 'input#lastSalePrc',
                                             'input#sell_price', 'form#goodsForm input[name="lastSalePrc"]', 'input[name="saleprice"]',
                                             'input#productPrice', 'input#selected-variant-price', 'input#final_sale_prc',
                                             'input#sale_price', 'input#twister-plus-price-data-price', 'input[name="set_coupon_dc_price"]',
                                             'input[name="set_goods_price"]']
            try:
                print("Lower_price_key_content_tag 탐색")
                for Lower_price_key_content_tag in Lower_price_key_content_tag_list:
                    try:
                        Lower_price_key = soup.select_one(Lower_price_key_content_tag)['content']
                    except:
                        pass
                Lower_price_key
            except NameError:
                print("Lower_price_key_basic_tag 탐색")
                try:
                    for Lower_price_key_basic_tag in Lower_price_key_basic_tag_list:
                        try:
                            Lower_price_key = soup.select_one(Lower_price_key_basic_tag).text
                        except:
                            pass
                    Lower_price_key
                except NameError:
                    print("Lower_price_key_value_tag 탐색")
                    try:
                        for Lower_price_key_value_tag in Lower_price_key_value_tag_list:
                            try:
                                Lower_price_key = soup.select_one(Lower_price_key_value_tag)['value']
                            except:
                                pass
                        Lower_price_key
                    except NameError:
                        Lower_price_key = "해당 링크에서 직접 보기"
        print('전처리 전 Lower_price_key? ', Lower_price_key)
        # Lower_price_key 전처리        
        # 단위 변환
        money_exchange_keywords = keyword_data['Condition_keyword']['money_exchange_keywords']['Kor'] + keyword_data['Condition_keyword']['money_exchange_keywords']['Eng']
        no_unit_change_keywords = keyword_data['Condition_keyword']['no_unit_change_keywords']['Kor'] + keyword_data['Condition_keyword']['no_unit_change_keywords']['Eng']
        if any(no_unit_change_keyword in User_url for no_unit_change_keyword in no_unit_change_keywords) == True:
            pass
        else:
            if any(money_exchange_keyword in User_url for money_exchange_keyword in money_exchange_keywords) == True:
                try:
                    naver_exchange = 'https://search.naver.com/search.naver?sm=tab_sug.ase&where=nexearch&query=%EB%8B%AC%EB%9F%AC+%ED%99%98%EC%9C%A8'
                    res = requests.get(naver_exchange, headers=headers) 
                    soup = BeautifulSoup(res.content, 'html.parser')
                    try:
                        naver_usd = soup.select_one('span.spt_con.up > strong').text.strip().replace(',','')
                    except:
                        naver_usd = soup.select_one('span.spt_con.dw > strong').text.strip().replace(',','')
                    Lower_price_key = str(int(round((float(Lower_price_key) * float(naver_usd)),0)))
                    print("달러 환율 적용한 Lower_price_key 값은? ", Lower_price_key, " 현재 원달러 환율: ", naver_usd)
                except:
                    Lower_price_key = Lower_price_key
            else:
                Lower_price_key = re.sub(r'(\s)', '', str(Lower_price_key))

                price_unit_dict = {'십':'0', '백':'00', '천':'000', '만':'0000', '십만':'00000', '백만':'000000', '천만':'0000000', '억':'00000000', '십억':'000000000','백억':'0000000000', '천억':'00000000000'}

                for unit_key in price_unit_dict.keys():
                    if unit_key in Lower_price_key:           
                        Lower_price_key_units = Lower_price_key.replace(unit_key, price_unit_dict.get(unit_key))
                    else:
                        Lower_price_key = Lower_price_key
                try: #한줄에 여러 가격 나올 경우 맨 앞에 가격만 추출
                    Lower_price_key = re.findall('(?:\d{0,3},)?(?:\d{3},)*\d{1,}', Lower_price_key_units)[0]
                except:
                    try:
                        Lower_price_key = re.findall('(?:\d{0,3},)?(?:\d{3},)*\d{1,}', Lower_price_key)[0]
                    except:
                        Lower_price_key = Lower_price_key
                try:
                    Lower_price_key = str(int(Lower_price_key)).strip()
                except:
                    Lower_price_key = Lower_price_key.strip().replace(',','')

                print("price_unit 변환된 값은? ", Lower_price_key)
        # 아래 고도화 필요... 필요/불가 구분은 했지만 결국 로직을 따라가보면 실패한 것은 '해당~직접보기'로 되어 '비교가를 찾을 수 없어요'로 귀결
        if Lower_price_key == "":
            Lower_price_key = "확인필요"
        elif Lower_price_key == "해당링크에서직접보기":
            Lower_price_key = "확인불가"
        else:
            try:
                Lower_price_key = int(float(Lower_price_key))
            except:
                Lower_price_key = Lower_price_key

        if type(Lower_price_key) == int:
            Lower_price_key = format(Lower_price_key, ',')  + "원"
            Lower_price.append(Lower_price_key)
            Lower_price_key = int(Lower_price_key.replace("원", "").replace(",", ""))
        else:
            Lower_price.append(Lower_price_key)
        print('Lower_price 리스트 값은, ', Lower_price)

        # 네이버 쇼핑 값일 경우 최저몰도 함께 출력 (프론트 반영 시)

#         if 'naver.com' in User_url and Type == '위시':

#             Lower_mall.append(Lower_mall_key)
#             print('Lower_mall 리스트 값은, ' , Lower_mall)

    #no_Lower_price_searched_keywords 셋팅(Lower_price만 찾고 Searched는 안 찾는 것(Ex. 부동산, 자동차, 숙박, 항공, 공연티켓, 기타 단독상품))

        no_Lower_price_searched_keywords = keyword_data['Condition_keyword']['no_Lower_price_searched_keywords']['Kor'] + keyword_data['Condition_keyword']['no_Lower_price_searched_keywords']['Eng']
        if any(no_Lower_price_searched_keyword in User_url + str(Lower_price_key) for no_Lower_price_searched_keyword in no_Lower_price_searched_keywords) == False:
            print("전후처리 전 Title_key값은 ", Title_key)

        # 설명 7번
            #title pre / post 처리 후 네이버쇼핑 최저가 검색 후 searched 값 도출

            # Title 전후처리

            # 전처리

            #패턴 1차: 대,일반 괄호(사이 한글 및 숫자 ,./포함) or |뒷문자(한글 및 숫자 ,./ 포함) 제거
            try:
                Title_pre_key = re.sub(r'\[[가-힣0-9%-,\. \/]*?\]|\(([가-힣0-9%-,\. \/]*?)\)|\|([가-힣0-9%-,\. \/]*?)', '', Title_key)
                print("1차, ", Title_pre_key)

            #패턴 2차: Disrtibutor_Kor 값 / 문자, 숫자, 한글이 아닌 값이 있는 경우 이를 제거 

                Title_pre_key = re.sub(Distributor_key,'',Title_pre_key)
                try:
                    Title_pre_key = re.sub(keyword_data['Distributor_keyword'][Distributor_key],'',Title_pre_key)
                except:
                    pass
                Title_pre_key = re.sub('[^\w가-힣 ]','',Title_pre_key)
                print("2차, ", Title_pre_key)

            #패턴 3차: 필요없는 값 제거 

                title_trash_words = keyword_data['Trash_keyword']['Title_searched']['Kor'] + keyword_data['Trash_keyword']['Title_searched']['Eng']
                for title_trash_word in title_trash_words:
                    Title_pre_key = Title_pre_key.replace(title_trash_word, "")
                print("3차, ", Title_pre_key)

                # regex로 Title_key 다 날릴 경우 대비

                if len(Title_pre_key.strip()) == 0:
                    Title_pre_key = Title_key

            except:
                Title_pre_key = Title_key

            print("Title_pre_key는 ", Title_pre_key)

            # 후처리: 제품번호 추출

            #패턴 2차: 영문 및 숫자로 이루어진 최소 6자리 제품번호 추출
        #~220713         pattern2 = re.compile("[A-Za-z\d\/]+[A-Za-z][a-zA-Z\d]{2}[a-zA-Z\d]+|[A-Za-z\d/]+[\d][a-zA-Z\d]{2}[A-Za-z][A-Za-z\d/]+") 
    #~220718         pattern2 = re.compile("((?=\S[A-Z])(?=\S*?[A-Z])(?=\S*?[0-9]).{6,})\S$|((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,})\S$") 
            pattern2 = re.compile('''(((?=[A-Z0-9])(?=[A-Za-z0-9]*?[A-Z])(?=[A-Za-z0-9]*?[0-9])[A-Za-z0-9]{7,})|
            ((?=[a-z])(?=[A-Za-z0-9]*?[a-z])(?=[A-Za-z0-9]*?[0-9])[A-Za-z0-9]{7,}))''')
            try:
                Title_post_key = pattern2.search(Title_pre_key).group()

                if Title_pre_key == Title_key:
                    Title_chosen_key = Title_post_key
                else:
                    if len(Title_pre_key) >= len(Title_post_key):
                        Title_chosen_key = Title_post_key
                    else:
                        Title_chosen_key = Title_pre_key

            except:
                Title_chosen_key = Title_pre_key
            finally:
                if (re.search('[0-9]m|[0-9] ml', Title_chosen_key)) != None:
                    Title_chosen_key = Title_pre_key    

            print("Title_chosen_key는, ", Title_chosen_key)
        # 설명 8번
            # Title_chosen_key 없을 경우, 탈출

            if Title_chosen_key == "해당 링크에서 직접 보기":

                Title_searched_key = "비교가를 찾을 수 없어요"
                Lower_price_searched_key = "비교가를 찾을 수 없어요"
                Lower_mall_searched_key = "비교가를 찾을 수 없어요"
                Lower_url_searched_key = "비교가를 찾을 수 없어요"

                Title_searched.append(Title_searched_key)
                Lower_price_searched.append(Lower_price_searched_key)
                Lower_mall_searched.append(Lower_mall_searched_key)
                Lower_url_searched.append(Lower_url_searched_key)

                print("Title_searched는 ", Title_searched)
                print("Lower_price_searched는 ", Lower_price_searched)
                print("Lower_mall_searched는 ", Lower_mall_searched)
                print("Lower_url_searched는 ", Lower_url_searched)

            # Title_chosen_key 있을 경우 최저가 검색 로직 구현
            else:
                try:
                    #최저가 검색: Title_pre or Title_post 를 활용하여 네이버 쇼핑 1순위(광고 제외) 검색 후 타이틀, 최저가, 최저가몰, URL 추출
                    if '&' in Title_chosen_key:
                        Title_chosen_key = Title_chosen_key.replace('&', '%26')
                    User_url_naver = 'https://search.shopping.naver.com/search/all?query=' + str(Title_chosen_key)
                    print("네이버쇼핑 검색 결과 주소?", User_url_naver)

                    headers = {'user-agent': generate_user_agent(device_type='smartphone')}
                    res = requests.get(User_url_naver, headers=headers) 
                    print("네이버쇼핑 검색 결과접속 상태?", res.status_code)
                    soup = BeautifulSoup(res.content, 'html.parser')

                    script = soup.select_one('script[type="application/json"]').text
                    dict_result_script_text = json.loads(str(script))
                    try:
                        naver_shopping_list_dict_list =  dict_result_script_text['props']['pageProps']['initialState']['products']['list'][0:]
                    except:
                        naver_shopping_list_dict_list =  dict_result_script_text['props']['pageProps']['dehydratedState']['queries'][2]['state']['data']['SearchAll']['bookSasResult']['itemList'][0]

                    if naver_shopping_list_dict_list:
                        for naver_shopping_list_dict_list_item in naver_shopping_list_dict_list:
                            try:
                                naver_shopping_list_dict_list_item = naver_shopping_list_dict_list_item['item']
                                if naver_shopping_list_dict_list_item.get('adId') == None:  
                                    try:
                                        Title_searched_key = naver_shopping_list_dict_list_item.get('productTitle')
                                    except:
                                        try:
                                            Title_searched_key = naver_shopping_list_dict_list_item.get('productTitleOrg')
                                        except:
                                            Title_searched_key = naver_shopping_list_dict_list_item.get('productName')

                                    try:
                                        Lower_price_searched_key = naver_shopping_list_dict_list_item.get('lowPrice')
                                    except:
                                        Lower_price_searched_key = naver_shopping_list_dict_list_item.get('mobilePrice')

                                    try:
                                        Lower_mall_searched_key = naver_shopping_list_dict_list_item['lowMallList'][0]['name']
                                    except:
                                        try:
                                            Lower_mall_searched_key = naver_shopping_list_dict_list_item['lowMallList'][0]['chnlName']
                                        except:
                                            try:
                                                Lower_mall_searched_key = naver_shopping_list_dict_list_item['mallName']
                                            except:
                                                Lower_mall_searched_key = naver_shopping_list_dict_list_item['mallNameOrg']

                                    Lower_url_searched_key = naver_shopping_list_dict_list_item['purchaseConditionInfos'][0]['crUrl']

                                    break;      
                            except:
                                Title_searched_key = naver_shopping_list_dict_list['title']
                                Lower_price_searched_key = naver_shopping_list_dict_list['lowPrice']
                                Lower_mall_searched_key = naver_shopping_list_dict_list['mallName']
                                Lower_url_searched_key = naver_shopping_list_dict_list['crUrl']      
                    else:
                        Title_searched_key = '비교된 상품이 없어요'
                        Lower_price_searched_key = '비교된 상품이 없어요'
                        Lower_mall_searched_key = '비교된 상품이 없어요'
                        Lower_url_searched_key = '비교된 상품이 없어요'
        #         # ip 차단으로 인해 하기 코드 사용 불가
        #             User_url_api = 'https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query=' + str(Title_chosen_key) + '&origQuery=' + str(Title_chosen_key)+ '&iq=&eq=&xq='

        #             print(User_url_api)
        # #             headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
        #             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

        #             res_api = requests.get(User_url_api, timeout=3, headers=headers) 

        #             if res_api.status_code != 200:
        #                 print("User_url_api 접속 오류입니다")

        #             res_api_json = json.loads(res_api.text)
        #     # 설명 9번
        #             #meta값
        #             try:
        #                 Title_searched_key = res_api_json['shoppingResult']['products'][0]['productTitle']
        #             except:
        #                 Title_searched_key = "조금 더 찾아봐야해요!"
        #             try:
        #                 Lower_price_searched_key = res_api_json['shoppingResult']['products'][0]['mobileLowPrice'] 
        #             except:
        #                 Lower_price_searched_key = "조금 더 찾아봐야해요!"
        #             try:
        #                 Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['lowMallList'][0]['name']
        #             except:
        #                 try:
        #                     Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['mallName']
        #                 except:
        #                     Lower_mall_searched_key = "조금 더 찾아봐야해요!"
        #             try:
        #                 Lower_url_searched_key = res_api_json['shoppingResult']['products'][0]['crUrl']
        #             except:
        #                 Lower_url_searched_key = "조금 더 찾아봐야해요!"

        #             print("네이버 쇼핑 최저가는, ", Lower_price_searched_key)

                except: #naver_open_api - 25,000회/1일 접속 가능
                    try:
                        print('naver_open_api 접속 시도')
                        naver_open_api = 'https://openapi.naver.com/v1/search/shop.json?query=' + Title_chosen_key + '&display=1'
                        print('naver_open_api? ', naver_open_api)
    #                     headers_naver_open_api = {'user-agent': generate_user_agent(device_type='smartphone'), "X-Naver-Client-Id":'kGjLkvRUDvR3yo09JJoV', "X-Naver-Client-Secret":'NLXuKVy6GG'}
                        headers_naver_open_api = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 
                                                  "X-Naver-Client-Id":'kGjLkvRUDvR3yo09JJoV', "X-Naver-Client-Secret":'kRm3qyLNTo'}
                        res_api = requests.get(naver_open_api, headers=headers_naver_open_api)

                        if res_api.status_code != 200:
                            print('naver_open_api 접속 오류')
                        else:
                            print('naver_open_api 접속 완료')
                            result_dict = json.loads(res_api.text)
                            try:
                                Title_searched_key = result_dict['items'][0]['title']
                                Title_searched_key_trash_words = ['<b>', '</b>']
                                for Title_searched_key_trash_word in Title_searched_key_trash_words:
                                    Title_searched_key = Title_searched_key.replace(Title_searched_key_trash_word, "")
                            except:
                                Title_searched_key = '비교가를 찾을 수 없어요'
                            try:
                                Lower_price_searched_key = result_dict['items'][0]['lprice']
                            except:
                                Lower_price_searched_key = '비교가를 찾을 수 없어요'
                            try:
                                Lower_mall_searched_key = result_dict['items'][0]['mallName']
                            except:
                                Lower_mall_searched_key = Lower_mall_searched_key
                            try:
                                Lower_url_searched_key = result_dict['items'][0]['link']
                            except:
                                Lower_url_searched_key = '비교가를 찾을 수 없어요'

                            try: #gate주소가 아닌  naver_catalog 주소 파악
                                product_id_naver_mall_url_re = re.compile('(?<=id=)[0-9]+')
                                product_id_naver_mall_url = product_id_naver_mall_url_re.findall(Lower_url_searched_key)[0]
                                Lower_url_searched_key_temp = 'https://search.shopping.naver.com/catalog/' + str(product_id_naver_mall_url)
                                res = requests.get(Lower_url_searched_key_temp, timeout=3, headers=headers) 
                                soup = BeautifulSoup(res.text, 'html.parser')
                                if '존재하지 않습니다' in str(soup): 
                                    print('Lower_url_searched_key_temp는 gate 주소, mall 직접 연결할 주소 파악 시작')
                                    res = requests.get(Lower_url_searched_key, timeout=3, headers=headers) 
                                    soup = BeautifulSoup(res.text, 'html.parser')
                                    script_text = soup.select_one('script[type="application/json"]').text
                                    dict_result_script_text = json.loads(script_text)
                                    Lower_url_searched_key = dict_result_script_text['props']['pageProps']['product']['productUrl']
                                else:
                                    print('naver_catalog 주소 파악')
                                    Lower_url_searched_key = Lower_url_searched_key_temp           
                            except:
                                print('naver_catalog 주소 파악')
                                Lower_url_searched_key = Lower_url_searched_key
                    except:
                        Title_searched_key = '비교된 상품이 없어요'
                        Lower_price_searched_key = '비교된 상품이 없어요'
                        Lower_mall_searched_key = '비교된 상품이 없어요'
                        Lower_url_searched_key = '비교된 상품이 없어요'

            # Lower_price_searched_key 전처리

            Lower_price_searched_key = str(Lower_price_searched_key).strip()

            Lower_price_searched_key = re.sub(r'([^0-9]*?)', '', Lower_price_searched_key)

            if Lower_price_searched_key == "":

                Lower_price_searched_key = "비교된 상품이 없어요"

            else:        
                Lower_price_searched_key = int(float(Lower_price_searched_key))   

            # price 비교: 둘 다 int 이며 0이 아닐 경우 시행

            if type(Lower_price_key) and type(Lower_price_searched_key) == int:
                try: 
                    if Lower_price_key < Lower_price_searched_key and Lower_price_key & Lower_price_searched_key != 0:
                        Lower_price_searched_key = Lower_price_key
                        Lower_mall_searched_key = Distributor_key
                        Lower_url_searched_key = User_url
                        print("가격 비교 성공")
                except:
                    print("가격 비교 불가")
            
        else:
            if Lower_price_key == '비교가를 찾을 수 없어요':
                Title_searched_key = '비교가를 찾을 수 없어요'
                Lower_price_searched_key = '비교가를 찾을 수 없어요'
                Lower_mall_searched_key = '비교가를 찾을 수 없어요'
                Lower_url_searched_key = '비교가를 찾을 수 없어요'
            else:
                Title_searched_key = '-'
                Lower_price_searched_key = '-'
                Lower_mall_searched_key = '-'
                Lower_url_searched_key = '-'
    else:
        print('Lower_price_key 탐색 불필요 대상임')
        Lower_price_key = '-'
        Lower_price.append(Lower_price_key)
        print('Lower_price는? ', Lower_price)
        
        Title_searched_key = '-'
        Lower_price_searched_key = '-'
        Lower_mall_searched_key = '-'
        Lower_url_searched_key = '-'

    Title_searched.append(Title_searched_key) #프론트에 안나옴
    if type(Lower_price_searched_key) == int:
        Lower_price_searched_key = format(Lower_price_searched_key, ',')  + "원"
        Lower_price_searched.append(Lower_price_searched_key)
        Lower_price_searched_key = int(Lower_price_searched_key.replace("원", "").replace(",", ""))
    else:
        Lower_price_searched.append(Lower_price_searched_key)
    #Distributor와 비교가 몰 이름 통일    
    if Lower_mall_searched_key in keyword_data['Distributor_keyword']:
        Lower_mall_searched_key = keyword_data['Distributor_keyword'][Lower_mall_searched_key]
    
    elif Lower_mall_searched_key in User_url_list:
        Lower_mall_searched_key = Distributor_key
    else:
        Lower_mall_searched_key = Lower_mall_searched_key
        
    Lower_mall_searched.append(Lower_mall_searched_key.strip("'"))
    Lower_url_searched.append(Lower_url_searched_key)

    print("프론트에 안나옴, Title_searched는 ", Title_searched)
    print("Lower_price_searched는 ", Lower_price_searched)
    print("Lower_mall_searched는 ", Lower_mall_searched)
    print("Lower_url_searched는 ", Lower_url_searched)

#Distributor_key 한글화 / 네이버 쇼핑몰 검색결과와 동일하게 설정하기
try:
    Distributor_keyword_list_Kor_dict = {k.lower():v for k, v in keyword_data['Distributor_keyword'].items()}
    Distributor_key = Distributor_keyword_list_Kor_dict[Distributor_key.lower()]
    print("Distributor_key 한글화 적용 성공, ", Distributor_key)
except:
    #NHN(고도몰)
    print("Distributor_key 태그 탐색 시도")
    if 'goods_view'in User_url:
        Distributor_name = soup.select_one('meta[property="og:description"]')['content']
        if len(Distributor_name) < 6:
            Distributor_key = Distributor_name
    else:
        try:
            Distributor_name = soup.select_one('meta[property="og:site_name"]')['content']
            if len(Distributor_name) < 8:
                Distributor_key = Distributor_name
        except:
            try: # 코리아센터
                script_re = re.compile('(?<=var shop_name = ).+(?=;)')
                Distributor_key = script_re.findall(str(soup))[0] 
            except:
                try:
                    Distributor_key = soup.select_one('meta[name="application-name"]')['content']
                except:
                    try:
                        Distributor_key = soup.select_one('meta[property="al:android:app_name"]')['content']
                    except:
                        try:
                            Distributor_key = soup.select_one('meta[property=""apptitle]')['content']
                        except:
                            print("Distributor_key 태그 탐색 실패")
                            Distributor_key = Distributor_key

# Distributor는 모두 대문자로
try:
    Distributor_key = Distributor_key.upper()
except:
    pass

print("최종 Distributor 값은 ", Distributor_key)
Distributor.append(Distributor_key)

print("scraping complete")


# # 접속 기록 확인(ip, headers for AWS)
try:
    access_test = 'http://httpbin.org/get'
    res = requests.get(access_test, headers=headers, timeout = 5) 
    print('''접속 기록 확인!!!   ''',res.text)
except:
    print("접속 기록 확인 불가, httpbin.org/get 사이트 점검 필요")

# 설명 10번

# # DB update

#DB 오픈

sql = '''
SELECT * FROM posts
'''
try:
    cur.execute(sql)
except:
    print('NO_mysql select, execute')
#userid 와 일치하는 posts_id 찾기

#DB commit이 되었다면 / 전체 DB 중 userid 값을 id 값으로 가지고 있는 것 중에서 가장 마지막 행의 id 값 / 
#DB commit이 안 되었다면 / 

try:
    print("try2")
    db_all_data = cur.fetchall() #fetch를 먹이면 tuple 형식으로 db data를 읽어옴
    db_last_data = db_all_data[-1]
    print('db_last_data', db_last_data)
    db_last_data_id = db_last_data[-9]
    print('db_last_data_id', db_last_data_id)
    print('UserId ', UserId)
    posts_id = db_last_data[0] 
    print("posts_id: ", posts_id)        
except:
    print('NO_mysql db_data reading')
if  db_last_data_id == UserId:
    print('UserId matching success')
else:
    print('NO_UserId matching success')
all_list_expt_user_url = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched

for list_one in all_list_expt_user_url:
    if len(list_one) == 0:
        list_one.append("no_data")
    elif len(list_one) > 1:
        del list_one[0]
        
all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, 
                  Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, 
                  Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, 
                  Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, 
                  createdAt, updatedAt, Mymemo, MyThema)

# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, 
#                   Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, 
#                   Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, 
#                   Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched)

sql = '''
UPDATE posts SET
    Type = %s, 
    Category_in = %s, 
    Distributor = %s, 
    Publisher = %s, 
    Category_out = %s, 
    Logo_image = %s, 
    Channel_logo = %s, 
    Thumbnail_image = %s, 
    User_url = %s, 
    Title = %s, 
    Maker = %s, 
    Date = %s, 
    Summary = %s, 
    crawl_Content = %s, 
    Emotion_cnt = %s, 
    Comm_cnt = %s, 
    Description = %s, 
    Comment = %s, 
    Tag = %s, 
    View_cnt = %s, 
    Duration = %s, 
    Lower_price = %s, 
    Lower_mall = %s, 
    Lower_price_card = %s, 
    Lower_mall_card = %s, 
    Star_cnt = %s, 
    Review_cnt = %s, 
    Review_content = %s, 
    Dscnt_rate = %s, 
    Origin_price = %s, 
    Dlvry_price = %s, 
    Dlvry_date = %s, 
    Model_no = %s, 
    Color = %s, 
    Location = %s, 
    Title_searched = %s, 
    Lower_price_searched = %s, 
    Lower_mall_searched = %s, 
    Lower_url_searched = %s, 
    UserId = %s, 
    createdAt = %s, 
    updatedAt = %s, 
    Mymemo = %s, 
    MyThema = %s
    WHERE id = %s
'''

# sql = '''
# UPDATE posts SET
#     Type = %s, 
#     Category_in = %s, 
#     Distributor = %s, 
#     Publisher = %s, 
#     Category_out = %s, 
#     Logo_image = %s, 
#     Channel_logo = %s, 
#     Thumbnail_image = %s, 
#     User_url = %s, 
#     Title = %s, 
#     Maker = %s, 
#     Date = %s, 
#     Summary = %s, 
#     crawl_Content = %s, 
#     Emotion_cnt = %s, 
#     Comm_cnt = %s, 
#     Description = %s, 
#     Comment = %s, 
#     Tag = %s, 
#     View_cnt = %s, 
#     Duration = %s, 
#     Lower_price = %s, 
#     Lower_mall = %s, 
#     Lower_price_card = %s, 
#     Lower_mall_card = %s, 
#     Star_cnt = %s, 
#     Review_cnt = %s, 
#     Review_content = %s, 
#     Dscnt_rate = %s, 
#     Origin_price = %s, 
#     Dlvry_price = %s, 
#     Dlvry_date = %s, 
#     Model_no = %s, 
#     Color = %s, 
#     Location = %s, 
#     Title_searched = %s, 
#     Lower_price_searched = %s, 
#     Lower_mall_searched = %s, 
#     Lower_url_searched = %s
#     WHERE id = %s
# '''

try:
    cur.execute(sql, (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt, Mymemo, MyThema, posts_id, ))
except:
    print('NO_last execute')

# try:
#     cur.execute(sql, (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, posts_id, ))
# except:
#     print('NO_last execute')

db.commit()

# ("UPDATE accounts SET Q001 = %s, Q002 = %s WHERE id = %s", (Q001, Q002, session['id'],))
print("save complete")

db.close()

# # 테스트
# # DB_input

# all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched


# for list_one in all_list:
#     if len(list_one) == 0:
#         list_one.append("no_data")

# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, Mymemo, MyThema)

# sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, Mymemo, MyThema) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# cur.execute(sql, all_list_tuple)

# db.commit()
# print("save complete")

# db.close()


# # 라니 오픈 (제이 클로즈)

# DB_input

# dt_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
# createdAt = dt_kst
# updatedAt = dt_kst

# all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched

# for list_one in all_list:
#     if len(list_one) == 0:
#         list_one.append("no_data")

# #DB 주의사항: all_list_tuple과 sql의 'INSERT INTO post ( 컬럼 )'의 인자들 순서를 동일하게 설정해야 함 (DB 내 칼럼 순서와 일치하지 않아도 됨)
# #다만, DB의 칼럼과 칼럼 명이 다르거나, DB에 칼럼을 새로 생성한다면, all_list_tuple과 sql에도 해당 인자를 추가해야 함

# # all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId)

# # sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, createdAt, updatedAt, UserId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)"
# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt, Mymemo, MyThema)

# sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, crawl_Content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt, Mymemo, MyThema) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# cur.execute(sql, all_list_tuple)

# db.commit() 
# print("save complete")

# db.close()

