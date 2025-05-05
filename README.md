# TP Scraping - BeautifulSoup

## Description

Le TP consiste en une application web permettant de collecter, stocker et explorer des articles en ligne depuis le Blog du Modérateur. 
Il est composé d'un scraper qui extrait les données d'articles, d'une API REST pour les interroger, et d'une interface utilisateur React pour visualiser et filtrer les résultats.
Pour des raisons de temps, le TP s'arrête au bout de 3 pages scrapées par catégorie mais le nombre max de pages est modifiable dans le code du fichier 'bs4_tp.py'. 

## Fonctionnalités principales

- **Scraping d'articles** : extraction automatique du contenu d'articles depuis le Blog du Modérateur
- **Stockage en base de données MongoDB** : sauvegarde structurée des articles avec leurs métadonnées
- **API REST** : endpoints pour requêter et filtrer les articles selon divers critères
- **Interface utilisateur réactive** : exploration des articles avec filtres multiples
- **Visualisation détaillée** : consultation du contenu complet des articles avec mise en forme
- **Filtrage avancé** : recherche par catégorie, sous-catégorie, auteur, titre et plage de dates

## Technologies utilisées

### Backend
- **Python 3** : langage principal pour le scraper et l'API
- **Beautiful Soup 4** : extraction de données HTML
- **Flask** : framework web léger pour l'API REST
- **PyMongo** : connecteur MongoDB pour Python
- **Flask-CORS** : gestion des requêtes cross-origin

### Frontend
- **React** : bibliothèque JavaScript pour l'interface utilisateur
- **Axios** : client HTTP pour les requêtes API
- **CSS3** : styles et mise en page responsive

### Base de données
- **MongoDB** : stockage NoSQL des articles scrapés

## Installation

### Prérequis
- Python 3.6+
- Node.js et npm
- MongoDB

### Étapes d'installation

1. Cloner le dépôt :
   ```bash
   git clone <url-du-depot>
   cd tps_scrapping
   ```

2. Installer les dépendances Python :
   ```bash
   pip3 install beautifulsoup4 requests pymongo flask flask-cors
   ```

3. Installer les dépendances JavaScript :
   ```bash
   cd frontend
   npm install
   ```

4. Configurer MongoDB :
   - Assurez-vous que MongoDB est en cours d'exécution sur localhost:27017
   - Une base de données nommée 'beautifulsoup' sera automatiquement créée

## Démarrage

1. Lancer le scraper pour collecter des articles (optionnel si la base est déjà alimentée) :
   ```bash
   cd scraper
   python3 bs4_tp.py
   ```

2. Démarrer l'API :
   ```bash
   cd api
   python3 api_script.py
   ```
   L'API sera accessible sur http://localhost:5000

3. Lancer l'interface utilisateur :
   ```bash
   cd frontend
   npm start
   ```
   L'application sera accessible sur http://localhost:3000

## Utilisation

1. Ouvrez votre navigateur et accédez à http://localhost:3000
2. Utilisez les filtres pour rechercher des articles par catégorie, sous-catégorie, auteur, titre ou date
3. Cliquez sur un article pour afficher son contenu complet dans une fenêtre modale