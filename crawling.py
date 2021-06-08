 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
from numpy.lib.function_base import append
import requests
import pandas as pd
import re
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# 한글깨짐 방지
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from env import conn

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
< naver 뉴스 검색시 리스트 크롤링하는 프로그램 > _select사용
- 크롤링 해오는 것 : 링크,제목,신문사,내용요약본
- 내용요약본  -> 정제 작업 필요
- 리스트 -> 딕셔너리 -> df -> 엑셀로 저장
'''''''''''''''''''''




# 엑셀로 저장하기 위한 변수
RESULT_PATH ='D:/news_crawling/'  #결과 저장할 경로
now = datetime.now() #파일이름 현 시간으로 저장하기

curs = conn.cursor()


def crawler(category, newsdate, start_page, end_page):

    # 각 크롤링 결과 저장하기 위한 리스트 선언
    category_list=[] # 카테고리
    page_list=[] # 크롤링하는 페이지 번호
    title_text=[] # 제목
    title_image=[] # 사진
    link_text=[] # 본문 링크
    source_text=[] # 신문사
    date_list=[] # publishedAt
    contents_text=[] # 요약
    full_content=[] # 본문 모든 내용
    likes=[] # 좋아요 숫자
    dislikes=[] # 감동이에요 숫자
    label=[] # 긍부정 평가 
    result={}

    categories = {
        '정치': 'politics', 
        '경제': 'economic', 
        '사회': 'society', 
        '세계': 'foreign', 
        'IT': 'digital', 
        '오피니언': 'editorial'
        }
    cat = categories.get(category)

    # start_page = 1 # start page number
    # end_page = 20   # finish page number
    start_page = int(start_page)
    end_page = int(end_page)

    while start_page < end_page:
        # BeautifulSoup
        url = f"https://news.daum.net/breakingnews/{cat}?page={start_page}&regDate={newsdate}"
        try:
            response = requests.get(url)
            html = response.content.decode('utf-8','replace').encode('utf-8','replace')
            soup = BeautifulSoup(html, 'html.parser')

            # strong 태그 중 class 명이 tit_thumb인 것
            atags = soup.find_all('strong', 'tit_thumb')

            cnt=0 
            for atag in atags:
                title = atag.a.text
                # strong 태그 중 뉴스 기사 제목 아닌 것들 (15번째 strong 넘어가는 strong 태그) 스크랩 하지 않기 위해 cnt<15
                if(cnt<15):

                    # insert current page number (한 페이지에 15개 이하인 issue solve)
                    page_list.append(start_page)

                    title = title.replace("'", '"')
                    title_text.append(title)     #제목
                    cur_url = atag.a.get('href') # 뉴스 기사 url
                    cur_url_txt = cur_url.replace("'", '"')
                    link_text.append(cur_url_txt)

                    ################## full content, 전체 뉴스 페이지에 접근 ##################
                    full_response = requests.get(cur_url) 
                    full_html = full_response.text
                    full_soup = BeautifulSoup(full_html, 'html.parser')

                    # 본문 (p 태그 중 dmcf-ptype이 general인 것)
                    contents_lists = full_soup.select('#harmonyContainer > section > p')
                    full_content_string=''
                    for contents_list in contents_lists:
                        if full_content_string != '':
                            full_content_string += '  '
                        contents_list = contents_list.text
                        full_content_string+=str(contents_list)
                    full_content_string = full_content_string.replace("'", '"')
                    # print("full content: ", full_content_string)
                    full_content.append(full_content_string)
                    contents_text.append(full_content_string[:120])

                    # 본문사진 (img 태그 중 class 명이 thumb_g_article인 것)
                    contents_lists = full_soup.find('img',"thumb_g_article")
                    if(not contents_lists):
                        title_image.append('')
                    else:
                        title_image.append(contents_lists.get('src'))

                    tmp_source_str = ""
                    publisher_list = full_soup.find_all('img', 'thumb_g')
                    publisher = publisher_list[1].get('alt')
                    reporter = full_soup.find('span', 'txt_info')
                    num_date = full_soup.find('span', 'num_date')

                    tmp_source_str += str(num_date.text)
                    tmp_source_str += str(reporter.text)
                    tmp_source_str += str(publisher)
                    source_text.append(tmp_source_str)
                    # print(tmp_source_str)
                    ###############################################################################
                else:
                    continue
                cnt+=1

            # # 신문사 (span 태그 중 class 명이 info_news인 것)
            # source_lists = soup.find_all('span', 'info_news')
            # if(source_lists==None):
            #         source_text.append('')
            # else:
            #     for source_list in source_lists:
            #         src_list = source_list.text
            #         src_list = src_list.replace("'", '"')
            #         source_text.append(src_list)    #신문사

            # 본문 요약본 (span 태그 중 class 명이 link_txt인 것)
            # contents_lists = soup.select('div.box_etc div.desc_thumb > span.link_txt')
            # # contents_lists = soup.find_all('span','link_txt')
            # if(contents_lists==None):
            #     source_text.append('')
            # else:
            #     for contents_list in contents_lists:
            #         contents_list = contents_list.text
            #         contents_list = str(contents_list).replace("'", '"')
            #         contents_list = contents_list.replace('\n', '').strip()
            #         contents_text.append(contents_list)

        
        except requests.exceptions.ConnectionError:
            continue

        start_page += 1

    # 카테고리
    category_list = [cat] * len(title_text)
    date_list = [newsdate] * len(title_text)

    # emotions
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    # options.add_argument('--no-sandbox')
    browser = webdriver.Chrome("./chromedriver", options=options)
    sleep(3)
    for link in link_text:
        browser.get(link)

        wait = WebDriverWait(browser, 10)
        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "selectionbox.type-RECOMMEND.unselected")))

        good_emotion = 0
        bad_emotion = 0
        count_elems = browser.find_elements_by_class_name('count')
        if(len(count_elems)==5):
            for i in range(0,3):
                elem = count_elems[i].text
                if(elem.isdigit()):
                    good_emotion = good_emotion+int(count_elems[i].text)
            for i in range(3,5):
                elem = count_elems[i].text
                if(elem.isdigit()):
                    bad_emotion = bad_emotion+int(count_elems[i].text)
        
        likes.append(good_emotion) # 전처리
        dislikes.append(bad_emotion) # 전처리

        if(good_emotion>bad_emotion):
            label.append(1) # 긍정
        else:
            label.append(0) # 부정
    browser.quit()

    # 모든 리스트의 길이가 같아야하므로 길이를 확인한다.
    print(len(category_list), len(page_list), len(title_text), len(title_image), len(link_text), len(source_text), len(date_list),len(contents_text),  len(full_content), len(likes), len(dislikes), len(label))

    # 모든 리스트 딕셔너리형태로 저장
    result= {
        "title":title_text ,
        "category": category_list,
        "source" : source_text ,
        "date": date_list,
        "contents": contents_text ,
        "link":link_text, 
        "image": title_image ,
        "full_contents": full_content ,
        "likes": likes,
        "dislikes": dislikes,
        "label": label
        }
    df = pd.DataFrame(result)  #df로 변환

    # 새로 만들 파일이름 지정
    outputFileName = f'daum_result_{cat}.xlsx'
    df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')

    # TITLE, SOURCE, CONTENTS, LINK, IMAGE, FULL_CONTENTS, LIKES, DISLIKES, LABEL
    # sql = "INSERT into CRAWLING(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for i in range(len(title_text)):
        sql_query = f"INSERT INTO CRAWLING2 VALUES('{category_list[i]}','{page_list[i]}','{title_text[i]}','{source_text[i]}','{date_list[i]}','{contents_text[i]}','{link_text[i]}','{title_image[i]}','{full_content[i]}','{likes[i]}','{dislikes[i]}','{label[i]}')"
        curs.execute(sql_query)
        conn.commit()


# 메인함수
def main():
    category = input("카테고리 입력: ") # 예시 : '경제', '사회', '세계','정치', '오피니언', 'IT' 
    newsdate = input("검색할 날짜 입력: 예)20210601 ")
    start_page = input("검색할 시작 페이지: ")
    end_pages = input("검색할 끝 페이지: ")
    # time = input("검색시간 입력")
    crawler(category, newsdate, start_page, end_pages)

# 메인함수 수행
main()