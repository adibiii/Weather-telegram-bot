import json

import requests
from bs4 import BeautifulSoup

response = requests.get("https://en.wikipedia.org/wiki/Counties_of_Iran")

soup = BeautifulSoup(response.content, "html.parser")

table_tag = soup.find('table', class_='wikitable sortable')
tr_tags = table_tag.find_all('tr')
#
a = tr_tags[1].contents
for i in range(len(a)):
    print(i, a[i].text)
# cities = dict()
# counter = 1
# while counter < 473:
#     a = list(tr_tags[counter].children)
#     province = a[1].text
#     i = int(a[3].text)
#     temp_list = list()
#     temp_list.append(a[5].text)
#     for j in range(1, i):
#         temp_list.append(tr_tags[counter+j].td.text)
#     cities.update({province: temp_list})
#     counter += i
#
# print(cities)
#
# with open('cities.json', 'w') as f:
#     f.write(json.dumps(cities))