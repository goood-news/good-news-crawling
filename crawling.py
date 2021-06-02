 # -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
from numpy.lib.function_base import append
import requests
import pandas as pd
import re

#한글깨짐 방지
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
< naver 뉴스 검색시 리스트 크롤링하는 프로그램 > _select사용
- 크롤링 해오는 것 : 링크,제목,신문사,내용요약본
- 내용요약본  -> 정제 작업 필요
- 리스트 -> 딕셔너리 -> df -> 엑셀로 저장
'''''''''''''''''''''

#각 크롤링 결과 저장하기 위한 리스트 선언

title_text=[] # 제목
title_image=[] # 사진
link_text=[] # 본문 링크
source_text=[] # 신문사
contents_text=[] # 요약
full_content=[] #본문 모든 내용
emotion_recommend=[] #추천해요 숫자
emotion_good=[] # 좋아요 숫자
emotion_touching=[] # 감동이에요 숫자
emotion_angry=[] # 화났어요 숫자
emotion_sad=[] #슬퍼요 숫자
result={}


#엑셀로 저장하기 위한 변수
RESULT_PATH ='D:/news_crawling/'  #결과 저장할 경로
now = datetime.now() #파일이름 현 시간으로 저장하기


# preprocessing function 전처리 함수
def contents_cleansing(contents):
    # 앞에 필요없는 부분 제거
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd> <span>', '',str(contents)).strip()  
    #뒤에 필요없는 부분 제거 (새끼 기사)
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd> </span>', '', first_cleansing_contents).strip()
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    return third_cleansing_contents


def crawler(category):

    categories = {
        '정치': 'politics', 
        '경제': 'economic', 
        '사회': 'society', 
        '세계': 'foreign', 
        'IT': 'digital', 
        '오피니언': 'editorial'
        }
    cat = categories.get(category)

    page = 1 # starting page number
    maxpage_t =1   # fin page number
    
    while page <= maxpage_t:
        
        # BeautifulSoup
        url = f"https://news.daum.net/breakingnews/{cat}?page={page}"
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # strong 태그 중 class 명이 tit_thumb인 것
        atags = soup.find_all('strong', 'tit_thumb')
        
        cnt=0 
        for atag in atags:
            title = atag.a.text
            # strong 태그 중 뉴스 기사 제목 아닌 것들 (15번째 strong 넘어가는 strong 태그) 스크랩 하지 않기 위해 cnt<15
            if(cnt<15):
                title_text.append(title)     #제목
                cur_url = atag.a.get('href') # 뉴스 기사 url
                link_text.append(cur_url)

                ################## full content, 전체 뉴스 페이지에 접근 ##################

                full_response = requests.get(cur_url) 
                full_html = full_response.text
                full_soup = BeautifulSoup(full_html, 'html.parser')

                # 본문 (p 태그 중 dmcf-ptype이 general인 것)
                contents_lists = full_soup.find_all('p','dmcf-ptype'=="general")
                news_full_content=[]
                for contents_list in contents_lists:
                    news_full_content.append(contents_list)
                full_content.append(news_full_content)

                # 본문사진 (img 태그 중 class 명이 thumb_g_article인 것)
                contents_lists = full_soup.find('img',"thumb_g_article")
                if(not contents_lists):
                    title_image.append('')
                else:
                    title_image.append(contents_lists.get('src'))

                ###############################################################################
            else:
                continue
            cnt+=1

        #신문사 (span 태그 중 class 명이 info_news인 것)
        source_lists = soup.find_all('span', 'info_news')
        for source_list in source_lists:
            source_text.append(source_list.text)    #신문사

        #본문요약본 (span 태그 중 class 명이 link_txt인 것)
        contents_lists = soup.find_all('span','link_txt')
        for contents_list in contents_lists:
            contents_cleansing(contents_list) # 전처리

        # make sure all the list's length are same
        # print(len(title_text), len(source_text), len(contents_text), len(link_text), len(title_image), len(full_content))

        #모든 리스트 딕셔너리형태로 저장
        result= {
            "title":title_text ,  
            "source" : source_text ,
            "contents": contents_text ,
            "link":link_text, 
            "image": title_image ,
            "full_contents": full_content ,
            }

        df = pd.DataFrame(result)  #df로 변환
        page += 1

    # 새로 만들 파일이름 지정
    outputFileName = f'daum_result_{cat}.xlsx'
    df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')

#메인함수
def main():
    category = input("카테고리 입력: ") # 예시 : '정치', '경제', '사회', '사회', '세계', 'IT', '오피니언'
    crawler(category)

#메인함수 수행
main()