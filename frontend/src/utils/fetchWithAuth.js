import { redirect } from 'react-router-dom';

const API_BASE_URL = "http://localhost:8000";

/**
 * Fonction utilitaire pour effectuer des requêtes API authentifiées.
 * Gère la récupération du jeton, l'ajout de l'en-tête Authorization, la gestion basique des erreurs,
 * et les redirections en cas d'erreurs 401/403.
 */
export const fetchWithAuth = async (endpoint, options = {}) => {
  const token = localStorage.getItem("awesomeLeadsToken");

  if (!token && !options.allowAnonymous) {
    console.warn(`fetchWithAuth: No token found for protected route ${endpoint}. Redirecting to login.`);
    throw redirect('/login');
  }

  const headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Expires': '0',
    ...options.headers,
  };

  // Ne définir l'en-tête Authorization que si le jeton existe
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Ne pas définir Content-Type si le corps est FormData
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.status === 401 || response.status === 403) {
      console.warn(`fetchWithAuth: Auth error (${response.status}) for ${endpoint}. Cleaning token and redirecting.`);
      localStorage.removeItem("awesomeLeadsToken");
      localStorage.removeItem("awesomeLeadsRefreshToken");
      throw redirect('/login');
    }

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        errorData = { detail: `HTTP Error ${response.status}: ${response.statusText}` };
      }
      console.error(`API Error (${response.status}) on ${endpoint}:`, errorData);
      const error = new Error(errorData.detail || `API Error (${response.status})`);
      error.status = response.status;
      error.data = errorData;
      throw error;
    }

    // Gérer spécifiquement le statut 204 No Content
    if (response.status === 204) {
      return null;// Ou renvoyer un indicateur de succès si nécessaire
    }

    // // Supposer une réponse JSON pour les autres requêtes réussies
    return await response.json();

  } catch (error) {
    if (error instanceof Response && error.status >= 300 && error.status < 400) {
      throw error; // Relancer les réponses de redirection
    }
    console.error(`fetchWithAuth Error during fetch for ${endpoint}:`, error);
    throw error; // Relancer l'erreur pour qu'elle soit gérée par l'appelant
  }
};
