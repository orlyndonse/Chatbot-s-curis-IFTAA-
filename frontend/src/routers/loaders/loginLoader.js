import { redirect } from "react-router-dom";

export const loginLoader = async () => {
  const token = localStorage.getItem("awesomeLeadsToken");
  
  // 1. Si pas de token, on laisse afficher la page de login
  if (!token) {
    // ✅ Nettoyer les données utilisateur si pas de token
    localStorage.removeItem("user");
    return null;
  }

  try {
    // 2. Vérification du token avec le endpoint /me
    const response = await fetch("http://localhost:8000/api/v1/auth/me", {
      headers: { Authorization: `Bearer ${token}` }
    });

    // 3. Token valide - redirection vers l'accueil
    if (response.ok) {
      // ✅ Optionnel : Mettre à jour les données utilisateur si elles ne sont pas présentes
      const userData = await response.json();
      if (userData && !localStorage.getItem("user")) {
        localStorage.setItem('user', JSON.stringify(userData));
      }
      return redirect("/");
    }

    // 4. Token invalide - nettoyage complet
    localStorage.removeItem("awesomeLeadsToken");
    localStorage.removeItem("awesomeLeadsRefreshToken");
    localStorage.removeItem("user"); // ✅ Nettoyer aussi les données utilisateur
    return null;

  } catch (error) {
    // 5. Erreur réseau - on laisse quand même afficher le login
    console.error("Erreur de vérification du token:", error);
    return null;
  }
};