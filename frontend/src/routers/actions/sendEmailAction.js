export const sendEmailAction = async ({ request }) => {
    const formData = await request.formData();
    const email = formData.get("email");

    try {
        const response = await fetch(
            "http://localhost:8000/api/v1/auth/resend-verification-email",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ addresses: [email] }), // Format compatible
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Échec de l'envoi");
        }

        return { ok: true, message: "✅ Email renvoyé ! Vérifiez vos spams." };

    } catch (err) {
        return { ok: false, message: `❌ ${err.message}` };
    }
};