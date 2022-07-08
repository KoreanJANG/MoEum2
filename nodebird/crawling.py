#!/usr/bin/env python
# coding: utf-8

# In[1]:



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
import sys;
from urllib import parse


# data - mysql DB 접속 #라니 오픈
try:
    db = pymysql.connect(host="login-lcture-fnu.cjk00gposwcb.ap-northeast-2.rds.amazonaws.com",
                         user='admin', password='zang0903!!', db='nodebird', charset='utf8mb4')
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
Crawl_content = []
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

# 라니 오픈
# https://wikidocs.net/16049 참고
# 파이썬 실팽시 파라미터로 url 받도록 수정
User_url = sys.argv[1]
# 파이썬 실팽시 파라미터로 user id 받도록 수정
UserId = sys.argv[2]

# # 제이 오픈
# User_url = input("???")

#설명 1번

#url accessibility check

#FB 헤더값
headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

#개인 헤더값
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

res = requests.get(User_url, headers = headers) 
if res.status_code != 200:
    print("URL 오류입니다")

# url redirection 잡기
        
if 'msearch' in User_url:

    User_url = User_url.replace("https://msearch", "https://search")
elif 'm.' in User_url:
    User_url = User_url.replace("https://m.", "https://")

try:
    with urllib.request.urlopen(User_url) as response:
        User_url = response.geturl()
        print("Redirection된 URL은, ", User_url)
except:
    
    User_url = User_url
    print("No Redirection된 URL은, ", User_url) 

# naver 앱 url(shorten and redirection and decode)
if 'link.naver.com' in User_url:

    User_url_decoded = parse.unquote(User_url)
#     print("User_url_decoded URL은, ", User_url_decoded) 

    User_url_decoded_re = re.compile('(?<=bridge\?url\=)(.*?)(?=\&dst)')

    User_url_decoded_red1 = User_url_decoded_re.findall(User_url_decoded)

    for User_url_decoded_red in User_url_decoded_red1:
        User_url = User_url_decoded_red
        
        print("link.naver의 redirection은", User_url)
               
#     if 'msearch' in User_url:
        
#         User_url = User_url.replace("https://msearch", "https://search")
        
#         print("User_url은? ", User_url)
    
# url split

User_url_list = re.split('\.|/|\?', User_url)

print("User_url_list는 ", User_url_list)

# DIstributor 키워드가 2개 이상 들어간 경우를 대비, 0~6번째까지 추출하여 Dstributor_key 와 매칭

User_url_list_Distributor = User_url_list[0:6]

print("User_url_list_Distributor는 ", User_url_list_Distributor)

# 설명 2번

# Distributor keyword input

Distributor_keyword_list = ['naver', 'coupang', '11st', 'tistory', 'daangn', 'instagram', 'musinsa', 'a-bly', 'zigzag', 
                            'brandi', 'gmarket', 'oliveyoung', 'wemakeprice', 'tmon', 'auction', 'gsshop', 'hnsmall', 'cjonstyle', 
                            'joongna', 'joonggonara', 'bunjang', 'facebook', 'velog', 'github', 'youtube', 'tiktok', 'google',
                           'aliexpress', 'amazon', 'ebay', 'interpark']

#Distributor 한글화 ( for Title 전처리 시 Distributor 한글 이름 제외 )

Distributor_keyword_list_Kor_dict = {'naver':'네이버', 'coupang':'쿠팡', '11st':'11번가', 'tistory':'티스토리', 'daangn':'당근마켓',
                                     'instagram':'인스타그램', 'musinsa':'무신사', 'a-bly':'에이블리', 'zigzag':'지그재그', 
                                     'brandi':'브랜디', 'gmarket':'지마켓', 'oliveyoung':'올리브영', 'wemakeprice':'위메프', 
                                     'tmon':'티몬', 'auction':'옥션', 'gsshop':'GS샵', 'hnsmall':'홈앤쇼핑', 'cjonstyle':'CJ', 
                                     'joongna':'중고나라', 'joonggonara':'중고나라', 'bunjang':'번개장터', 'facebook':'페이스북',
                                     'velog':'velog', 'github':'github', 'youtube':'유튜브', 'tiktok':'tictok', 'google':'google',
                                     'aliexpress':'aliexpress', 'amazon':'amazon', 'ebay':'ebay', 'interpark':'인터파크'}
# keyword 추가 필요

# url - Distributor_keyword list match

# soup 정의 설정
# ua = UserAgent(use_cache_server=True)

soup = BeautifulSoup(res.content, 'html.parser')

Distributor_keyword_match_list = list(
    set(User_url_list_Distributor).intersection(Distributor_keyword_list))
print("Distributor_keyword_match_list은", Distributor_keyword_match_list)
if len(Distributor_keyword_match_list) >= 1:

    Distributor_key = Distributor_keyword_match_list[0]

else:

    try:
        Distributor_key = soup.select_one(
            'meta[property="og:site_name"]')['content']
    except:
        try:
            Distributor_key = soup.select_one('title').get_text()
        except:
            Distributor_key = "해당 링크에서 직접 보기"

print("Distributor_key 값은 ", Distributor_key)

# 설명 3번

# Category_in_keyword input

Category_in_keyword_list_shopping = ['11st', 'coupang', 'musinsa', 'a-bly', 'zigzag', 'brandi', 'gmarket', 'oliveyoung',
                                     'wemakeprice', 'idus', 'tmon', 'auction.', 'gsshop.', 'shopping', 'smartstore', 
                                     'hnsmall', 'cjonstyle', 'brand.naver', 'store', 'products', 'product', 'wemakeprice', 
                                     'tmon', 'goods', 'aliexpress', 'amazon', 'ebay', 'interpark']
Category_in_keyword_list_blog = ['blog', 'tistory', 'velog', 'github', 'contents', 'premium', 'post']
Category_in_keyword_list_sns = ['instagram', 'band', 'facebook']
Category_in_keyword_list_video = ['youtube', 'tiktok', 'tv']
Category_in_keyword_list_second = ['daangn', 'joonggonara', 'joongna', 'bunjang', 'products', 'shop']
Category_in_keyword_list_cafe = ['cafe']
Category_in_keyword_list_news = ['news', 'joongang', 'yna', 'weather', 'entertain']
Category_in_keyword_list_images = ['img', 'jpg', 'png', 'jpeg']
Category_in_keyword_list_enter = ['book', 'music', 'music-flo']

# keyword 추가 필요

# url - Distributor_keyword list match

#url - Distributor_keyword list match

Category_in_keyword_list_all = [Category_in_keyword_list_cafe, Category_in_keyword_list_news, 
                                Category_in_keyword_list_shopping, Category_in_keyword_list_blog, Category_in_keyword_list_sns, 
                                Category_in_keyword_list_video, Category_in_keyword_list_second, Category_in_keyword_list_images,
                                Category_in_keyword_list_enter]

Category_in_keyword_dict = {'image' : Category_in_keyword_list_images, 'news' : Category_in_keyword_list_news, 
                            'cafe' : Category_in_keyword_list_cafe, 'second' : Category_in_keyword_list_second, 
                            'blog' : Category_in_keyword_list_blog, 'shopping' : Category_in_keyword_list_shopping, 
                            'sns' : Category_in_keyword_list_sns, 'video' : Category_in_keyword_list_video,
                            'enter' : Category_in_keyword_list_enter}

#해결필요: Category_in_keyword_dict 의 vlaues 값 중복 시 마지막 하나만 표현(dict 고유의 성격), 따라서 key값이 마지막것으로 표현됨

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

Category_in.append(Category_in_key)

print("Category_in 리스트 값은 ", Category_in)

#Publisher & Distributor & Category_out 파악

if Category_in_key == 'news':

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
        Distributor_key = Publisher_key

    except: 
        Publisher_key = "해당 링크에서 직접 보기"

    Publisher.append(Publisher_key)

    Distributor.append(Distributor_key)

    print("Publisher 리스트 값은 ", Publisher)
    print("수정된 Distributor 리스트 값은 ", Distributor)

else:
    Distributor.append(Distributor_key)
    print("Distributor 리스트 값은 ", Distributor)

# 설명 4번
# Type 파악

if Category_in_key in ['news', 'cafe', 'blog']:
    Type_key = "글"

elif Category_in_key in ['shopping', 'second']:
    Type_key = "쇼핑"

elif Category_in_key in ['video', 'enter']:
    Type_key = "동영상"

elif Category_in_key in ['sns']:
    Type_key = "이미지"

    # jpg 등 이미지 확장자가 url에 포함된 경우 이를 이미지로 분류
elif any(Category_in_keyword_list_image in User_url for Category_in_keyword_list_image in Category_in_keyword_list_images) == True:
    Type_key = "이미지"

else:
    Type_key = "기타"

Type.append(Type_key)
print("Type 리스트 값은 ", Type)

#설명 5번

# meta값 도출
headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

res = requests.get(User_url, headers=headers) 
soup = BeautifulSoup(res.content, 'html.parser')

if 'blog.naver' in User_url:
#설명 5번_iframe
    #iframe 대비 src_url 설정
    #FB일 경우 SRC 탐색 X
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    res = requests.get(User_url, headers=headers) 
    soup = BeautifulSoup(res.content, 'html.parser')
    
    src_url = "https://blog.naver.com/" + soup.iframe['src']
    print(src_url)
    res_iframe = requests.get(src_url, headers=headers)
#     res_noifr.status_code
    soup_iframe = BeautifulSoup(res_iframe.content, "html.parser") 
    try:
        Title_key = soup_iframe.select_one('meta[property="og:title"]')['content']    
    except:
        Title_key = "해당 링크에서 직접 보기"
    try:
        Description_key = soup_iframe.select_one('meta[property="og:description"]')['content']
    except:
        Description_key = "해당 링크에서 직접 보기"
    try:
        Thumbnail_image_key = soup_iframe.select_one('meta[property="og:image"]')['content']
    except:
        Thumbnail_image_key = "해당 링크에서 직접 보기"

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
#설명 5번_api    
    #내부 API
    #header값을 유저로 설정 -> meta값 이외 스크래핑 가능

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
    res = requests.get(User_url, headers=headers) 
    soup = BeautifulSoup(res.content, 'html.parser')

    article_no = User_url_list[6] #여기 인덱스 수정. regex로 가져오기( /d+{}
#     print("article_no", article_no)

    clubid = soup.select_one('input[name="clubid"]')['value']
#     print("clubid ", clubid )

    User_url_api = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/' + str(clubid) + '/articles/' + str(article_no)
    print(User_url_api)
    
    res_api = requests.get(User_url_api, headers=headers) 
    if res_api.status_code != 200:
        print("User_url_api 접속 오류입니다")

    #내부 api 
    soup_api = BeautifulSoup(res_api.text, 'html.parser')

    script_api = soup_api.text
    dict_result_script_api = json.loads(script_api)

    #meta값
    try:
        Title_key = dict_result_script_api['result']['article']['subject']
    except:
        try: 
            #header값을 FB으로 설정 -> meta값만 스크래핑 가능
            headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
            res = requests.get(User_url, headers=headers) 
            soup = BeautifulSoup(res.content, 'html.parser')
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            try:
                #selenium 크롤링 설정(iframe 다중)
                soup = BeautifulSoup(res.text, 'html.parser')

                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('disable-gpu')
                options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                options.add_argument('lang = ko_KR')


                # 드라이버 생성
                # chromedriver 설치된 경로를 정확히 기재해야 함
                chromedriver = 'D/moEum/nodejs-book-master/ch9/9.5.6_파이썬 연동 처리/9.5.4_검색_삭제처리_완료/nodebird/chromedriver.exe'  # 윈도우
                # chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥
                driver = webdriver.Chrome(chromedriver, options=options)

                # 크롤링할 사이트 호출
                driver.get(User_url)
                # iframe 진입
                driver.switch_to.frame("cafe_main")

                res_iframe = driver.page_source
                soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                Title_key = soup_iframe.select_one('h3.title_text').get_text()
                driver.quit()
            except:
                Title_key = "해당 링크에서 직접 보기"

    try:
        Description_key = dict_result_script_api['result']['article']['contentHtml']
    except: # Publisher (카페 네임)
        try:
            Description_key = dict_result_script_api['result']['cafe']['pcCafeName']
        except:
            try:
                #header값을 FB으로 설정 -> meta값만 스크래핑 가능
                headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
                res = requests.get(User_url, headers=headers) 
                soup = BeautifulSoup(res.content, 'html.parser')
                Description_key = soup.select_one('meta[property="og:description"]')['content']
            except:
                try:                    
                    #selenium 크롤링 설정(iframe 다중)
                    soup = BeautifulSoup(res.text, 'html.parser')

                    options = webdriver.ChromeOptions()
                    options.add_argument('headless')
                    options.add_argument('disable-gpu')
                    options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                    options.add_argument('lang = ko_KR')
                    # 드라이버 생성
                    # chromedriver 설치된 경로를 정확히 기재해야 함
                    chromedriver = 'D/moEum/nodejs-book-master/ch9/9.5.6_파이썬 연동 처리/9.5.4_검색_삭제처리_완료/nodebird/chromedriver.exe'  # 윈도우
                    # chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥
                    driver = webdriver.Chrome(chromedriver, options=options)

                    # 크롤링할 사이트 호출
                    driver.get(User_url)
                    # iframe 진입
                    driver.switch_to.frame("cafe_main")

                    res_iframe = driver.page_source
                    soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                    Description_key = soup_iframe.select_one('div.se-main-container').get_text()
                    driver.quit()
                except:
                    Description_key = "해당 링크에서 직접 보기"

    try: 
        # 카페 대표 썸네일 (게시물 썸네일 불러올 경우 Selenium 필요)
        Thumbnail_image_key = dict_result_script_api['result']['cafe']['image']['url']
    except:
        try: 
            #header값을 FB으로 설정 -> meta값만 스크래핑 가능
            headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
            res = requests.get(User_url, headers=headers) 
            soup = BeautifulSoup(res.content, 'html.parser')
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
        except:
            try:
                #selenium 크롤링 설정(iframe 다중)
                soup = BeautifulSoup(res.text, 'html.parser')

                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('disable-gpu')
                options.add_argument('User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')
                options.add_argument('lang = ko_KR')
                # 드라이버 생성
                # chromedriver 설치된 경로를 정확히 기재해야 함
                chromedriver = 'D/moEum/nodejs-book-master/ch9/9.5.6_파이썬 연동 처리/9.5.4_검색_삭제처리_완료/nodebird/chromedriver.exe'  # 윈도우
                # chromedriver = '/usr/local/Cellar/chromedriver/chromedriver' # 맥
                driver = webdriver.Chrome(chromedriver, options=options)

                # 크롤링할 사이트 호출
                driver.get(User_url)
                # iframe 진입
                driver.switch_to.frame("cafe_main")

                res_iframe = driver.page_source
                soup_iframe = BeautifulSoup(res_iframe, "html.parser")
                Title_key = soup_iframe.select_one('h3.title_text').get_text()
                driver.quit()
            except:
                try:
                    se_main_container = soup_iframe.select_one('div.se-main-container')
                    Thumbnail_image_key = se_main_container.select_one('img')['src']
                    driver.quit()                  
                except:
                    Thumbnail_image_key = "해당 링크에서 직접 보기"
                
elif 'coupang' in User_url:
#설명 5번_script        
    headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

    #일반 bs

    res = requests.get(User_url, headers=headers) 

    soup = BeautifulSoup(res.text, 'html.parser')

    try:

        script_re = re.compile('(?<=exports.sdp =).+')
        script_text1 = script_re.findall(str(soup))
        script_text = str(script_text1[0].strip().replace(';', ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Title_key = dict_result_script_text['itemName']
        except:
                Title_key = dict_result_script_text['title']

        Description_key1 = dict_result_script_text['sellingInfoVo']['sellingInfo']    
        for Description_key in Description_key1:
            Description_key = Description_key
            
        Thumbnail_image_key = dict_result_script_text['images'][0]['detailImage']    

    except:

        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            try:
                Title_key = soup.select_one('title').get_text()
            except:
                Title_key = "해당 링크에서 직접 보기"

        try:
            Description_key = soup.select_one('meta[property="og:description"]')['content']
        except:
            Description_key = "해당 링크에서 직접 보기"
                
        try:
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
        except:
            Thumbnail_image_key = "해당 링크에서 직접 보기"    


elif 'gmarket' in User_url:
#설명 5번_일반(bs)
    print("응답코드: ", res.status_code)

    try:
        #         Title_key = soup.select_one('meta[property="og:title"]')['content']
        Title_key = soup.select_one(
            'meta[property="og:description"]')['content']
    except:
        try:
            Title_key = soup.select_one('title').get_text()
        except:
            Title_key = "해당 링크에서 직접 보기"

    try:
        Description_key = soup.select_one(
            'meta[property="og:description"]')['content']
    except:
        Description_key = "해당 링크에서 직접 보기"

    try:
        if Type_key == '이미지' and Category_in_key != 'sns':
            Thumbnail_image_key = User_url
        else:
            Thumbnail_image_key = soup.select_one(
                'meta[property="og:image"]')['content']
    except:
        Thumbnail_image_key = "해당 링크에서 직접 보기"

elif 'oliveyoung' in User_url:

    print("응답코드: ", res.status_code)

    try:
        Title_key = soup.select_one('p.prd_name').get_text()
    except:
        try:
            Title_key = soup.select_one('title').get_text()
        except:
            Title_key = "해당 링크에서 직접 보기"

    try:
        Description_key = soup.select_one(
            'meta[property="og:description"]')['content']
    except:
        Description_key = "해당 링크에서 직접 보기"

    try:
        if Type_key == '이미지' and Category_in_key != 'sns':
            Thumbnail_image_key = User_url
        else:
            Thumbnail_image_key = soup.select_one('div > #mainImg')['src']
    except:
        Thumbnail_image_key = "해당 링크에서 직접 보기"
        
elif 'wemakeprice' in User_url:
#설명 5번_selenium    
#     라니 오픈
    chromedriver = 'D/moEum/nodejs-book-master/ch9/9.5.6_파이썬 연동 처리/9.5.4_검색_삭제처리_완료/nodebird/chromedriver.exe'  # 윈도우
#     #제이 클로즈
#     chromedriver = 'C:/Users/FNUCNI/chromedriver.exe'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('User-Agent: facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)')
    options.add_argument('lang = ko_KR')

    driver = webdriver.Chrome(chromedriver, options=options)

    driver.get(User_url)
    User_url = driver.current_url

    print('final redirected url은', User_url)
    
    headers = {'user-agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}

    res = requests.get(User_url, headers=headers) 
    soup = BeautifulSoup(res.content, 'html.parser')
    
    script_re = re.compile('(?<=initialData\'\, JSON\.parse\(\').+')
    script_text1 = script_re.findall(str(soup))

    script_text = str(script_text1[0].strip().replace("'));", "").replace('\\"',"").replace("\\", "").replace("[\t\n\r\f\v]", ""))
    dict_result_script_text = json.loads(script_text)

    try:

        try:
            Title_key = dict_result_script_text['dealNm']
        except:
            Title_key = dict_result_script_text['ogTitle']

        try:
            Description_key = dict_result_script_text['dcateNm']
        except:
            Description_key = dict_result_script_text['lcateNm']        

        try:
            Thumbnail_image_key = dict_result_script_text['mainImgList'][0]['thumb']['imgUrl']
        except:
            Thumbnail_image_key = dict_result_script_text['mainImgList'][0]['origin']['imgUrl']

    except:

        try:
            Title_key = soup.select_one('meta[property="og:title"]')['content']
        except:
            try:
                Title_key = soup.select_one('title').get_text()
            except:
                Title_key = "해당 링크에서 직접 보기"

        try:
            Description_key = soup.select_one('meta[property="og:description"]')['content']
        except:
            Description_key = "해당 링크에서 직접 보기"

        try:
            Thumbnail_image_key = soup.select_one('meta[property="og:image"]')['content']
        except:
            Thumbnail_image_key = "해당 링크에서 직접 보기"  

  
elif 'bunjang' in User_url:

    product_id_bunjang_re = re.compile('(?<=products\/)[0-9]+')

    product_id_bunjang1 = product_id_bunjang_re.findall(User_url)

    for product_id_bunjang in product_id_bunjang1:
        User_url_api = 'https://api.bunjang.co.kr/api/1/product/' + str(product_id_bunjang) + '/detail_info.json?version=4'

    res_api = requests.get(User_url_api, headers = headers) 

    if res_api.status_code != 200:
        print("User_url_api 접속 오류입니다")

    result_dict = json.loads(res_api.text)

    try:
        Title_key = result_dict['item_info']['name']
    except:
        Title_key = "해당 링크에서 직접 보기"

    try:
        Description_key = result_dict['item_info']['description']
    except:
        Description_key = "해당 링크에서 직접 보기"

    try:
        Thumbnail_image_key = result_dict['item_info']['product_image']
    except:
        Thumbnail_image_key = "해당 링크에서 직접 보기"

else:
    # bs4 크롤링 설정

    print("응답코드 bs4 일반: ", res.status_code)

    try:
        Title_key = soup.select_one('meta[property="og:title"]')['content']
    except:
        try:
            Title_key = soup.select_one('title').get_text()
        except:
            Title_key = "해당 링크에서 직접 보기"

    try:
        Description_key = soup.select_one(
            'meta[property="og:description"]')['content']
    except:
        Description_key = "해당 링크에서 직접 보기"

    try:
        if Type_key == '이미지' and Category_in_key != 'sns':
            Thumbnail_image_key = User_url
        else:
            Thumbnail_image_key = soup.select_one(
                'meta[property="og:image"]')['content']
    except:
        Thumbnail_image_key = "해당 링크에서 직접 보기"

    if Distributor_key == "youtube":
        try:
            Duration_key = soup.select_one(
                'meta[itemprop="duration"]')['content']
            Duration_key = Duration_key.replace(
                "PT", "").replace("M", "분 ").replace("S", "초")

        except:
            Duration_key = "해당 링크에서 직접 보기"
        Duration.append(Duration_key)
        print("Duration 리스트 값은, ", Duration)

Title.append(Title_key.strip())    
Description.append(Description_key.strip().replace("\r\n", "").replace("\ufeff", "").replace("\n", ""))    
Thumbnail_image.append(Thumbnail_image_key.strip())
11
print('Title 리스트 값은, ', Title)
print('Description 리스트 값은, ', Description)
print('Thumbnail_image 리스트 값은, ', Thumbnail_image)
#설명 6번
# lprice & mall 파악

if Type_key == '쇼핑':
    print("현재 가격 스크래핑 시작")

# 쇼핑 Distributor 주요 0개사 지정

    # 11번가
    if Distributor_key in ['11st']:
        try:
            Lower_price_key = soup.select_one(
                'div.b_product_info_price.b_product_info_price_style2 > div > div > ul > li > dl.price > dd > strong > span.value').text
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    # 쿠팡
    elif Distributor_key in ['coupang']:

        if 'trip.coupang' in User_url: # 쿠팡 트립

            try:
                script_text1 = soup.select_one('script#travel-detail-product-data').get_text()
                dict_result_script_text = json.loads(script_text1)
                Lower_price_key = dict_result_script_text['product']['representativeVendorItem']['price']['totalSalesPrice']

            except:
                Lower_price_key = "해당 링크에서 직접 보기"

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
    elif Distributor_key in ['musinsa']:
        try:
            Lower_price_key = soup.select_one('#goods_price').text
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    # 번개장터
    elif Distributor_key in ['bunjang']:
        try:
            Lower_price_key = result_dict['item_info']['price']
            if result_dict['item_info']['status'] == "3":
                Lower_price_key = "품절인가봐요!"
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    #에이블리
    elif Distributor_key in ['a-bly']:

        product_id_alby_re = re.compile('(?<=goods\/)[0-9]+')
        product_id_alby1 = product_id_alby_re.findall(User_url)

        for product_id_alby in product_id_alby1:
            User_url_api = 'https://api.a-bly.com/webview/goods/' + str(product_id_alby)

        res_api = requests.get(User_url_api, headers = headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        result_dict = json.loads(res_api.text)

        try:
            Lower_price_key = result_dict['goods']['representative_option']['member_level_price']
        except:
            try:
                Lower_price_key = result_dict['goods']['representative_option']['price']
            except:
                try:
                    Lower_price_key = result_dict['goods']['representative_option']['original_price']
                except:
                    Lower_price_key = "해당 링크에서 직접 보기"

    # 지그재그
    elif Distributor_key in ['zigzag']:

        # product_id regex

        product_id_re = re.compile('(?<=p\/)[0-9]+')
        product_id1 = product_id_re.findall(User_url)

        # store url 확인

        for product_id in product_id1:
            User_url_rd = 'https://store.zigzag.kr/catalog/products/' +                 str(product_id)

        res_rd = requests.get(User_url_rd, headers=headers)

        if res_rd.status_code != 200:
            print("User_url_api 접속 오류입니다")

        # store. zigzag 링크 - js 스크래핑

        soup_rd = BeautifulSoup(res_rd.text, 'html.parser')

        script_rd = soup_rd.select_one('#__NEXT_DATA__')
        script_rd = script_rd.text

        dict_result_rd = json.loads(script_rd)

        try:
            Lower_price_key = dict_result_rd['props']['pageProps']['product']['product_price']['final_price']
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    # 브랜디
    elif Distributor_key in ['brandi']:
        try:
            Lower_price_key = soup.select_one('p.price').text
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    # 지마켓
    elif Distributor_key in ['gmarket']:
        try:
            Lower_price_key = soup.select_one('strong.price_real').text
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    # 올리브영
    elif Distributor_key in ['oliveyoung']:
        try:
            Lower_price_key = soup.select_one('span.price-2').text
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    # 당근마켓
    elif Distributor_key in ['daangn']:
        try:
            Lower_price_key = soup.select_one('#article-price').text
        except:
            Lower_price_key = "해당 링크에서 직접 보기"

    # 위메프(js_sele)
    elif Distributor_key in ['wemakeprice']:
        script_re = re.compile('(?<=initialData\'\, JSON\.parse\(\').+')
        script_text1 = script_re.findall(str(soup))
        script_text = str(script_text1[0].strip().replace("'));", "").replace('\\"',"").replace("\\", "").replace("[\t\n\r\f\v]", ""))
        dict_result_script_text = json.loads(script_text)

        try:
            Lower_price_key = dict_result_script_text['prodMain']['sale']['benefitPrice']
        except:
            Lower_price_key = dict_result_script_text['prodMain']['sale']['salePrice']

    # Hosting 주요 3개사 지정

    else:
        try:
            # cafe24
            Lower_price_key = soup.select_one('#span_product_price_text').text
        except:
            try:
                # NHN커머스
                Lower_price_key = soup.select_one(
                    '#frmView > div > div > div.item_detail_list > dl.item_price').text
            except:
                try:
                    # 코리아센터
                    Lower_price_key = soup.select_one('span.price').text
                except:
                    try:
                        Lower_price_key = soup.select_one('.price').text
                    except:
                        try:
                            Lower_price_key = soup.select_one('span.priceArea_price__ombaK active').text
                        except:
                            # 기타
                            Lower_price_key = "해당 링크에서 직접 보기"

    # Lower_price_key 전처리
    print("Lower_price_key 전처리 전 값은? ", Lower_price_key)
    Lower_price_key = str(Lower_price_key).strip()

    Lower_price_key = re.sub(r'([^0-9]*?)', '', Lower_price_key)

    if Lower_price_key == "":
        Lower_price_key = "품절인가봐요!"

    else:
        Lower_price_key = int(Lower_price_key)

    Lower_price.append(Lower_price_key)

    print('Lower_price 리스트 값은, ', Lower_price)

    # 네이버 쇼핑 값일 경우 최저몰도 함께 출력

    if 'naver.com' in User_url and Type == '쇼핑':

        Lower_mall.append(Lower_mall_key)
        print('Lower_mall 리스트 값은, ' , Lower_mall)

    #title pre / post 처리 후 네이버쇼핑 최저가 검색 후 searched 값 도출

    print("Title_key값은 ", Title_key)
# 설명 7번
    # Title 전후처리

    # 전처리

    #패턴 1차: 대,일반 괄호(사이 한글 및 숫자 ,./포함) or |뒷문자(한글 및 숫자 ,./ 포함) 제거
    try:
        Title_pre_key = re.sub(r'\[[가-힣0-9,\. \/]*?\]|\(([가-힣0-9,\. \/]*?)\)|\|([가-힣0-9,\. \/]*?)', '', Title_key)

        print("1차, ", Title_pre_key)
    #패턴 2차: Disrtibutor_Kor 값 제거 

        Title_pre_key = re.sub(Distributor_keyword_list_Kor_dict[Distributor_key],'',Title_pre_key)
        print("2차, ", Title_pre_key)
    #패턴 3차: 필요없는 값 제거 
        trash_words = ['중고거래', '미당첨시', '자동환불', '쇼핑']
        for trash_word in trash_words:
            Title_pre_key = Title_pre_key.replace(trash_word, "")

        Title_pre_key = re.sub('[^\w가-힣 ]','',Title_pre_key)

        print("3차, ", Title_pre_key)

        # regex로 Title_key 다 날릴 경우 대비

        if len(Title_pre_key.strip()) == 0:
            Title_pre_key = Title_key

    except:
        Title_pre_key = Title_key

    print("Title_pre_key는 ", Title_pre_key)

    # 후처리: 제품번호 추출

    #패턴 2차: 영문 및 숫자로 이루어진 최소 6자리 제품번호 추출
    pattern2 = re.compile("[A-Za-z\d/]+[A-Za-z][a-zA-Z\d]{2}[\d]+|[A-Za-z\d/]+[\d][a-zA-Z\d]{2}[A-Za-z][A-Za-z\d/]+") 

    # pattern = re.compile(
    #     '[A-Za-z\d/]+'  # at least one letter or digit or "/"    +
    #     '[A-Za-z]'      # exactly one letter                     +
    #     '\d'            # exactly one digit                      +
    #     '[A-Za-z\d/]+'  # at least one letter or digit or "/"    >= 4 chars
    #     '|'             # OR
    #     '[A-Za-z\d/]+'  # at least one letter or digit or "/"    +
    #     '\d'            # exactly one digit                      +
    #     '[A-Za-z]'      # exactly one letter                     +
    #     '[A-Za-z\d/]+'  # at least one letter or digit or "/"    >= 4 chars
    # )

    try:
        Title_post_key2 = pattern2.findall(Title_pre_key) 

        for Title_post_key1 in Title_post_key2:
            Title_post_key = Title_post_key1

        if Title_pre_key == Title_key:
            Title_chosen_key = Title_post_key
        else:
            if len(Title_pre_key) >= len(Title_post_key):
                Title_chosen_key = Title_post_key
            else:
                Title_chosen_key = Title_pre_key

    except:
        Title_chosen_key = Title_pre_key

    print("Title_chosen_key는, ", Title_chosen_key)
# 설명 8번
    # Title_chosen_key 없을 경우, 탈출
    
    if Title_chosen_key == "해당 링크에서 직접 보기":

        Title_searched_key = "조금 더 찾아봐야해요!"
        Lower_price_searched_key = "조금 더 찾아봐야해요!"
        Lower_mall_searched_key = "조금 더 찾아봐야해요!"
        Lower_url_searched_key = "조금 더 찾아봐야해요!"

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

        #최저가 검색: Title_pre or Title_post 를 활용하여 네이버 쇼핑 1순위(광고 제외) 검색 후 타이틀, 최저가, 최저가몰, URL 추출

        User_url_api = 'https://search.shopping.naver.com/api/search/all?sort=rel&pagingIndex=1&pagingSize=40&viewType=list&productSet=total&deliveryFee=&deliveryTypeValue=&frm=NVSHATC&query=' + str(Title_chosen_key) + '&origQuery=' + str(Title_chosen_key)+ '&iq=&eq=&xq='

        print(User_url_api)
        headers = {'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}

        res_api = requests.get(User_url_api, headers=headers) 

        if res_api.status_code != 200:
            print("User_url_api 접속 오류입니다")

        res_api_json = json.loads(res_api.text)
# 설명 9번
        #meta값
        try:
            Title_searched_key = res_api_json['shoppingResult']['products'][0]['productTitle']
        except:
            Title_searched_key = "조금 더 찾아봐야해요!"
        try:
            Lower_price_searched_key = res_api_json['shoppingResult']['products'][0]['mobileLowPrice'] 
        except:
            Lower_price_searched_key = "조금 더 찾아봐야해요!"
        try:
            Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['lowMallList'][0]['name']
        except:
            try:
                Lower_mall_searched_key = res_api_json['shoppingResult']['products'][0]['mallName']
            except:
                Lower_mall_searched_key = "조금 더 찾아봐야해요!"
        try:
            Lower_url_searched_key = res_api_json['shoppingResult']['products'][0]['crUrl']
        except:
            Lower_url_searched_key = "조금 더 찾아봐야해요!"
        
        print("네이버 쇼핑 최저가는, ", Lower_price_searched_key)

    Title_searched.append(Title_searched_key)

    # Lower_price_searched_key 전처리

    Lower_price_searched_key = str(Lower_price_searched_key).strip()

    Lower_price_searched_key = re.sub(r'([^0-9]*?)', '', Lower_price_searched_key)

    if Lower_price_searched_key == "":

        Lower_price_searched_key = "조금 더 찾아봐야해요!"

    else:        
        Lower_price_searched_key = int(Lower_price_searched_key)   

    # price 비교

    if type(Lower_price_key) and type(Lower_price_searched_key) == int:

        try:
            if Lower_price_key < Lower_price_searched_key:
                Lower_price_searched_key = Lower_price_key
                Lower_mall_searched_key = Distributor_key
                Lower_url_searched_key = User_url
        except:
            print("가격 비교 불가")

    Lower_price_searched.append(Lower_price_searched_key)
    Lower_mall_searched.append(Lower_mall_searched_key)
    Lower_url_searched.append(Lower_url_searched_key)

    print("Title_searched는 ", Title_searched)
    print("Lower_price_searched는 ", Lower_price_searched)
    print("Lower_mall_searched는 ", Lower_mall_searched)
    print("Lower_url_searched는 ", Lower_url_searched)

print("scraping complete")
# 설명 10번

# 라니 오픈
# DB_input

all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched


for list_one in all_list:
    if len(list_one) == 0:
        list_one.append("no_data")

all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall, Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color, Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId)

sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched, UserId, createdAt, updatedAt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())"

cur.execute(sql, all_list_tuple)

db.commit()
print("load complete")

db.close()


# 라니 클로즈 (제이 오픈)

# DB_input

# all_list = Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched

# for list_one in all_list:
#     if len(list_one) == 0:
#         list_one.append("no_data")

# #DB 주의사항: all_list_tuple과 sql의 'INSERT INTO post ( 컬럼 )'의 인자들 순서를 동일하게 설정해야 함 (DB 내 칼럼 순서와 일치하지 않아도 됨)
# #다만, DB의 칼럼과 칼럼 명이 다르거나, DB에 칼럼을 새로 생성한다면, all_list_tuple과 sql에도 해당 인자를 추가해야 함

# all_list_tuple = (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched)

# sql = "INSERT INTO posts (Type, Category_in, Distributor, Publisher, Category_out, Logo_image, Channel_logo, Thumbnail_image, User_url, Title, Maker, Date, Summary, Crawl_content, Emotion_cnt, Comm_cnt, Description, Comment, Tag, View_cnt, Duration, Lower_price, Lower_mall,Lower_price_card, Lower_mall_card, Star_cnt, Review_cnt, Review_content, Dscnt_rate, Origin_price, Dlvry_price, Dlvry_date, Model_no, Color,Location, Title_searched, Lower_price_searched, Lower_mall_searched, Lower_url_searched) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


# cur.execute(sql, all_list_tuple)


# db.commit() 
# print("save complete")

# db.close()

