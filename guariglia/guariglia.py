import math

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

import utils

url = "https://www.guariglialeiloes.com.br/"

response = requests.get(url)
if response.status_code == 200:
    html = response.text
    soup = bs(html, "lxml")
    tables = soup.find_all('div', {'class': 'card-body d-flex flex-column'})
    links = []
    for item in tables:
        link = {'link': item.find('a')['href']}
        if item.find('div', {'class': 'label_leilao rounded ativo'}):
            link['status'] = item.find('div', {'class': 'label_leilao rounded ativo'}).text
            aux = item.find_all('div', text=lambda text: text and 'Lotes' in text)
            link['auctions'] = int(aux[0].text[:3])
        links.append(link)

    main_link = []
    for link in links:
        try:
            if link['status']:
                main_link.append(link)
        except KeyError:
            pass
    pages = math.ceil(main_link[0]['auctions'] / 30)
    page_link = main_link[0]['link'] + "?page="

    items = []

    for page in range(1, pages):
        response = requests.get(page_link+str(page))
        html = response.text
        soup = bs(html, "lxml")
        lots = soup.find_all('div', {'class': 'lote rounded'})
        items = utils.build_item(items, lots)

    utils.save_csv(items)
