from __future__ import unicode_literals
import os
import requests
from bs4 import BeautifulSoup

# Change Working Directory

os.chdir('your path')

# Crawler

def crawl_naver_webtoon(episode_url):
    
    # Html address
    html = requests.get(episode_url).text
    # Parsing
    soup = BeautifulSoup(html, 'html.parser')
    # remove :, ? to make file names
    comic_title = ' '.join(soup.select('.toon_info h4')[0].text.split()).replace(':', '').replace('?', '')
    
    for img_tag in soup.select('.img_sc img'):
        
        # Select image`s address
        image_file_url = img_tag['src']
        # Seting image file`s path - 1
        image_dir_path = os.path.join(os.path.dirname('__file__'), comic_title)
        # setting image file`s path - 2
        image_file_path = os.path.join(image_dir_path, os.path.basename(image_file_url))
        
        # Saving image files
        if not os.path.exists(image_dir_path):
            os.makedirs(image_dir_path)
        
        headers = {'Referer' : episode_url}
        image_file_data = requests.get(image_file_url, headers = headers).content
        
        open(image_file_path, 'wb').write(image_file_data)
    
    print('웹툰 이미지 수집이 완료되었습니다!')
    
# Crawling

# Collecting urls
    
urls = list()
for _ in range(1, 106):
    urls.append('https://comic.naver.com/navercontest/2019/detail.nhn?titleId='
                + str(_)
                + '&round=PRE_ROUND&sortType=&genreGroup=')

# Let`s Crawl !!!
    
if __name__ == '__main__':
    for _ in range(len(urls)):
        episode_url = urls[_]
        crawl_naver_webtoon(episode_url)
