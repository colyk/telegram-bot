import re
import unicodedata
from multiprocessing import Pool
from pprint import pprint
from typing import Dict, List
from xml.dom import minidom

import requests

__all__ = ["Feed"]


class Feed:
    def __init__(self):
        self.TAG_RE = re.compile(r"<[^>]+>")

        self.targets = ["title", "description", "link", "category"]
        self.resources = {
            "habr": "https://habr.com/ru/rss/best/daily",
            "nuancesprog": "https://nuancesprog.ru/feed/",
            "proglib": "https://proglib.io/feed",
        }

    def get_habr_feed(self) -> List[Dict]:
        url = self.resources["habr"]
        return self._get_feed(url)

    def get_nuancesprog_feed(self) -> List[Dict]:
        url = self.resources["nuancesprog"]
        return self._get_feed(url)

    def get_proglib_feed(self) -> List[Dict]:
        url = self.resources["proglib"]
        return self._get_feed(url)

    def get_feeds(self):
        p = Pool(len(self.resources))
        return p.map(self._get_feed, self.resources.values())

    def _get_feed(self, url: str) -> List[Dict]:
        rss = self._fetch_rss(url)
        return self._parse_rss(rss)

    def _fetch_rss(self, url: str) -> str:
        r = requests.get(url)
        r.encoding = "utf-8"
        return r.text

    def _parse_rss(self, rss: str) -> List[Dict]:
        feed = []
        xmldoc = minidom.parseString(rss)
        news_list = xmldoc.getElementsByTagName("item")
        for news in news_list:
            news_info = self._parse_news_info(news)
            feed.append(news_info)
        return feed

    def _parse_news_info(self, news) -> Dict:
        news_info = {}
        for target in self.targets:
            target_elements = news.getElementsByTagName(target)
            target_data = []
            for sub_el in target_elements:
                sub_data = sub_el.firstChild.data.strip()
                sub_data = self._normalize(sub_data)
                target_data.append(sub_data)

            news_info[target] = target_data[0] if len(target_data) == 1 else target_data
        return news_info

    def _normalize(self, text: str) -> str:
        new_text = unicodedata.normalize("NFKD", text)
        return self.TAG_RE.sub("", new_text)


def main():
    feed = Feed()
    habr_feed = feed.get_habr_feed()
    pprint(habr_feed)

    nuancesprog_feed = feed.get_nuancesprog_feed()
    pprint(nuancesprog_feed)

    proglib_feed = feed.get_proglib_feed()
    pprint(proglib_feed)

    feeds = feed.get_feeds()
    pprint(feeds)


if __name__ == "__main__":
    main()
