import { redirect } from 'react-router-dom';

const API_BASE_URL = "http://localhost:8000"; // Or use import.meta.env.VITE_API_URL

/**
 * Helper function for making authenticated API requests.
 * Handles token retrieval, adding Authorization header, basic error handling,
 * and redirects on 401/403 errors.
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

  // Only set Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Do not set Content-Type if the body is FormData
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

    // Handle 204 No Content specifically
    if (response.status === 204) {
      return null; // Or return a success indicator if needed
    }

    // Assume JSON response for other successful requests
    return await response.json();

  } catch (error) {
    if (error instanceof Response && error.status >= 300 && error.status < 400) {
      throw error; // Re-throw redirect responses
    }
    console.error(`fetchWithAuth Error during fetch for ${endpoint}:`, error);
    throw error; // Re-throw the error to be handled by the caller
  }
};
