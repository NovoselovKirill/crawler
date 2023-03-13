import time
from queue import Queue
from threading import Lock
from typing import Callable

import requests

from src.modules.crawler_policy import CrawlerPolicy

LinkFactory = Callable[[str], 'Link']


def link_factory(cname: dict[str, str], crawler_policy: CrawlerPolicy, timeout: int) -> LinkFactory:
    locks = {}
    for domain in set(cname.values()):
        locks[domain] = Lock()

    def create(url: str):
        return Link(url, cname, locks, crawler_policy, timeout)

    return create


class Link:
    __slots__ = ['url', 'domain', '_cname', '_locks', '_crawler_policy', '_timeout']

    _redirects = {}
    _queue = Queue()

    @classmethod
    def resolve_redirects(cls):
        for redirects in cls._queue.get_nowait():
            cls._redirects.update(redirects)

    def __init__(
            self,
            url: str,
            cname: dict[str, str],
            locks: dict[str, Lock],
            crawler_policy: CrawlerPolicy,
            timeout: int):
        url = self._normalize(url)
        if url in Link._redirects:
            url = Link._redirects

        self.url = url
        self.domain = ...
        self._cname = cname
        self._locks = locks
        self._crawler_policy = crawler_policy
        self._timeout = timeout

    def _request(self) -> requests.Response | None:
        try:
            response = requests.get(self.url, timeout=self._timeout)
        except requests.exceptions.RequestException:
            return None

        if response.history:
            response_url = self._normalize(response.url)
            redirects = {self._normalize(resp.url): response_url for resp in response.history}
            Link._queue.put(redirects)
        return response if 200 <= response.status_code < 300 else None

    def _request_with_delay(self, delay: float | int):
        with self._locks[self.domain]:
            res = self._request()
            time.sleep(delay)
        return res

    def go(self):
        if not self._crawler_policy.can_fetch(self):
            return None
        delay = self._crawler_policy.get_delay(self.domain)
        if delay == 0:
            return self._request()
        return self._request_with_delay(delay)

    def _normalize(self, url: str) -> str:
        ...
        return ''

    def __str__(self):
        return self.url
