from typing import List

from src.modules.crawler_policy import CrawlerPolicy
from atomicwrites import atomic_write


class Crawler:
    def __init__(self, start_urls: List[str], crawler_policy: CrawlerPolicy):
        pass
