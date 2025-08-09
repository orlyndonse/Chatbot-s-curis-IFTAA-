// src/routers/actions/resetPassword.js
import { redirect } from "react-router-dom";

export const resetPasswordAction = async ({ request }) => {
    const formData = await request.formData();
    const newPassword = formData.get("new_password");
    const confirmPassword = formData.get("confirm_password");
    // Récupérer le token depuis le formulaire (ajouté à l'étape 4)
    const token = formData.get("token");

    // ... (Validations client inchangées) ...
    if (!token) {
         return { error: "Token de réinitialisation manquant." };
    }
     if (!newPassword || !confirmPassword) {
         return { error: "Tous les champs sont requis" };
     }
     if (newPassword !== confirmPassword) {
         return { error: "Les mots de passe ne correspondent pas" };
     }
     if (newPassword.length < 8) {
         return { error: "Le mot de passe doit contenir au moins 8 caractères" };
     }

    try {
        const response = await fetch(
            // L'URL n'inclut plus le token
            `http://localhost:8000/api/v1/auth/password-reset-confirm`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    token: token, // Envoyer le token dans le corps
                    new_password: newPassword,
                    confirm_new_password: confirmPassword
                }),
            }
        );
        // ... (gestion de la réponse inchangée) ...
         const data = await response.json();

         if (!response.ok) {
             return {
                 error: data.detail || "Échec de la réinitialisation",
                 status: response.status
             };
         }

         return redirect("/login?reset=success");

    } catch (error) {
        console.error("Erreur:", error);
        return {
            error: "Erreur de connexion au serveur",
            status: 500
        };
    }
};