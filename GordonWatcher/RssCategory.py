from News import News
from hashlib import sha224
from feedparser import parse
from requests import get


class RssCategory:
    def __init__(self, url: str) -> None:

        self.url = url
        self.latest_hash: str
        self.latest_news: News

        self.latest_hash = sha224(get(self.url).text.encode('utf-8')).hexdigest()
        self.latest_news = self.get_latest_news()

        self.untracked_news: list(News)


    def get_latest_news(self):
        news = parse(self.url).entries
        if len(news) > 0:
            self.latest_news = News(news[0].get('title'), news[0].get('summary'), news[0].get('link'), news[0].get('published'))


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



    def find_untracked_news(self) -> list:
        news = parse(self.url).entries
        untracked_news = []
        for i in range(len(news)):
            if news[i].get('published') == self.latest_news.published:
                break
            else:
                untracked_news.append(News(news[i].get('title'), news[i].get('summary'), news[i].get('link'), news[i].get('published')))
        return untracked_news