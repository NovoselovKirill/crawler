from typing import List


class CrawlerPolicy:
    def __init__(self, allowed_domains: List[str], ignore_robots: bool):
        pass

    def can_fetch(self, url):
        pass


