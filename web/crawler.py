from urllib.error import HTTPError, URLError

import requests
from bs4 import BeautifulSoup, SoupStrainer

from .utils import get_clean_url, is_link_internal, is_url_valid


class Crawler:
    def __init__(self, url, depth_limit=2, nested_limit=3):
        self.crawled_urls = []
        self.data = []
        self.depth = 1
        self.depth_limit = depth_limit
        self.nested_limit = nested_limit
        if is_url_valid(url):
            url = get_clean_url(url, "")

            self.index = 0
            # self.crawl(url)

    def crawl(self, url, nested=0):
        title = ""
        print(nested)
        """
        Crawl over URLs
            - scrape for anchor tags with hrefs in a webpage
            - reject if unwanted or cleanup the obtained links
            - append to a set to remove duplicates
            - "crawled_urls" is the repository for crawled URLs
        @input:
            url: URL to be scraped
        """
        found_urls = []
        if nested < self.depth_limit:
            found_urls_dict = []
        else:
            found_urls_dict = []
        try:
            page = requests.get(url=url, timeout=1)
            content = page.content
            soup = BeautifulSoup(
                content, "lxml", parse_only=SoupStrainer(["a", "title"])
            )
            title = soup.title.text
            for anchor in soup.find_all("a"):
                link = anchor.get("href")
                if is_url_valid(link):
                    # Complete relative URLs
                    link = get_clean_url(url, link)
                    if not is_link_internal(link, url):
                        # print(link)

                        found_urls.append(link)
                else:
                    pass

        except HTTPError as e:
            print("HTTPError:" + str(e.code) + " in ", url)
        except URLError as e:
            print("URLError: " + str(e.reason) + " in ", url)
        except Exception:
            import traceback

            print("Generic exception: " + traceback.format_exc() + " in ", url)

        found_urls = set(found_urls)
        crawl_counter = 0
        if nested < self.depth_limit:
            for crawl_url in found_urls:
                # print(url)
                if crawl_counter < self.nested_limit:
                    nested_crawls = self.crawl(crawl_url, nested=nested + 1)

                    found_urls_dict.append(nested_crawls)
                    crawl_counter += 1
                    print(f"URL {crawl_url} Nested counter = {crawl_counter}")
        else:
            return {"url": url, "title": title, "nested": None}

        return {"url": url, "title": title, "nested": found_urls_dict}
