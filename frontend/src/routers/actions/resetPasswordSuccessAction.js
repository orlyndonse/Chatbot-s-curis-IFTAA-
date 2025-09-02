export const resetPasswordSuccessAction = async ({ request }) => {
    const formData = await request.formData();
    const email = formData.get("email");

    try {
        const response = await fetch(
            "http://localhost:8000/api/v1/auth/password-reset-request", // On appelle l'endpoint de demande de réinitialisation
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                // Cet endpoint attend {"email": "..."}
                body: JSON.stringify({ email: email }),
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Échec de la nouvelle demande");
        }

        // Message de succès pour le renvoi de l'email de réinitialisation
        return { ok: true, message: "✅ Nouveau lien envoyé !" };

    } catch (err) {
        return { ok: false, message: `❌ ${err.message}` };
    }
};