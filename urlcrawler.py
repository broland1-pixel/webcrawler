import os
import re

import requests
import urllib.parse

from bs4 import BeautifulSoup

url_to_do = set()
url_collected = set()
given_url = None


def start_spider(url):
    url_to_do.add(url)

    spider_go()


def spider_go():

    while url_to_do.__len__() > 0:
        url = url_to_do.pop()

        if url in url_collected:
            continue

        if url.find(".flac") is not -1 or url.find(".png") is not -1 or url.find(".jpg") is not -1 or url.find(".pdf") is not -1 or url.find(".txt") is not -1 or url.find("xml") is not -1:
            url_collected.add(url)
            continue

        print("Collecting: " + url)
        site = requests.get(url=url)

        soup = BeautifulSoup(site.content, "html.parser")

        for link in soup.find_all("a"):
            href = link.attrs.get("href")
            if href is None or "" or href.find("jquery") is not -1:
                continue

            # Join the relative links
            if href.find("http") is not -1 or href.find("https:") is not -1:
                href = href.split("#", 1)[0]  # Removes parts of the url
            elif href.find(given_url) is not -1:
                href = href.split("#", 1)[0]  # Removes parts of the url
            else:
                href = urllib.parse.urljoin(url, href)
                href = href.split("#", 1)[0]  # Removes parts of the url

            if href.find(given_url) is not -1 and url not in url_collected:
                url_to_do.add(href)

        url_collected.add(url)


def start_scraper():
    print("scraper")

    url_set = {}
    default_value = 0
    urls_done = 0

    for url in url_collected:
        urls_done = urls_done + 1

        print(url)
        if url.find(".flac") is not -1 or url.find(".png") is not -1 or url.find(".jpg") is not -1 or url.find(".pdf") is not -1 or url.find(".txt") is not -1 or url.find("xml") is not -1:
            url_set[url] = url_set.get(url, default_value) + 1
            continue

        data = requests.get(url=url)

        soup = BeautifulSoup(data.content, "html.parser")  # Uses html.parser because that is the default
        for link in soup.find_all("a"):
            href = link.attrs.get("href")
            if href is None or "" or href.find("jquery") is not -1:
                continue

            # Join the relative links
            if href.find("http") is not -1 or href.find("https:") is not -1:
                href = href.split("#", 1)[0]  # Removes parts of the url
                url_set[href] = url_set.get(href, default_value) + 1
            elif href.find(given_url) is not -1:
                href = href.split("#", 1)[0]  # Removes parts of the url
                url_set[href] = url_set.get(href, default_value) + 1
            else:
                href = urllib.parse.urljoin(url, href)

                href = href.split("#", 1)[0]  # Removes parts of the url
                url_set[href] = url_set.get(href, default_value) + 1

    with open("report.txt", "w") as output:
        for key, value in url_set.items():
            output.write(key + "," + str(value) + ",\n")  # os.linesep)

    print("done")
    print(url_collected.__len__())
    print(urls_done)


if __name__ == '__main__':
    given_url = "http://books.toscrape.com/"
    start_spider(url=given_url)
    start_scraper()
