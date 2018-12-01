# =============================================================================
# EXERCICE : les résultats sont données dans l'odre : LVMH / AIRBUS / DANONE
#
# Récupérer les informations suivantes pour les sociétés : LVMH, Airbus et Danone
# 1. Ventes au quarter à fin décembre 2018
# 2. Prix de l'action et son % de changement au moment du crawling
# 3. % Shares Owned des investisseurs institutionels
# 4. Dividend yield de la company, le secteur et de l'industrie
# =============================================================================

# Pour voir les réponses sous forme de DataFrame : 
# Exécuter la totalité du script et afficher df1, df2, df3 et df4

# Chargement des packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Connexion aux url pour obtenir le code source et usage de BeautifulSoup
list_url = ["https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/AIR.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/DANO.PA"]

# =============================================================================
# 1. Ventes au quarter à fin décembre 2018
# =============================================================================

result = []

for url in list_url :
	# Récuper html et le parser
	response = requests.get(url)
	parser = BeautifulSoup(response.content, 'html.parser')	
	div = parser.find_all('div', {'class' : 'moduleBody'})
	td = div[2].find_all('td')	
	ventes_millions = td[1]
	ventes_millions_text = ventes_millions.text	
	nb_estimates = td[2]
	nb_estimates_text = nb_estimates.text	
	mean = td[3]
	mean_text = mean.text	
	high = td[4]
	high_text = high.text	
	low = td[5]
	low_text = low.text	
	year_ago = td[6]
	year_ago_text = year_ago.text
	# Print les résultats
	print('\nRésultats :\n',
		  '\nSales in millions : ', ventes_millions.text, ', ' ,
          '# of estimates : ' , nb_estimates.text, ', ',
          'mean : ' , mean.text , ', ' ,
          'high : ' , high.text , ', ' ,
          'low : ' , low.text , ', ' , 
          '1 year ago : ' , year_ago.text)
	
	# Print les résultats sous forme de DataFrame	
	result.append([ventes_millions_text, nb_estimates_text, mean_text, 
				high_text, low_text, year_ago_text])

index = ['LVMH', 'Airbus', 'Danone']	
df1 = pd.DataFrame(result, columns=['Period for sales in million', 'Nb estimates', 
									'mean', 'high', 'low',
									'1_year_ago'], index=index)
print(df1)

# =============================================================================
# 2. Prix de l'action et son % de changement au moment du crawling
# =============================================================================

result = []

for url in list_url:
	response = requests.get(url)
	parser = BeautifulSoup(response.content, 'html.parser')

	# Toutes les class : class='sectionQuoteDetail' avec un selecteur retournant une liste
	class_sectionQuote = parser.select('.sectionQuoteDetail')
	span_prix = class_sectionQuote[0].find_all('span')
	span_change = class_sectionQuote[1].find_all('span')
	
	# Prix
	prix = span_prix[1]
	devise = span_prix[2]
	prix_text = prix.text
	devise_text = devise.text
	
	# Change in %
	change = span_change[2]
	change_text = change.text
	
	# regex : supprimer certains pattern dans le prix et le change
	prix_text = re.sub('\n\t\t\t\t', '', prix_text)
	change_text = re.sub('\t\t    \n\t\t\t\t\t\t    ', '', change_text)
	print('prix :', prix_text, devise_text, '& change in % :', change_text)
	
	# Enregistrer les resultats dans un dataframe
	result.append([prix_text,devise_text, change_text])

print('\n Résultats sous forme de DataFrame:')	
index = ['LVMH', 'Airbus', 'Danone']	
df2 = pd.DataFrame(result, columns = ['prix', 'devise', 'change %'], index=index)
print(df2)

# =============================================================================
# 3. % Shares Owned des investisseurs institutionels
# =============================================================================

result = []
    
for url in list_url : 
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    div = soup.find_all('div', {'class' : 'moduleBody'})
    td = div[13].find_all('td')
    shares_owned = td[1]
    shares_owned_text = shares_owned.text
    """ print les résultats pour les 3 url """
    print('\nRésultats :\n' , '\n' ,
          '% shares owned : ' , shares_owned_text)
    result.append(shares_owned_text)
	
# On affiche les résultats avec ceux de la question précédente	
index = ['LVMH', 'Airbus', 'Danone']		
df_bis = pd.DataFrame(result, columns = ['Shares owned'], index=index)
df3 = pd.concat([df2, df_bis], axis=1)
print('\nRésultats', '\n', df3)
del df_bis
  
# =============================================================================
# 4. Dividend yield de la company, du secteur et de l'industrie
# =============================================================================    
    
result = []
for url in list_url : 
    
    response = requests.get(url)
    parser = BeautifulSoup(response.content, 'html.parser')
    
    div = parser.find_all('div', {'class' : 'moduleBody'})
    td = div[4].find_all('td')
    dividend_yield_company = td[1] 
    dividend_yield_sector = td[2]
    dividend_yield_insdustry = td[3]

    """ print les résultats pour les 3 url """
    print('\nRésultats :\n' + '\n' +
          'Dividend yield company : ' , dividend_yield_company.text, ', ' ,
          'Dividend yield sector : ' , dividend_yield_sector.text, ', ' ,
          'Dividend yield industry : ' , dividend_yield_insdustry.text)
    result.append([dividend_yield_company.text, dividend_yield_sector.text, 
				   dividend_yield_insdustry.text])

# Print les résultats sous forme de DataFrame
index = ['LVMH', 'Airbus', 'Danone']	
columns = ['dividend_yield_company', 'dividend_yield_sector', 'dividend_yield_insdustry']
df_bis = pd.DataFrame(result, columns=columns, index=index)
df4 = pd.concat([df3, df_bis], axis=1)
print(df4)
del df_bis
