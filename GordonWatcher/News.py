
class News:
    def __init__(self, title: str = None, summary: str = None, link: str = None, published: str = None) -> None:
        self.title: str
        self.summary: str
        self.link: str
        self.published: str

        if title is not None:
            self.title = title
        if summary is not None:
            self.summary = summary
        if link is not None:
            self.link = link
        if published is not None:
            self.published = published
