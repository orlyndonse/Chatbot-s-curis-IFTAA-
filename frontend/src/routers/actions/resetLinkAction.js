/**
 * @copyright 2025 isetsfax
 */

import { redirect } from "react-router-dom";

export const resetLinkAction = async ({ request }) => {
  const formData = await request.formData();

  const userData = {
    email: formData.get("email"),
  };

  try {
    // 1. Enregistrement
    const resetlinkResponse = await fetch("http://localhost:8000/api/v1/auth/password-reset-request", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });

    // Récupérer la réponse même en cas d'erreur
    const responseData = await resetlinkResponse.json();

    if (!resetlinkResponse.ok) {
      // Extraction du message d'erreur du backend de manière plus robuste
      let errorMessage = "Échec de l'envoie";
      
      if (responseData.detail) {
        errorMessage = responseData.detail;
      } else if (responseData.message) {
        errorMessage = responseData.message;
      } else if (typeof responseData === 'string') {
        errorMessage = responseData;
      }
      
      throw new Error(errorMessage);
    }

    // 3. Redirection vers la vérification email
    return redirect(`/resetpasswordsuccess?email=${encodeURIComponent(userData.email)}`);

  } catch (err) {
    // Assurer que nous retournons toujours une chaîne de caractères pour le message d'erreur
    return {
      ok: false,
      message: err.message || "Une erreur est survenue lors de l'envoie",
    };
  }
};