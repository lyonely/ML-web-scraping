import sys
import re
from util import get_soup
from webscrape import create_json

to_crawl = set()
visited = list()
product_links = set()

def get_links(max_links):

    while len(to_crawl) > 0 and len(product_links) < max_links:
        url = to_crawl.pop()
        print(url + " is being searched")
        try:
            soup = get_soup(url)
            page_links = soup.find_all('a')
            for link in page_links:

                save_link = 'https://www.tesco.com' + str(link.get('href'))

                if '/products/' in save_link:
                    product_links.add(save_link)
                    continue

                x = re.findall(r".*page=[0-9]*", save_link)
                if len(x) == 0:
                    continue
                l = x[0]
                if not l in visited:
                    to_crawl.add(l)
                    visited.append(l)

        except:
            pass
    return product_links


def main(url, no_links):
    to_crawl.add(str(url))
    links = get_links(int(no_links))
    for x in links:
        json_obj = create_json(x)
        print(json_obj)


if __name__ == "__main__":
    # python3 crawling.py "https://www.tesco.com/groceries/en-GB/shop/fresh-food/all" 150
    main(sys.argv[1], sys.argv[2])
