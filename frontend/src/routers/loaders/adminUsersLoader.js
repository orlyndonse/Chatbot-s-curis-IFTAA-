import { redirect } from "react-router-dom";
import { fetchWithAuth } from "../../utils/fetchWithAuth";
import { getUserFromLocalStorage } from "./appLoader";

export const adminUsersLoader = async () => {
  const user = getUserFromLocalStorage();

  // Sécurité : si pas d'utilisateur ou si l'utilisateur n'est pas admin, on redirige
  if (!user || user.role !== 'admin') {
    // Redirige vers la page d'accueil si l'utilisateur n'est pas autorisé
    return redirect('/');
  }

  try {
    const users = await fetchWithAuth('/api/v1/admin/users');
    return { users };
  } catch (error) {
    console.error("Failed to load users for admin:", error);
    // En cas d'erreur (ex: token expiré), on peut aussi rediriger vers le login
    if (error.status === 401) return redirect('/login');
    // Pour d'autres erreurs, on peut afficher une page d'erreur ou simplement retourner un tableau vide
    return { users: [] };
  }
};