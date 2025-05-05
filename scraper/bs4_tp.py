import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')  
db = client['beautifulsoup']  
collection = db['articles'] 

# Fonction pour récupérer les détails et le contenu d'un article
def get_details(url, categorie):
    # En-têtes pour simuler un vrai navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR] Requête échouée pour {url} : {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Récupérer le titre de l'article
    try:
        titre = soup.find('h1', class_='entry-title pt-md-8 pt-6 pb-4').get_text(strip=True)
    except AttributeError:
        print(f"[ERREUR] Titre introuvable pour {url}")
        return None

    # Récupérer le thumbnail
    thumbnail = soup.find('meta', property='og:image')
    thumbnail_url = thumbnail['content'] if thumbnail else None

    # Récupérer la sous-catégorie
    sous_categorie_tag = soup.find('a', class_='post-tags')
    sous_categorie = sous_categorie_tag.get_text(strip=True) if sous_categorie_tag else None

    # Récupérer le résumé
    resume_tag = soup.find('div', class_='article-hat t-quote pb-md-8 pb-5')
    resume = resume_tag.get_text(strip=True) if resume_tag else None

    # Récupérer la date de publication
    date_tag = soup.find('time', class_='entry-date published updated')
    date_str = date_tag['datetime'] if date_tag and date_tag.has_attr('datetime') else None
    try:
        date_formatted = datetime.fromisoformat(date_str).date().isoformat() if date_str else None
    except (ValueError, TypeError):
        date_formatted = None

    # Récupérer l'auteur
    auteur_tag = soup.find('span', class_='byline')
    auteur = auteur_tag.get_text(strip=True).replace('Par ', '') if auteur_tag else None

    # Récupérer les images dans l'article
    images_dict = {}
    seen_urls = set()
    article_content = soup.find('div', class_='col-12 mt-md-8 mt-6 mb-md-7 mb-4')

    if not article_content:
        print(f"[ERREUR] Contenu introuvable pour {url}")
        return None

    img_tags = article_content.find_all('img', class_=re.compile(r'\bwp-image-\d+\b'))

    for img in img_tags:
        url_img = img.get('data-src') or img.get('data-lazy-src') or img.get('src')
        if not url_img and img.get('srcset'):
            url_img = img['srcset'].split(',')[0].split()[0].strip()

        description = img.get('alt', '')

        if url_img and not url_img.startswith('data:image') and url_img not in seen_urls:
            images_dict[f'image_{len(images_dict) + 1}'] = {'url': url_img, 'description': description}
            seen_urls.add(url_img)

    # Récupérer le contenu complet de l'article avec les retours à la ligne
    # Supprimer les éléments non pertinents
    meta_data = article_content.find('div', class_='list-article entry-meta p-4')
    if meta_data:
        meta_data.decompose()

    cookie_data = article_content.find('div', class_='boxed-s p-4')
    if cookie_data:
        cookie_data.decompose()

    contenu_elements = article_content.find_all(['p', 'h2', 'ul'])
    contenu = []

    for element in contenu_elements:
        if element.name == 'p':
            for a_tag in element.find_all('a'):
                a_tag.insert_before(" ")
                a_tag.insert_after(" ")
            text = element.get_text(separator="\n", strip=True)
            if text:
                contenu.append({'type': 'paragraphe', 'text': text})
        elif element.name == 'h2':
            text = element.get_text(strip=True)
            if text:
                contenu.append({'type': 'titre', 'text': text})
        elif element.name == 'ul':
            list_items = [li.get_text(strip=True) for li in element.find_all('li')]
            if list_items:
                contenu.append({'type': 'liste', 'items': list_items})

    # Créer un dictionnaire pour l'article
    article_details = {
        'titre': titre,
        'thumbnail': thumbnail_url,
        'categorie': categorie,
        'sous_categorie': sous_categorie,
        'resume': resume,
        'date': date_formatted,
        'auteur': auteur,
        'images': images_dict,
        'contenu': contenu
    }

    return article_details


# Fonction pour récupérer tous les liens d'articles sur une page
def get_article_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article_links = []
    articles = soup.find_all('article')
    for article in articles:
        link_tag = article.find('a', href=True)
        if link_tag:
            article_links.append(link_tag['href'])

    return article_links

# Fonction pour scraper toutes les pages d'une catégorie
def get_all_pages(categorie, start_url, max_pages=3):
    all_articles = []
    url = start_url
    page_number = 1

    while url and page_number <= max_pages:
        # Récupérer les liens de tous les articles sur la page courante
        article_links = get_article_links(url)
        
        # Scraper chaque article
        for article_url in article_links:
            article_details = get_details(article_url, categorie)
            if article_details:  # Vérifie que le scraper n’a pas échoué
                all_articles.append(article_details)
                # Sauvegarder l'article dans MongoDB
                try:
                    collection.insert_one(article_details)
                except Exception as e:
                    print(f"Erreur MongoDB lors de l’insertion de {article_url} : {e}")

        # Passer à la page suivante (URL corrigée)
        page_number += 1
        url = f"https://www.blogdumoderateur.com/{categorie}/page/{page_number}/"  

        # Vérifier si la page suivante existe (si l'URL renvoie un statut 404, alors on arrête)
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Page {page_number} not found. Scraping complete.")
            break

    return all_articles

# Liste des catégories
categories = ['web', 'marketing', 'social', 'tech']

# Scraper les articles de chaque catégorie
for categorie in categories:
    start_url = f"https://www.blogdumoderateur.com/{categorie}"
    print(f"Scraping category: {categorie}")
    articles = get_all_pages(categorie, start_url, max_pages=3)
