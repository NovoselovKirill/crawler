from typing import List
from urllib.robotparser import RobotFileParser

from src.modules.links import Link


class CrawlerPolicy:
    __slots__ = ['_domains', '_ignore_disallow', '_ignore_crawl_delay', '_ignore_request_rate', '_robots']

    def __init__(self, cnames: List[str], mode: str):
        self._domains = set(cnames)
        self._ignore_disallow = 'd' in mode or '*' in mode
        self._ignore_crawl_delay = 'c' in mode or '*' in mode
        self._ignore_request_rate = 'r' in mode or '*' in mode
        self._robots = {}
        for domain in self._domains:
            robot = RobotFileParser(domain + '/robots.txt')
            robot.read()
            self._robots[domain] = robot

    def can_fetch(self, link: Link) -> bool:
        if link.domain not in self._domains:
            return False
        if self._ignore_disallow:
            return True
        robot = self._robots[link.domain]
        return robot.can_fetch('*', str(link))

    def _get_crawl_delay(self, domain: str):
        if self._ignore_crawl_delay:
            return 0
        robot = self._robots[domain]
        delay = robot.crawl_delay('*')
        if delay is None:
            return 0
        return int(delay)

    def _get_request_rate(self, domain: str):
        if self._ignore_request_rate:
            return 0
        robot = self._robots[domain]
        request_rate = robot.request_rate('*')
        if request_rate is None:
            return 0
        return request_rate.requests / request_rate.seconds

    def get_delay(self, domain: str):
        return max(self._get_crawl_delay(domain), self._get_request_rate(domain))
