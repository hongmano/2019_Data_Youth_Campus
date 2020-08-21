# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 22:10:12 2019

@author: Mano
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 21:57:18 2019

@author: Mano
"""

import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import os
import json
import re
import time

 
start = time.time()
os.chdir('C:/Users/Mano/Desktop/co')

start = time.time()

def save(data, file_name):
    file = open(file_name, 'a')
    file.write(data + '\n')

def data_parse(soup, url):

    hangul = re.compile('[^ 가-힣]+')
    titleId = str(parse_qs(urlparse(url).query)['titleId'][0])
    title_1 = rq.get(url)
    title_2 = BeautifulSoup(title_1.content, 'lxml')
    title = title_2.select('.toon_info h4')[0].text.replace(',', '')
    page_count = 1
    object_id = '2019_navercontest_' + str(_ + 1) + '_PRE_ROUND'
    u = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=comic_challenge&templateId=2017_navercontest&pool=cbox3&_callback=jQuery1707844765148129176_1565363485067&lang=ko&country=KR&objectId=' + str(object_id) + '&categoryId=&pageSize=10&indexSize=5&groupId=&listType=OBJECT&pageType=default&page=2&refresh=false&sort=NEW&_=1565363506085'

    while True:
        
        comment_url = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=comic_challenge&templateId=2017_navercontest&pool=cbox3&_callback=jQuery1707844765148129176_1565363485067&lang=ko&country=KR&objectId=' + str(object_id) + '&categoryId=&pageSize=10&indexSize=5&groupId=&listType=OBJECT&pageType=default&page=' + str(page_count) + '&refresh=false&sort=NEW&_=1565363506085'
        header = {

                'Host' : 'apis.naver.com',
                'Referer' : 'https://comic.naver.com/navercontest/2019/comment.nhn?titleId=' + titleId + '&round=PRE_ROUND',
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
                final = str(userid) + ',' + str(usernickname) + ',' + str(comment_time) + ',' + str(title) + ',' + str(page_count) + ',' + str(result) + ',' + str(like) + ',' + str(unlike)
                save(final, 'comment.txt')
                
            if not len(comments):
                break

            else:
                
                page_count += 1

        except:

            page_count += 1
            pass

urls = list()
for _ in range(1, 106):
    urls.append('https://comic.naver.com/navercontest/2019/detail.nhn?titleId='
                + str(_)
                + '&round=PRE_ROUND&sortType=&genreGroup=')
    
    
if __name__ == '__main__':
    for _ in range(len(urls)):
            res = rq.get(urls[_])
            webtoon_page_soup = BeautifulSoup(res.content, 'lxml')
            data_parse(webtoon_page_soup, urls[_])
end = time.time()

print('최강자전 댓글 크롤링에 걸린 시간은 {}분 입니다.'.format(round((end - start) / 60, 1)))
