import React from 'react';

const ArticleModal = ({ article, onClose }) => {
  // Fermer la modale en cliquant à l'extérieur
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  // Formatter la date
  const formatDate = (dateString) => {
    if (!dateString) return 'Date non spécifiée';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      });
    } catch (e) {
      return dateString;
    }
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <div className="modal-header">
          <h2 className="modal-title">{article.titre || 'Sans titre'}</h2>
          <div className="modal-meta">
            <strong>{article.auteur || 'Auteur inconnu'}</strong> • {formatDate(article.date)}
          </div>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        {article.thumbnail && (
          <div className="modal-image-container">
            <img 
              src={article.thumbnail} 
              alt="thumbnail" 
              className="modal-image" 
              style={{ width: '100%', maxHeight: '400px', objectFit: 'cover' }}
            />
          </div>
        )}
        
        <div className="modal-body">
          <hr className="article-divider" />
          
          {article.contenu && Array.isArray(article.contenu) ? (
            article.contenu.map((item, index) => {
              if (item.type === 'paragraphe') {
                return <p key={index} className="article-paragraph">{item.text}</p>;
              }
              if (item.type === 'titre') {
                return <h3 key={index} className="article-heading">{item.text}</h3>;
              }
              if (item.type === 'liste') {
                return (
                  <ul key={index} className="article-list">
                    {item.items.map((li, idx) => (
                      <li key={idx} className="article-list-item">{li}</li>
                    ))}
                  </ul>
                );
              }
              return null;
            })
          ) : (
            article.contenu && <p className="article-paragraph">{article.contenu}</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ArticleModal;
