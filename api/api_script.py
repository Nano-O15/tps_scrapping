from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import json
import re

app = Flask(__name__)
CORS(app)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['beautifulsoup']
collection = db['articles']

# Convertisseur pour les types non sérialisables
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

# Route pour rechercher des articles par catégorie ou sous-catégorie (insensible à la casse)
@app.route('/articles', methods=['GET'])
def get_articles():
    # Récupération de tous les paramètres de filtrage
    categorie = request.args.get('categorie')
    sous_categorie = request.args.get('sous_categorie')
    auteur = request.args.get('auteur')
    titre = request.args.get('titre')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')

    query = {}
    
    # Application des filtres si présents
    if categorie:
        query['categorie'] = re.compile(f'^{re.escape(categorie)}$', re.IGNORECASE)
    if sous_categorie:
        query['sous_categorie'] = re.compile(f'^{re.escape(sous_categorie)}$', re.IGNORECASE)
    if auteur:
        query['auteur'] = re.compile(re.escape(auteur), re.IGNORECASE)
    if titre:
        query['titre'] = re.compile(re.escape(titre), re.IGNORECASE)
    
    # Filtres de date
    date_conditions = {}
    if date_debut:
        date_conditions['$gte'] = date_debut
    if date_fin:
        date_conditions['$lte'] = date_fin
    if date_conditions:
        query['date'] = date_conditions

    articles = list(collection.find(query))
    return JSONEncoder().encode(articles), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)
