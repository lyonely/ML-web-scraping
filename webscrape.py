import json
from util import get_soup

def create_json(url):
    soup = get_soup(url)
    macros_value = {}
    try:
        nutrition_table = soup.select('table')[0]
        rows = nutrition_table.select('tr')
        for row in rows:
            info = row.select('td')
            if len(info) == 0:
                continue
            macro = str(info[0].findAll(text=True)[0]).strip(' ')
            value = str(info[1].findAll(text=True)[0]).strip(' ')
            macros_value[macro] = value
    except IndexError:
        pass

    json_object = json.dumps({
        "url": url,
        # name, and company
        "tag1": 'table',
        "tag2": 'tr',
        "tag3": 'td',
        "health": macros_value,
    })

    return json_object
