from datetime import datetime
from feedparser.util import FeedParserDict

class News:
    def __init__(self, title: str = None, summary: str = None, link: str = None, 
    published: str = None, timestamp: datetime = None) -> None:
        
        self.title: str
        self.summary: str
        self.link: str
        self.published: str
        self.timestamp: datetime

        self.title = title
        self.summary = summary
        self.link = link
        self.published = published
        self.timestamp = timestamp


    def _compare_news_and_entry(self, entry) -> bool:
        pass


    @staticmethod
    def feedparser_entry_to_news(entry: FeedParserDict, timestamp: datetime):
        if not (entry.has_key('title') and entry.has_key('summary') and entry.has_key('link') and entry.has_key('published')):
            return None
        return News(entry.get('title'), entry.get('summary'), entry.get('link'), entry.get('published'), timestamp)


    def _to_string(self) -> str:
        return f'Title: {self.title}, Summary: {self.summary}, Link: {self.link}, Published: {self.published}, Timestamp: {self.timestamp}'


    def _to_message_string(self) -> str:
        return f'Title: {self.title} \n\nSummary: {self.summary} \n\nLink: {self.link} \n\nPublished: {self.published}'