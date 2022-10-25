import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_soup(url):
    driver = webdriver.Chrome(service=Service('./drivers/chromedriver'))
    try:
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        return soup
    except Exception:
        print("Error occured with: " + url)
    finally:
        driver.quit()
