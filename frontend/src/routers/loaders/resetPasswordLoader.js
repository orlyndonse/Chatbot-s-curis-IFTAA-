export const resetPasswordLoader = async ({ request }) => { // request est disponible ici
  const url = new URL(request.url);
  const token = url.searchParams.get("token"); // Lire depuis ?token=

  if (!token) {
      // Gérer l'absence de token (redirection, erreur...)
      // Exemple : throw redirect('/login?error=invalid_reset_link');
       throw new Response("Token manquant dans le lien", { status: 400 });
  }

  try {
       const res = await fetch(`http://localhost:8000/api/v1/auth/validate-reset-token/${token}`);
       if (!res.ok) throw new Error("Token invalide ou expiré");
       const validationData = await res.json();
       if (!validationData.valid) {
           throw new Error(validationData.detail || "Token invalide ou expiré");
       }
       return { token }; // Retourner le token si valide
  } catch (error) {
       console.error("Validation token failed:", error);
       // Gérer l'erreur de validation (redirection, message...)
       // Exemple : throw redirect(`/login?error=${encodeURIComponent(error.message)}`);
       throw new Response(error.message || "Token invalide ou expiré", { status: 400 });
  }
};