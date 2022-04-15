
from RssCategory import RssCategory
from GordonBot import GordonBot
from NewsRepository import NewsRepository

from time import sleep
from datetime import datetime

from requests import get
from re import search
import threading
import asyncio


class GordonWatcher:

    BASE_URL = 'https://gordonua.com/ukr/rsslist.html'
    RSS_LIST_START_PATTERN = '<ul class="rss_list">'
    RSS_LIST_END_PATTERN = '</ul>'
    RSS_UNIT_PATTERN = '<li><a target="_blank" href="'

    TICK = 60

    LOG_FILE_NAME = 'C:/Users/yakiv.artiukhov/source/university/Work Practice/GordonTelegramBot/log.txt'

#news_repository: NewsRepository, 
    def __init__(self, news_repository: NewsRepository, base_url: str = None, log_file_name: str = None) -> None:
        self.base_url: str
        self.log_file_name: str

        self.news_repository: NewsRepository = news_repository

        if base_url is None:
            self.base_url = self.BASE_URL
        else:
            self.base_url = base_url
            
        self.rss_categories: list[RssCategory] = self.get_rss_categories(self.base_url)

        if log_file_name is None:
            self.log_file_name = self.LOG_FILE_NAME
        else:
            self.log_file_name = log_file_name


    def get_rss_categories(self, url) -> list[RssCategory]:
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


    def start_watching(self, tick: int = None) -> None:
        if tick is not None:
            self.tick = tick
        thread = threading.Thread(target=self.__start_watching, args=())
        #thread.daemon = True
        thread.start()
    def __start_watching(self) -> None:
        while True:
            for category in self.rss_categories:
                self.watch_rss_categoty(category)
            sleep(60)


    def watch_rss_categoty(self, rss_category: RssCategory) -> None:
        self.log(f'\n$ Time: {datetime.now()} | Category: {rss_category.url} | ')        
        
        if rss_category.is_there_new_news(): 
            self.news_repository.add_news(rss_category.untracked_news)
            for entry in rss_category.untracked_news:
                self.log(f'\n    {entry._to_string()}')
            self.log(f'\n')
        else:
            self.log(f'Updates: None\n')

    
    def log(self, message: str) -> None:
        print(message)
        with open(self.log_file_name, 'a', encoding="utf-8") as log_file:
            log_file.write(message)
