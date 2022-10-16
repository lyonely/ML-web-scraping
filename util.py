from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_soup(url):
    try:
        driver = webdriver.Chrome(service=Service('./drivers/chromedriver'))
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        driver.quit()
        return soup
    except Exception:
        print("Error occured with: " + url)