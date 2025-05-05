import React from 'react';

const ArticleCard = ({ article, onClick }) => {
  // Si la date est disponible, formatons-la proprement
  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
      });
    } catch (e) {
      return dateString;
    }
  };

  return (
    <div className="article-card" onClick={onClick}>
      {article.thumbnail && (
        <img 
          src={article.thumbnail} 
          alt={article.titre || 'Article thumbnail'} 
          className="article-image" 
        />
      )}
      <div className="article-content">
        <h3 className="article-title">{article.titre || 'Sans titre'}</h3>
        <div className="article-meta">
          <span>{article.auteur || 'Auteur inconnu'}</span>
          <span>{formatDate(article.date)}</span>
        </div>
      </div>
    </div>
  );
};

export default ArticleCard;
