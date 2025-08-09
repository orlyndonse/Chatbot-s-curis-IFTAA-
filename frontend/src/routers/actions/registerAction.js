/**
 * @copyright 2025 isetsfax
 */

import { redirect } from "react-router-dom";

export const registerAction = async ({ request }) => {
  const formData = await request.formData();

  const userData = {
    username: formData.get("username"),
    email: formData.get("email"),
    first_name: formData.get("first_name"),
    last_name: formData.get("last_name"),
    password: formData.get("password"),
  };

  try {
    // 1. Enregistrement uniquement
    const signupResponse = await fetch("http://localhost:8000/api/v1/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });

    const responseData = await signupResponse.json(); // Lire la réponse même en cas d'erreur

    if (!signupResponse.ok) {
      // Gérer les erreurs d'inscription du backend
      let errorMessage = "Échec de l'inscription";
      if (responseData.detail) {
        errorMessage = responseData.detail;
      } else if (responseData.message) {
        errorMessage = responseData.message;
      } else if (typeof responseData === 'string') {
        errorMessage = responseData;
      }
      // Renvoyer l'erreur pour affichage (par ex: snackbar)
      return {
        ok: false,
        message: errorMessage,
      };
    }

    // 2. Si l'inscription réussit (status 201), rediriger directement
    console.log("Signup successful, redirecting to send-email page...");
    return redirect(`/send-email?email=${encodeURIComponent(userData.email)}`);

    /* ---> SECTION SUPPRIMÉE <---
    // 2. Connexion automatique (Supprimée car cause le problème)
    const loginResponse = await fetch("http://localhost:8000/api/v1/auth/login", { ... });
    if (!loginResponse.ok) { ... }
    const { access_token } = await loginResponse.json();
    localStorage.setItem("awesomeLeadsToken", access_token);
    */

  } catch (err) {
    // Gérer les erreurs réseau ou autres erreurs inattendues
    console.error("Error during registration fetch:", err);
    return {
      ok: false,
      // Fournir un message d'erreur générique ou plus spécifique si possible
      message: err.message || "Une erreur réseau est survenue lors de l'inscription",
    };
  }
};