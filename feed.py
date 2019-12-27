import requests
from xml.dom import minidom
from typing import List, Dict
from pprint import pprint
import unicodedata
import re


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
        rss = self._fetch_rss(url)
        habr_feed = self._parse_rss(rss)
        return habr_feed

    def get_nuancesprog_feed(self) -> List[Dict]:
        url = self.resources["nuancesprog"]
        rss = self._fetch_rss(url)
        nuancesprog_feed = self._parse_rss(rss)
        return nuancesprog_feed

    def get_proglib_feed(self) -> List[Dict]:
        url = self.resources["proglib"]
        rss = self._fetch_rss(url)
        proglib_feed = self._parse_rss(rss)
        return proglib_feed

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
                sub_data = self.normalize(sub_data)
                target_data.append(sub_data)

            news_info[target] = target_data[0] if len(target_data) == 1 else target_data
        return news_info

    def normalize(self, text: str) -> str:
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


if __name__ == "__main__":
    main()
