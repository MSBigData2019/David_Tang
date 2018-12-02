from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import pandas as pd
import re

def offer(parser, offer, data):
    data['offer'].append(offer)
    data['price, km, year'].append([price(parser), km(parser), year(parser)])

def price(parser):
    div = parser.find('div', {'class':'gpfzj'})
    price = str(div.find_next('strong').text)
    regex = re.compile(r"\d+\s+\d+")
    price_bis = re.search(regex, price).group(0)
    price_bis = re.sub(r"\s+", "", price_bis)
    return int(price_bis)

def km(parser):
    desc = parser_annonce.find('ul', {'class' : 'infoGeneraleTxt column2'})
    km = desc.findNext('span').findNext('span').text
    km = re.sub(r"\s+|[a-z]", "", km)
    return int(km)

def year(parser):
    desc = parser_annonce.find('ul', {'class' : 'infoGeneraleTxt column2'})
    return int(desc.findNext('span').text)

def response_request(url):
    response = requests.get(url)
    parser = BeautifulSoup(response.text, 'html.parser')
    return parser
    
url = 'https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&regions=FR-IDF%2CFR-PAC%2CFR-NAQ'
response = requests.get(url)
parser = BeautifulSoup(response.content, features="lxml")
cars = int(parser.find('span', {'class':'numAnn'}).text)
result = {'offer' : [],
                    'price, km, year' : []
                    }
class1=[]
link_list = parser.findAll('a', class_='linkAd ann')
for link in link_list:
    class1.append(link['href'])

url_p1 = 'https://www.lacentrale.fr'
for i in range(len(class1)):
    url_annonce = url_p1 + class1[i]
    parser_annonce = response_request(url_annonce)
    offer(parser_annonce, class1[i], result)

df_result = pd.DataFrame(df['price, km, year'].values.tolist(), columns=['Price', 'Km', 'Year'])
print(df_result)