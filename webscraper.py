import json
import re
from util import get_soup


def create_json(url='https://www.waitrose.com/ecom/products/waitrose-indian-butter-chicken-curry/030474-14885-14886'):
    soup = get_soup(url)
    macros_value = {}
    try:
        nutrition_table = soup.select('table')[0]
        rows = nutrition_table.select('tr')[1:]
        for row in rows:
            info = row.contents
            if len(info) == 0:
                continue

            i = 0
            for _ in range(len(info)):
                x = re.match(r"<.*>.*<.*>", str(info[i]).strip(' '))
                if x:
                    break
                i += 1

            macro = str(info[i].contents[0]).strip(' ')
            i += 1
            for _ in range(len(info) - i):
                x = re.match(r"<.*>.*<.*>", str(info[i]).strip(' '))
                if x:
                    break
                i += 1

            value = str(info[i].contents[0]).strip(' ')
            macros_value[macro] = value
    except Exception:
        print("error with: " + url)
        pass

    json_object = json.dumps({
        "url": url,
        # name, and company
        "tag1": 'table',
        "tag2": 'tr',
        "health": macros_value,
    })

    return json_object
