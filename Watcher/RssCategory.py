from News import News

from datetime import date, datetime

from hashlib import sha224
from feedparser import parse
from requests import get


class RssCategory:
    def __init__(self, url: str) -> None:

        self.url: str = url
        self.latest_hash: str
        self.latest_news: News

        self.latest_hash = sha224(get(self.url).text.encode('utf-8')).hexdigest()
        self.latest_news = self.get_latest_news()

        self.untracked_news: list[News] = None


    def get_latest_news(self) -> News:
        news = parse(self.url).entries
        if len(news) > 0:
            return News.feedparser_entry_to_news(news[0], datetime.now())


    def is_there_new_news(self) -> bool:
        current_hash = sha224(get(self.url).text.encode('utf-8')).hexdigest()
        if self.latest_hash == current_hash:
            return False
        else:
            self.latest_hash = current_hash
            self.untracked_news = self.find_untracked_news()
            if len(self.untracked_news) > 0:
                self.latest_news = self.untracked_news[0]
                return True
            return False


    def find_untracked_news(self) -> list[News]:
        news = parse(self.url).entries
        untracked_news = []
        for i in range(len(news)):
            if news[i].get('published') == self.latest_news.published:
                break
            else:
                untracked_news.append(News.feedparser_entry_to_news(news[i], datetime.now()))
        return untracked_news