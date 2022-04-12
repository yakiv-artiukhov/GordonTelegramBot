from turtle import speed
from RssCategory import RssCategory

from time import sleep
from requests import get
from re import search
from datetime import datetime

class GordonWatcher:
    
    BASE_URL = 'https://gordonua.com/ukr/rsslist.html'
    RSS_LIST_START_PATTERN = '<ul class="rss_list">'
    RSS_LIST_END_PATTERN = '</ul>'
    RSS_UNIT_PATTERN = '<li><a target="_blank" href="'


    def __init__(self, base_url: str = None) -> None:
        self.subscriber_list = []
        
        if base_url is None:
            self.base_url = self.BASE_URL
        else:
            self.base_url = base_url
            
        self.rss_categories: list = self.get_rss_categories(self.base_url)


    def get_rss_categories(self, url) -> list:
        response = get(url)
        page_lines = response.text.splitlines()
        page_lines_amount = len(page_lines)
        rss_unit_list = []

        for i in range(page_lines_amount):
            if search(self.RSS_LIST_START_PATTERN, page_lines[i]) is not None:
                break

        for i in range(i, page_lines_amount):
            rss_unit_list.append(page_lines[i])
            if search(self.RSS_LIST_END_PATTERN, page_lines[i]):
                break
        
        rss_links_list = []
        for rss_unit in rss_unit_list:
            result = search(self.RSS_UNIT_PATTERN, rss_unit)
            if result is not None:
                pos = result.span()[1]
                while rss_unit[pos] != '"':
                    pos+=1
                rss_links_list.append(RssCategory(url=rss_unit[result.span()[1]:pos]))
        
        return rss_links_list


    def start_watching(self, tick=None) -> None:
        for category in self.rss_categories[1:len(self.rss_categories)]:
            self.watch_rss_categoty(category)


    def watch_rss_categoty(self, rss_category: RssCategory) -> None:
        print(datetime.now(), rss_category.url, 'Start tracking')
        i = 1
        while(True):
            print(datetime.now(), i, 'iteration', end='____ ')
            if rss_category.is_there_new_news(): 
                news = rss_category.untracked_news
                print(rss_category.url, news)
            else:
                print(rss_category.url, 'No updates')
            sleep(60)
            i += 1
        

g = GordonWatcher()
# for c in g.rss_categories:
#     print(c.url)
g.start_watching()

