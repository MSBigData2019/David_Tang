# Ordinateurs portables Acers & Dell, qui a le plus de promo?
import requests
from bs4 import BeautifulSoup

# ACER    
page = requests.get('https://www.darty.com/nav/recherche?p=200&s=relevence&text=acer&fa=756')
soup = BeautifulSoup(page.content, 'html.parser')
div = soup.find_all('div', {'class' : 'page-main clearfix'})
p = div[0].find_all('p', {'class':'darty_prix_barre_remise darty_small separator_top'})
print('nombre de pc portable asus en promo : ' + str(len(p)))
print('il y a ' + str(31) + ' ordinateurs portables dell en promo\n')

# DELL 
list_url = ["https://www.darty.com/nav/recherche?p=200&s=relevence&text=dell&fa=756",
            "https://www.darty.com/nav/recherche?p=200&s=relevence&text=dell&fa=756&o=200"]
for url in list_url : 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find_all('div', {'class' : 'page-main clearfix'})
    p = div[0].find_all('p', {'class':'darty_prix_barre_remise darty_small separator_top'})
    print('nombre de pc portable dell en promo sur chaque page : ' + str(len(p)))
print('il y a ' + str(55+24) + ' ordinateurs portables dell en promo')

#------------------------------------------------------------------------------


