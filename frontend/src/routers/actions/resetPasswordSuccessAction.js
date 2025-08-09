// my chat application/Code_Source/frontend/src/routers/actions/resetPasswordSuccessAction.js
// (Nom de fichier inchangé, mais la logique interne change)

export const resetPasswordSuccessAction = async ({ request }) => {
    const formData = await request.formData();
    const email = formData.get("email");

    try {
        const response = await fetch(
            // --- CORRECTION DE L'ENDPOINT ---
            "http://localhost:8000/api/v1/auth/password-reset-request", // On appelle l'endpoint de demande de réinitialisation
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                // --- CORRECTION DU FORMAT DU CORPS ---
                // Cet endpoint attend {"email": "..."}
                body: JSON.stringify({ email: email }),
            }
        );

        if (!response.ok) {
            const error = await response.json();
            // L'erreur potentielle ici serait plutôt liée à l'inexistence du compte,
            // mais le backend renvoie un message générique "Si un compte..."
            // donc on garde un message d'erreur générique côté frontend.
            throw new Error(error.detail || "Échec de la nouvelle demande");
        }

        // Message de succès pour le renvoi de l'email de réinitialisation
        return { ok: true, message: "✅ Nouveau lien envoyé !" };

    } catch (err) {
        return { ok: false, message: `❌ ${err.message}` };
    }
};