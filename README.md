# good-news-crawling

다음 뉴스 크롤링 코드. pip package 로 만들 예정!
실행하면 바로 AWS Mysql Server로 이동. (엔드포인트, 포트는 직접 입력해야함)

### Requirements
- chromedriver.exe (make complicence with local OS)
- set mySQL information in local env.py file at root

### Run
$ python crawling.py --category society
arguments: 
- category: society: 사회, economy: 경제, IT: 과학기술, foreign: 세계뉴스, opinion: 사설  (default '사회')
- time: 20210604 (default current)
- save_xml: True: MySQL Server와 xml 파일로 저장, False: MySQL로만 저장. 

### Test
Install: $ pip install pytest
Run: $ pytest test.py

### 저장되는 내용
- title
- source: 언론사, 시간
- contents: 요약 (1줄 정도)
- link: 해당 뉴스 링크
- image: 기사 이미지 없는 경우 빈칸
- full_contents: 기사 전문
- likes: 긍정적인 피드백 수(추천해요, 좋아요, 감동이에요)
- dislikes: 부정적인 피드백 수(화나요, 슬퍼요)

### 사용 기술
- Selenium
- bs4
- python
- MySQL (AWS RDS)
$ python crawling.py

### Test
$ python test.py
