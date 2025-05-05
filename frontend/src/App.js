import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ArticleCard from './ArticleCard';
import ArticleModal from './ArticleModal';
import './App.css';

const App = () => {
  const [filters, setFilters] = useState({
    categorie: '',
    sous_categorie: '',
    auteur: '',
    titre: '',
    date_debut: '',
    date_fin: ''
  });

  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const res = await axios.get('http://localhost:5000/articles', {
        params: {
          categorie: filters.categorie,
          sous_categorie: filters.sous_categorie,
          auteur: filters.auteur,
          titre: filters.titre,
          date_debut: filters.date_debut,
          date_fin: filters.date_fin
        }
      });

      setArticles(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  return (
    <div className="App">
      <div className="main-container">
        <h1>Recherche d'Articles</h1>
        
        <div className="filter-container">
          <div className="filter-grid">
            <input 
              className="filter-input" 
              name="categorie" 
              placeholder="Catégorie" 
              value={filters.categorie}
              onChange={handleChange} 
            />
            <input 
              className="filter-input" 
              name="sous_categorie" 
              placeholder="Sous-Catégorie" 
              value={filters.sous_categorie}
              onChange={handleChange} 
            />
            <input 
              className="filter-input" 
              name="auteur" 
              placeholder="Auteur" 
              value={filters.auteur}
              onChange={handleChange} 
            />
            <input 
              className="filter-input" 
              name="titre" 
              placeholder="Titre" 
              value={filters.titre}
              onChange={handleChange} 
            />
            <input 
              className="filter-input" 
              name="date_debut" 
              type="date" 
              value={filters.date_debut}
              onChange={handleChange} 
            />
            <input 
              className="filter-input" 
              name="date_fin" 
              type="date" 
              value={filters.date_fin}
              onChange={handleChange} 
            />
            <div className="search-button-container">
              <button className="search-button" onClick={fetchArticles}>
                {loading ? 'Chargement...' : 'Rechercher'}
              </button>
            </div>
          </div>
        </div>

        {loading ? (
          <div style={{textAlign: 'center', padding: '2rem'}}>
            <p>Chargement des articles...</p>
          </div>
        ) : (
          <div className="articles-grid">
            {articles.length > 0 ? (
              articles.map(article => (
                <ArticleCard 
                  key={article._id} 
                  article={article} 
                  onClick={() => setSelectedArticle(article)} 
                />
              ))
            ) : (
              <div style={{gridColumn: '1 / -1', textAlign: 'center', padding: '2rem'}}>
                <p>Aucun article trouvé. Veuillez ajuster vos critères de recherche.</p>
              </div>
            )}
          </div>
        )}

        {selectedArticle && (
          <ArticleModal article={selectedArticle} onClose={() => setSelectedArticle(null)} />
        )}
      </div>
    </div>
  );
};

export default App;
