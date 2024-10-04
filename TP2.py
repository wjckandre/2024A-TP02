"""
TP2 : Système de gestion de livres pour une bibliothèque

Groupe de laboratoire : 06
Numéro d'équipe :  13
Noms et matricules : Wojcik André 2374413, Wajdi Gherairi 2368214
"""
import csv
import datetime

########################################################################################################## 
# PARTIE 1 : Création du système de gestion et ajout de la collection actuelle
########################################################################################################## 

bibliotheque = {}
csvfile = open('collection_bibliotheque.csv', newline='')
reader = csv.reader(csvfile)

for row in reader:
    if row[0] != 'titre':
        bibliotheque[row[3]] = {"titre" : row[0], "auteur" : row[1], "date_publication" : row[2]}


print(f" \n Bibliotheque initiale : {bibliotheque} \n")


########################################################################################################## 
# PARTIE 2 : Ajout d'une nouvelle collection à la bibliothèque
########################################################################################################## 

csvfile = open('nouvelle_collection.csv', newline='')
reader = csv.reader(csvfile)

for row in reader:
    if row[0] != 'titre':
        if row[3] in bibliotheque.keys():
            print(f"Le livre {row[3]} ---- {row[0]} par {row[1]} ---- est déjà présent dans la bibliothèque")
        else:
            print(f"Le livre {row[3]} ---- {row[0]} par {row[1]} ---- a été ajouté avec succès")
            bibliotheque[row[3]] = {"titre" : row[0], "auteur" : row[1], "date_publication" : row[2]}




########################################################################################################## 
# PARTIE 3 : Modification de la cote de rangement d'une sélection de livres
########################################################################################################## 

cote_change = []
for cote,info in bibliotheque.items():

    if 'S' in cote:
        cote_change.append(cote)
for i in cote_change:
    temp = bibliotheque.pop(i)
    new_cote = "W"+i
    bibliotheque[new_cote] = temp



print(f' \n Bibliotheque avec modifications de cote : {bibliotheque} \n')




########################################################################################################## 
# PARTIE 4 : Emprunts et retours de livres
########################################################################################################## 

csvfile = open('emprunts.csv', newline='')
reader = csv.reader(csvfile)

print(reader)
emprunts = []
for row in reader:
    emprunts.append(row[0])
    if row[0] != 'cote_rangement':
        if 'S' in row[0]:
            bibliotheque['W'+row[0]]['date_emprunt'] = row[1]
            row[0] = 'W'+row[0]
        else:
            bibliotheque[row[0]]['date_emprunt'] = row[1]

for cote,info in bibliotheque.items():
    # if 'WS' in cote:
    #     temp = cote.replace('WS','S')
    #     if temp in emprunts:
    #         bibliotheque[cote]['emprunts']=  "emprunté"
    #     else:
    #         bibliotheque[cote]['emprunts'] = "disponible"    
    if cote in emprunts:
        bibliotheque[cote]['emprunts']=  "emprunté"
    else:
        bibliotheque[cote]['emprunts'] = "disponible"


print(f' \n Bibliotheque avec ajout des emprunts : {bibliotheque} \n')


########################################################################################################## 
# PARTIE 5 : Livres en retard 
########################################################################################################## 

date = datetime.datetime.now().date()

livres_perdus = []
for cote,info in bibliotheque.items():
    if info['emprunts'] == 'emprunté':
        date_emprunt = datetime.datetime(int(info['date_emprunt'][0:4]), int(info['date_emprunt'][5:7]), int(info['date_emprunt'][8:10]))
        date_actuel = datetime.datetime(date.year, date.month, date.day)
        temps_emprunt = date_actuel - date_emprunt
        if temps_emprunt.days >= 365:
            livres_perdus.append(cote)
        elif temps_emprunt.days >= 80:
            bibliotheque[cote]["frais_retard"] = 100
        elif temps_emprunt.days > 30:
            bibliotheque[cote]["frais_retard"] = (temps_emprunt.days - 30) * 2
bibliotheque["livres_perdus"] = livres_perdus

print(f' \n Bibliotheque avec ajout des retards et frais : {bibliotheque} \n')

