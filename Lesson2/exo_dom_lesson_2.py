# =============================================================================
# EXERCICE : les résultats sont données dans l'odre : LVMH / AIRBUS / DANONE
#
# Récupérer les informations suivantes pour les sociétés : LVMH, Airbus et Danone
# 1. Ventes au quarter à fin décembre 2018
# 2. Prix de l'action et son % de changement au moment du crawling
# 3. % Shares Owned des investisseurs institutionels
# 4. Dividend yield de la company, le secteur et de l'industrie
# =============================================================================

# Chargement des packages
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Connexion aux url pour obtenir le code source et usage de BeautifulSoup
list_url = ["https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/AIR.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/DANO.PA"]

# =============================================================================
# 1. Prix de vente de l'action et % de changement au moment du crawling
# =============================================================================

for url in list_url : 
    
    page = requests.get(url) # récupérer url
    soup = BeautifulSoup(page.content, 'html.parser') # récupérer html
     
    div = soup.find_all('div', {'class' : 'moduleBody'}) # tous les div
    td = div[2].find_all('td') # tous les td du 3e div
    ventes_millions = td[1] # 2e td = sales in millions
    nb_estimates = td[2] 
    mean = td[3]
    high = td[4]
    low = td[5]
    year_ago = td[6]
    
    """ print les résultats pour les 3 url """
    print('\nRésultats :\n' + '\n' +
          'sales in millions : ' + str(ventes_millions.text) + ', ' + 
          '# of estimates : ' + str(nb_estimates.text) + ', ' + 
          'mean : ' + str(mean.text) + ', ' +
          'high : ' + str(high.text) + ', ' +
          'low : ' + str(low.text) + ', ' + 
          '1 year ago : ' + str(year_ago.text))

# =============================================================================
# 2. Prix de l'action et son % de changement au moment du crawling
# =============================================================================

for url in list_url : 
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    div = soup.find_all('div', {'class' : 'sectionQuoteDetail'}) # tous les div
    span = div[0].find_all('span') # les span du 1er div
    prix = span[1] # 2e span
    devise = span[2]    
    
    """ print les résultats pour les 3 url """
    print('\nRésultats :\n' + '\n' +
          'prix : ' + str(prix.text) + ', ' + 
          'devise : ' + str(devise.text))  
    
# =============================================================================
# 3. % Shares Owned des investisseurs institutionels
# =============================================================================
    
for url in list_url : 
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    div = soup.find_all('div', {'class' : 'moduleBody'})
    td = div[13].find_all('td')
    shares_owned = td[1]    
    
    """ print les résultats pour les 3 url """
    print('\nRésultats :\n' + '\n' +
          '% shares owned : ' + str(shares_owned.text))
    
# =============================================================================
# 4. Dividend yield de la company, du secteur et de l'industrie
# =============================================================================    
    
for url in list_url : 
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    div = soup.find_all('div', {'class' : 'moduleBody'})
    td = div[4].find_all('td')
    dividend_yield_company = td[1] 
    dividend_yield_sector = td[2]
    dividend_yield_insdustry = td[3]

    """ print les résultats pour les 3 url """
    print('\nRésultats :\n' + '\n' +
          'Dividend yield company : ' + str(dividend_yield_company.text), ', ' +
          'Dividend yield sector : ' + str(dividend_yield_sector.text), ', ' +
          'Dividend yield industry : ' + str(dividend_yield_insdustry.text))