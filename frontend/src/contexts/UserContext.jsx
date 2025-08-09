import React, { createContext, useEffect, useState, useCallback } from "react";

export const UserContext = createContext();
const API_BASE_URL = "http://localhost:8000";

export const UserProvider = ({ children }) => {
  // Initialisation du token depuis localStorage
  const [token, setTokenState] = useState(() => {
    return localStorage.getItem("awesomeLeadsToken") || null;
  });

  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Synchronise le token avec le localStorage et réinitialise user si nécessaire
  const setToken = useCallback((newToken) => {
    console.log("Setting new token:", newToken ? "Token présent" : "Token absent");
    if (newToken) {
      localStorage.setItem("awesomeLeadsToken", newToken);
    } else {
      localStorage.removeItem("awesomeLeadsToken");
      localStorage.removeItem("awesomeLeadsRefreshToken"); // Nettoyage du refresh token aussi
    }
    setTokenState(newToken);
    if (!newToken) setUser(null);
  }, []);

  // Fonction pour récupérer le profil utilisateur
  const fetchUserProfile = useCallback(async () => {
    if (!token) {
      console.log("Aucun token, utilisateur non connecté");
      setIsLoading(false);
      return;
    }

    console.log("Tentative de récupération du profil avec token");
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
        headers: { 
          Authorization: `Bearer ${token}`,
          // Ajout d'en-têtes pour éviter la mise en cache
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        },
      });

      if (!response.ok) {
        console.error("Erreur API:", response.status);
        throw new Error("Session expirée ou invalide");
      }
      
      const userData = await response.json();
      console.log("Profil utilisateur récupéré:", userData.email);
      setUser(userData);
    } catch (error) {
      console.error("Erreur de récupération du profil:", error.message);
      // En cas d'erreur, on nettoie le token
      setToken(null);
    } finally {
      setIsLoading(false);
    }
  }, [token, setToken]);

  // Charge le profil au montage et quand le token change
  useEffect(() => {
    console.log("Token changé, rechargement du profil");
    fetchUserProfile();
  }, [fetchUserProfile]);

  // Écoute des changements de localStorage dans d'autres onglets/fenêtres
  useEffect(() => {
    const handleStorageChange = (e) => {
      if (e.key === "awesomeLeadsToken") {
        console.log("Token modifié dans un autre onglet");
        const newToken = e.newValue;
        setTokenState(newToken || null);
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  // Fonction de déconnexion
  const logout = useCallback(async () => {
    console.log("Tentative de déconnexion");
    try {
      // Tentative de révocation du token côté serveur
      if (token) {
        await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
          method: 'GET',
          headers: { Authorization: `Bearer ${token}` },
        }).catch(err => console.error("Erreur lors de la déconnexion côté serveur:", err));
      }
    } finally {
      // Dans tous les cas, on nettoie côté client
      setToken(null);
    }
  }, [token, setToken]);

  // Valeur fournie par le contexte
  const contextValue = {
    token,
    user,
    isLoading,
    setToken,
    logout,
  };

  return (
    <UserContext.Provider value={contextValue}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = React.useContext(UserContext);
  if (!context) throw new Error("useUser must be used within UserProvider");
  return context;
};