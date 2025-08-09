import { redirect } from "react-router-dom";

export const loginAction = async ({ request }) => {
  const formData = await request.formData();
  const credentials = {
    email: formData.get('email'),
    password: formData.get('password')
  };

  console.log("Tentative de connexion avec:", credentials.email);

  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
      credentials: 'include'
    })

    // 2. Gestion des réponses
    const data = await response.json();

    if (!response.ok) {
      // Debug: afficher les détails de la réponse d'erreur
      console.log("Login failed - Status:", response.status);
      console.log("Login failed - Response data:", data);
      
      // Vérifier si l'erreur est due à un email non vérifié
      // Élargir les conditions de détection
      const isUnverifiedError = (
        (response.status === 403 || response.status === 401 || response.status === 400) &&
        (
          data.detail?.toLowerCase().includes('verify') ||
          data.detail?.toLowerCase().includes('vérifié') ||
          data.detail?.toLowerCase().includes('verification') ||
          data.detail?.toLowerCase().includes('not verified') ||
          data.detail?.toLowerCase().includes('unverified') ||
          data.message?.toLowerCase().includes('verify') ||
          data.message?.toLowerCase().includes('vérifié') ||
          data.message?.toLowerCase().includes('verification')
        )
      );
      
      if (isUnverifiedError) {
        console.log("Redirecting to send-email page for unverified user");
        return redirect(`/send-email?email=${encodeURIComponent(credentials.email)}`);
      }
      
      return {
        error: data.detail || data.message || "Échec de la connexion"
      };
    }

    // 3. Succès - Stockage du token
    localStorage.setItem('awesomeLeadsToken', data.access_token);
    if (data.refresh_token) {
      localStorage.setItem('awesomeLeadsRefreshToken', data.refresh_token);
    }

    console.log("Token stocké avec succès, redirection vers l'accueil (depuis login)..."); // Log amélioré

    // 4. Redirection vers la page d'accueil AVEC un paramètre
    return redirect('/?fromLogin=true'); // <-- MODIFICATION ICI

  } catch (error) {
    console.error("Erreur de connexion fetch:", error); // Log l'erreur réseau/fetch
    return {
      error: 'Erreur de connexion au serveur'
    };
  }
};