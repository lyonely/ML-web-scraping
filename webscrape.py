from selenium import webdriver
import json
from bs4 import BeautifulSoup

driver = webdriver.Chrome('./chromedriver')

url = "https://www.tesco.com/groceries/en-GB/products/289623609"
driver.get(url)
page = driver.page_source
soup = BeautifulSoup(page, 'lxml')

nutrition_table = soup.select('table')[0]

rows = nutrition_table.select('tr')
macros_value = {}
for row in rows:
    info = row.select('td')
    if len(info) == 0:
        continue
    macro = str(info[0].findAll(text=True)[0]).strip(' ')
    value = str(info[1].findAll(text=True)[0]).strip(' ')
    macros_value[macro] = value

nutrition_json = json.dumps(macros_value, indent=4)

json_object = json.dumps({
    "url": url,
    "tag1": 'table',
    "tag2": 'tr',
    "tag3": 'td',
    "health": macros_value,
})

query = json.loads(json_object)

print(query["health"]["Energy"])

driver.quit()

