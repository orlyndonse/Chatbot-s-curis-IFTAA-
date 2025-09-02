import React, { createContext, useState, useEffect, useCallback, useMemo, useContext } from 'react';
import PropTypes from 'prop-types';

// 1. Créer le contexte
const LanguageContext = createContext();

// 2. Créer le fournisseur de contexte
export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(
    () => localStorage.getItem('language') || 'fr'
  );

  useEffect(() => {
    // Mettre à jour le localStorage et les attributs de la page quand la langue change
    localStorage.setItem('language', language);
    document.documentElement.lang = language;
    document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr';
  }, [language]);

  const toggleLanguage = useCallback(() => {
    setLanguage((prevLang) => (prevLang === 'fr' ? 'ar' : 'fr'));
  }, []);

  const value = useMemo(() => ({
    language,
    toggleLanguage,
  }), [language, toggleLanguage]);

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

LanguageProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

// 3. Créer un hook pour utiliser le contexte facilement
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};