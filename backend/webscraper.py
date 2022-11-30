from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

from backend.timer import timed

@timed
def soup(driver, url):
    """Scrapes the web"""
    try:
        driver.get(url)
        page = driver.page_source
        return BeautifulSoup(page, 'html.parser')
    except HTTPError:
        print("Error with: " + url)
    except URLError:
        print("Error with: " + url)

    return None


def soup_without_driver(html: str):
    """ Uses frontend to scrape """
    return BeautifulSoup(html, 'html.parser')
