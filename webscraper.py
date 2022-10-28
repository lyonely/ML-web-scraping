from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_soup(url):
    """Scrapes the web"""
    driver = webdriver.Chrome(service=Service('./drivers/chromedriver'))
    try:
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        return soup
    except HTTPError:
        print("Error with: " + url)
    except URLError:
        print("Error with: " + url)
    finally:
        driver.quit()

    return None
