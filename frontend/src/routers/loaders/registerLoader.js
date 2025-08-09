/**
 * @copyright 2025 isetsfax
 */

import { redirect } from "react-router-dom";

export const registerLoader = async () => {
  // Si vous voulez rediriger les utilisateurs déjà connectés
  // (À adapter selon votre logique d'authentification)
  const token = localStorage.getItem("awesomeLeadsToken");
  if (token) {
    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/me", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) return redirect("/"); // Redirige si déjà connecté
    } catch (err) {
      console.error("Erreur de vérification du token :", err);
    }
  }
  return null; // Continue vers la page d'inscription
};