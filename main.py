import json

from pyquery import PyQuery as pq
# from requests import Session
from requests_html import HTMLSession as Session
from requests.cookies import RequestsCookieJar

import re


def extract_satellite_info(id=5):
    satellite_info = {}
    client = Session()
    jar = RequestsCookieJar()
    jar.set('userinfo', 'lat=0&lng=0&alt=0&tz=UCT&loc=Unspecified&cul=zh')
    client.cookies = jar

    url = f'https://www.heavens-above.com/SatInfo.aspx?satid={id}&lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT'
    response = client.get(url)

    # result = response.html.search('<strong>{title}</strong>{}<table>{table}</table>')

    schema_item = re.compile(r'<strong>(.*?)</strong>.*?<table>(.*?)</table>', re.DOTALL)
    results = schema_item.findall(response.text)
    for title, table in results:
        item = {}
        print(f'item: {title.strip()}')
        schema_table = re.compile(r'<tr>.*?<td.*?>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>', re.DOTALL)
        # schema_td = re.compile(r'<td>.*?</td>', re.DOTALL)

        tds = schema_table.findall(table)
        for key, value in tds:
            key = pq(key).text()
            value = pq(value).text()
            value = value.replace('\n', ' ')

            item[key] = value
            print(f'\tkey={key}\n\tvalue={value}')

        satellite_info[title] = item
    return satellite_info


if __name__ == '__main__':
    satellite_ids = [
        44238,
        44249,
        44252,
        44257,
        44275,
        44279,
        44281,
        44282,
        44287,
    ]
    json_list_path = 'satallite_info.jl'
    with open(json_list_path, 'a+') as file:
        for id in satellite_ids:
            info = extract_satellite_info(id)
            file.write(json.dumps(info) + ',')
