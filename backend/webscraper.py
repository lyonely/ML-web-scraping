from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


def get_soup(driver, url):
    """Scrapes the web"""
    try:
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        return soup
    except HTTPError:
        print("Error with: " + url)
    except URLError:
        print("Error with: " + url)

    return None

