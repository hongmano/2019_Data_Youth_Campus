from __future__ import unicode_literals
from urllib.parse import urlparse, parse_qs, urljoin
import requests as rq
import os
from bs4 import BeautifulSoup
import re

# Change Working Directory

os.chdir('your path')

# Crawler

def crawl_naver_webtoon(episode_url):
    
    # Html address
    html = rq.get(episode_url).text
    
    # Parsing
    soup = BeautifulSoup(html, 'html.parser')
    
    # remove :, ? to make file names
    comic_title = ' '.join(soup.select('.comicinfo h2')[0].text.split()).replace('\r', '').replace('\t', '')
    comic_title = re.sub('[\/:*?"<>|.]', '', comic_title)
    ep_title = ' '.join(soup.select('.tit_area h3')[0].text.split())
    ep_title = re.sub('[\/:*?"<>|.]', '', ep_title)
    
    for img_tag in soup.select('.wt_viewer img'):
        
        # Select image`s address
        image_file_url = img_tag['src']
        # Seting image file`s path - 1
        image_dir_path = os.path.join(os.path.dirname('__file__'), comic_title, ep_title)
        # setting image file`s path - 2
        image_file_path = os.path.join(image_dir_path, os.path.basename(image_file_url))
        
        # Saving image files
        if not os.path.exists(image_dir_path):
            os.makedirs(image_dir_path)
        
        headers = {'Referer' : episode_url}
        image_file_data = rq.get(image_file_url, headers = headers).content
        
        open(image_file_path, 'wb').write(image_file_data)
    
    print('웹툰 이미지 수집이 완료되었습니다!')

def save(data, file_name):
    file = open(file_name, 'a')
    file.write(data + '\n')
    
def make_link(webtoon_url, page_count):
    return webtoon_url + '&page=' + str(page_count)

def get_daily_webtoon():
    
    TOP_URL = 'http://comic.naver.com/webtoon/weekday.nhn'
    NAVER_URL = 'http://comic.naver.com'
    webtoon_main_url = TOP_URL
    res = rq.get(webtoon_main_url)
    main_soup = BeautifulSoup(res.content, 'lxml')
    
    webtoon_links = [{'title' : a_tag.get('title'),
                      'link' : urljoin(NAVER_URL, a_tag.get('href'))} 
                        for a_tag in main_soup.select('.daily_all a.title')]
    
    return webtoon_links

def get_all_webtoon(webtoon, is_save):

    TOP_URL = 'http://comic.naver.com/webtoon/weekday.nhn'
    NAVER_URL = 'http://comic.naver.com'
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
            t = re.sub('[\/:*?"<>|.]', '', t)
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

def star_point(url):
    
    for _ in range(len(url)):
        
        for __ in range(len(url[_])):
            
            res = rq.get(url[_][__])
            webtoon_page_soup = BeautifulSoup(res.content, 'lxml')
            starpoint = webtoon_page_soup.select('#topPointTotalNumber')[0].text
            titleId = str(parse_qs(urlparse(url[_][__]).query)['titleId'][0])
            no = str(parse_qs(urlparse(url[_][__]).query)['no'][0])
            
            save(titleId + ':' + no + ':' + starpoint, 'starpoint.txt')
            
# Crawling

# Collecting urls(Latent 10 webtoons for each, excepting adult webtoons)

if __name__ == '__main__':
    urls = list()
    test = list()
    for_adult = ['닥터 하운드', '살인자o난감 (재)', '피와 살', '헬58', '헬퍼 2 : 킬베로스', '소유', '사냥개들', '살人스타그램', '압락사스', '스퍼맨: 현자단의 역습']         
    webtoons = get_daily_webtoon()
    for _ in range(len(webtoons)):
        if webtoons[_]['title'] not in for_adult:
            test.append(webtoons[_])
    for webtoon in test:
        urls.append(get_all_webtoon(webtoon, False)[0:5])
        
# Let`s Crawl Image !!!

if __name__ == '__main__':
    for _ in range(len(urls)):
        episode_url = urls[_]
        for __ in range(len(urls[_])):
            crawl_naver_webtoon(episode_url[__])

# Let`s Crawl Starpoints !!!


star_point(urls)
            
