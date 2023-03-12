from typing import List


class CrawlerPolicy:
    def __init__(self, allowed_domains: List[str], mode: str):
        pass

    def can_fetch(self, normalized_url) -> bool:
        pass

