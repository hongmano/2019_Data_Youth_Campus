# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 22:29:10 2019

@author: Mano
"""

import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import os
import json
import re
import time

os.chdir('C:\\Users\\Mano\\Desktop\\co')

start = time.time()
NAVER_URL = 'http://comic.naver.com'
TOP_URL = 'http://comic.naver.com/webtoon/weekday.nhn'

def make_link(webtoon_url, page_count):
    return webtoon_url + '&page=' + str(page_count)

def save(data, file_name):
    file = open(file_name, 'a')
    file.write(data + '\n')
    
def get_daily_webtoon():
    
    webtoon_main_url = TOP_URL
    res = rq.get(webtoon_main_url)
    main_soup = BeautifulSoup(res.content, 'lxml')
    
    webtoon_links = [{'title' : a_tag.get('title'),
                      'link' : urljoin(NAVER_URL, a_tag.get('href'))}
                        for a_tag in main_soup.select('.daily_all a.title')]
    
    return webtoon_links

def get_all_webtoon(webtoon, is_save):
    
    page_count = 1
    is_unlast = True
    
    target_webtoons = list()
    webtoon_url = webtoon['link']
    webtoon_title = webtoon['title']
    
    while is_unlast:
        
        link = make_link(webtoon_url, page_count)

        target_webtoon_res = rq.get(link)
        webtoon_soup = BeautifulSoup(target_webtoon_res.content, 'lxml')
        a_tags = webtoon_soup.select('.viewList td.title a')
                
        for a_tag in a_tags:
            
            t = a_tag.text.replace('\n', '').replace('\r', '').replace('\t', '')
            h = urljoin(NAVER_URL, a_tag.get('href'))
            
            if h not in target_webtoons:
                target_webtoons.append(h)
            else:
                is_unlast = False
        
        page_count += 1
    
    if is_save:
        for webtoon in target_webtoons:
            save(webtoon_title + ':' + webtoon, 'all_webtoons.txt')
        
    return target_webtoons

def data_parse(soup, url):
    
    hangul = re.compile('[^ ㄱ-ㅣ 가-힣]+')
    titleId = str(parse_qs(urlparse(url).query)['titleId'][0])
    no = str(parse_qs(urlparse(url).query)['no'][0])
    
    objectId = titleId + '_' + no
    
    page_count = 1
    
    u = 'http://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=comic&templateId=webtoon&pool=cbox3&_callback=jQuery1124012459877334097458_1565172327568&lang=ko&country=KR&objectId=' + objectId + '&categoryId=&pageSize=15&indexSize=10&groupId=&listType=OBJECT&sort=NEW&_=1565172327571'
    hangul = re.compile('[^ 가-힣]+')
    title = soup.select('.comicinfo h2')[0].text.split('\r')[0]
    
    while True:
        
        comment_url = make_link(u, page_count)
        
        header = {
                
                'Host' : 'apis.naver.com',
                'Referer' : 'http://comic.naver.com/comment/comment.nhn?titleId=' + titleId + '&no=' + no,
                'Content-Type' : 'application/javascript'
        }
    
        res = rq.get(comment_url, headers = header)
        soup = BeautifulSoup(res.content, 'lxml')
        
        try:
            
            content_text = soup.select('p')[0].text
            one = content_text.find('(') + 1
            two = content_text.find(');')
            content = json.loads(content_text[one:two])
            comments = content['result']['commentList']
            
            for comment in comments:
                
                userid = comment['maskedUserId']
                usernickname = comment['userName']
                comment_time = comment['modTime'][0:10]
                c = comment['contents'].replace('\n', '').replace('\r', '').replace('\t', '')
                like = comment['sympathyCount']
                unlike = comment['antipathyCount']
                result = hangul.sub('', c)
                c = comment['contents'].replace('\n', '').replace('\r', '').replace('\t', '')
                final = str(userid) + ',' + str(usernickname) + ',' + str(comment_time) + ',' + str(title) + ',' + str(no) + ',' + str(page_count) + ',' + str(result) + ',' + str(like) + ',' + str(unlike)
                save(final, 'comment.txt')
                
            
            
            if not len(comments):
                break
            
            else:
                
                page_count += 1
                
        except:
            page_count += 1
            pass
        
if __name__ == '__main__':
    urls = list()
    test = list()
    for_adult = ['닥터 하운드', '살인자o난감 (재)', '피와 살', '헬58', '헬퍼 2 : 킬베로스', '소유', '사냥개들', '살人스타그램', '압락사스', '스퍼맨: 현자단의 역습']         
    webtoons = get_daily_webtoon()
    for _ in range(len(webtoons)):
        if webtoons[_]['title'] not in for_adult:
            test.append(webtoons[_])
            
            
for webtoon in test:
    urls.append(get_all_webtoon(webtoon, False)[::-1][0:5])


for _ in range(len(urls)):
    for __ in range(len(urls[_])):
        res = rq.get(urls[_][__])
        webtoon_page_soup = BeautifulSoup(res.content, 'lxml')
        data_parse(webtoon_page_soup, urls[_][__])
        
end = time.time()

print('웹툰 1~5화 댓글 크롤링에 걸린 시간은 {}분 입니다.'.format(round((end - start) / 60, 0)))
