# Create a personal token : https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
# Token code : XXX

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://gist.github.com/paulmillr/2657075"
token_code = ' XXX '
head = {'Authorization': 'token {}'.format(token_code)}

#------------------------------------------------------------------------------
    # texte ressemble à : 
    # parent est du texte : "#1", "#2", etc
    # enfants sont des balises "td"    
    # map(function_to_apply, list_of_inputs)
    
#1. Récupérer le nom des meilleurs contributeurs : Users #1 -> #257
def get_top_users(url_link) : # Fonction qui va chercher les noms des top users
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    top_users_list = []  # Initialiser une liste
    for i in range(1,257) : 
        top_users_list.append(soup.find(text="#"+str(i)).parent.findNext("td").text)                          
    return top_users_list    
    

    # test de la fonction, stock la liste des users (avec username + nom) 
liste_users = get_top_users(url)                        

#------------------------------------------------------------------------------

# Step 1 : Récupérer la liste des users
    # 1. Récupérer le usernames des users sans le nom : 
         # eg : 'fabot (fabien pottentcier)' -> on veut que le username 'fabot' 
    # 2. Récupérer le username dans une liste des users 
    
def get_username(user_nom):
    return user_nom[:user_nom.find('(')-1] 

def get_list_usernames(list_user):
    result = list(map(get_username, list_user)) 
    return result
    # map(function_to_apply, list_of_inputs) applique une fonction à une liste d'inputs

liste_usernames = get_list_usernames(liste_users)
# print(liste_usernames)

#------------------------------------------------------------------------------

# GOAL : Récupérer la liste des moyennes des étoiles des repositories de chaque users

# Récupérer les repos des users ici : https://api.github.com/users/USERNAME/repos 
    # Entrer le username qui nous intéresse eg : fabpot > https://api.github.com/users/fabpot/repos
    # Copier le Json dans un beautifier Json : 
        # on voit que le nombre d'étoiles par repo se nomme : "stargazers_count"


# Donc: Créer une fonction qui reçoit une liste de usernames et retourne le dictionnaire

# Step 1 Créer un dictionnaire contenant les { usernames_list : mean_stars_repo  }
# Step 2 :usernames contient la liste des usernames
# Step 3  mean_stars_repo contient le nombre d'étoiles moyen / nombre de repos  
    # Récupérer les repos Json
    # Load les repos Json 
    # Compter les étoiles totales : si pas de repo, pas d'étoiles, sinon faire la division
        # si pas de repo, pas d'étoiles, sinon faire la division par le nb de repo et arrondir
        # le mettre dans mean_star_repo

def dict_usernames_stargazers(list_usernames) : 
    main_url = "https://api.github.com/users/"
    list_mean_stars = []
    dict_username = {}
    
    # Importer les repos de chaque user + mon token perso dans requests.get
    for username in list_usernames : 
        get_repo = requests.get(main_url + str(username) + "/repos", headers=head)
        json_repo = json.loads(get_repo.content)
    
    # Sum des stargazers par users
    sum_stars = 0
    mean_stars = 0
    for repo in json_repo : 
        sum_stars += repo['stargazers_count']
    
    # Moyenne des stargazers par repos de users
    if len(json_repo) == 0 : 
        mean_stars = 0
    else : 
        mean_stars = sum_stars/len(json_repo)
    
    list_mean_stars.append(round(mean_stars,3))
    
    # Rattacher les 2 listes aux dictionnaires
    dict_username["Usernames"] = list_usernames
    dict_username["Mean_stars"] = list_mean_stars
    
    return dict_usernames_stargazers

dict_users_stars = dict_usernames_stargazers(liste_usernames)

#------------------------------------------------------------------------------
# Cr"ation d'un DataFrame 

df = pd.DataFrame(dict_users_stars)
df_sorted = df.sort_values(by="Mean Stars", ascending=False)
    


















