from News import News

from datetime import datetime
import threading

class NewsRepository():
    # TODO implement RLock to let access news_list to multiple readers at the same time

    def __init__(self, lock: threading.Lock) -> None:
        self.NEWS_LIFETIME = 600

        self.news_list: list[News] = []
        self.lock = lock


    def add_news(self, news_list: list[News]) -> None:
        self.lock.acquire()
        self._remove_expired_news()
        self.news_list = [*self.news_list, *news_list]
        self.lock.release()


    def _remove_expired_news(self) -> None:
        now = datetime.now()
        self.news_list = [item for item in self.news_list if (now - item.timestamp).seconds < self.NEWS_LIFETIME]
             

    def get_untracked_news(self, timestamp: datetime) -> list[News]:
        self.lock.acquire()
        untracked_news = [item for item in self.news_list if item.timestamp > timestamp]
        self.lock.release()

        return untracked_news
