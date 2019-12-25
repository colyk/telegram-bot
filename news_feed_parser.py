import requests
from xml.dom import minidom
from typing import List
from pprint import pprint

import re

TAG_RE = re.compile(r"<[^>]+>")


def remove_tags(text):
    return TAG_RE.sub("", text)


def parse_habr() -> List[dict]:
    url = "https://habr.com/ru/rss/best/daily/?fl=ru"
    r = requests.get(url)
    xmldoc = minidom.parseString(r.text)
    news_list = xmldoc.getElementsByTagName("item")

    habr_feed = []
    targets = ["title", "description", "link", "category"]
    for news in news_list:
        target_info = {}
        for target in targets:
            target_elements = news.getElementsByTagName(target)
            target_data = []
            for sub_el in target_elements:
                sub_data = sub_el.firstChild.data.strip()
                sub_data = remove_tags(sub_data)
                target_data.append(sub_data)

            target_info[target] = (
                target_data[0] if len(target_data) == 1 else target_data
            )
        habr_feed.append(target_info)

    return habr_feed


def main():
    habr_feed = parse_habr()
    pprint(habr_feed)


if __name__ == "__main__":
    main()
