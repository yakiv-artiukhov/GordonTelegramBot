import requests
from re import match

class GordonWatcher:
    
    BASE_URL = 'https://gordonua.com/ukr/rsslist.html'
    RSS_LIST_START_PATTERN = '<ul class="rss_list">'
    RSS_LIST_END_PATTERN = '</ul>'
    RSS_UNIT_PATTERN = '<li><a target="_blank" href="'


    def __init__(self, base_url=None) -> None:
        self.subscriber_list = []
        
        if base_url is None:
            self.base_url = self.BASE_URL
        else:
            self.base_url = base_url
            
        self.categories_link_list = self.get_categories_link_list(self.base_url)


    def get_categories_link_list(self, url) -> list:
        request = requests.get(url)
        rss_page_lines = request.text.splitlines()

        for i in range(len(rss_page_lines)):
            if match(self.RSS_LIST_START_PATTERN, rss_page_lines[i]) is not None:
                break
        
        rss_unit_list = []
        for i in range(i, len(rss_page_lines)):
            rss_unit_list.append(rss_page_lines[i])
            if match(self.RSS_LIST_END_PATTERN, rss_page_lines[i]):
                break
        
        rss_links_list = []
        for rss_unit in rss_unit_list:
            result = match(self.RSS_UNIT_PATTERN, rss_unit)
            if result is not None:
                pos = result.span()[1]
                while rss_unit[pos] != '"':
                    pos+=1
                rss_links_list.append(rss_unit[result.span()[1]:pos])
        
        return rss_links_list


    def start_watching(self, tick=None) -> None:
        pass

    def watch_rss_categoty(self, url) -> None:
        pass

g = GordonWatcher()