import { redirect } from "react-router-dom";

export const loginLoader = async () => {
  const token = localStorage.getItem("awesomeLeadsToken");
  
  // 1. Si pas de token, on laisse afficher la page de login
  if (!token) return null;

  try {
    // 2. Vérification du token avec le endpoint /me
    const response = await fetch("http://localhost:8000/api/v1/auth/me", {
      headers: { Authorization: `Bearer ${token}` }
    });

    // 3. Token valide - redirection vers l'accueil
    if (response.ok) return redirect("/");

    // 4. Token invalide - nettoyage
    localStorage.removeItem("awesomeLeadsToken");
    return null;

  } catch (error) {
    // 5. Erreur réseau - on laisse quand même afficher le login
    console.error("Erreur de vérification du token:", error);
    return null;
  }
};