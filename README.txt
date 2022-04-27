------------------------README--------------------------


------------------------imports-------------------------

Vous trouverez ci-dessous les librairies externes à importer pour faire fonctionner notre programme

pip install tkinter
pip install sparqlwrapper
pip install requests
pip install mysql-connector-python


------------------------dossiers-------------------------


database : contient les requêtes SQL effectuées dans notre base de données locale

dataScraping : contient les functions permettant d'effectuant le scraping des données sur le site web https://www.the-numbers.com/

model : contient la classe model Film utilisait par le médiateur

service : contient les appels au web service OMDb API et le traitement des données retournées.

sparQL : contient les appels de la source DBPedia à l'aide de requête SParQL


------------------------autres------------------------

Le fichier main contient l'interface graphique et fais appel au médiateur

Le fichier médiateur effectue les différentes appels aux sources et effectue la jointure.