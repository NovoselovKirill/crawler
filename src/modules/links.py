from queue import Queue
from typing import Callable, NamedTuple

import requests

from src.modules.crawler_policy import CrawlerPolicy

LinkFactory = Callable[[str], 'Link']


def link_factory(cname: dict[str, str], crawler_policy: CrawlerPolicy, timeout: int) -> LinkFactory:
    def create(url: str):
        return Link(url, cname, crawler_policy, timeout)

    return create


class Link:
    __slots__ = ['url', '_cname', '_crawler_policy', '_timeout']

    _redirects = {}
    _queue = Queue()

    @classmethod
    def resolve_redirects(cls):
        for redirects in cls._queue.get_nowait():
            cls._redirects.update(redirects)

    def __init__(self, url: str, cname: dict[str, str], crawler_policy: CrawlerPolicy, timeout: int):
        url = self._normalize(url)
        if url in Link._redirects:
            url = Link._redirects

        self.url = url
        self._cname = cname
        self._crawler_policy = crawler_policy
        self._timeout = timeout

    def go(self):
        try:
            response = requests.get(self.url, timeout=self._timeout)
        except requests.exceptions.RequestException:
            return None

        if response.history:
            response_url = self._normalize(response.url)
            redirects = {self._normalize(resp): response_url for resp in response.history}
            Link._queue.put(redirects)
        return response.content if 200 <= response.status_code < 300 else None

    def _normalize(self, url) -> str:
        ...
        return ''

    def __str__(self):
        return self.url
