import { redirect } from 'react-router-dom';
import { fetchWithAuth } from '../../utils/fetchWithAuth'; // Helper for authenticated fetches

const appLoader = async ({ request }) => { // <-- Ajout de { request } ici pour accéder à l'URL
  console.log("AppLoader: Starting data fetch...");

  // <-- AJOUT : Récupérer les paramètres d'URL -->
  const url = new URL(request.url);
  const fromLogin = url.searchParams.get('fromLogin') === 'true';
  // <-- FIN AJOUT -->

  const token = localStorage.getItem("awesomeLeadsToken");
  if (!token) {
    console.log("AppLoader: No token found, redirecting to login.");
    return redirect('/login');
  }

  let user = null;
  let conversations = [];
  let initialMessages = []; // Messages for the first conversation

  try {
    // 1. Fetch user data
    console.log("AppLoader: Fetching user data...");
    user = await fetchWithAuth("/api/v1/auth/me");
    if (!user) {
      console.error("AppLoader: Failed to fetch user data (redirecting).");
      // fetchWithAuth devrait gérer la redirection, mais double sécurité
      return redirect('/login');
    }
    console.log("AppLoader: User data fetched:", user.email);

    // 2. Fetch conversations
    console.log("AppLoader: Fetching conversations...");
    conversations = await fetchWithAuth("/api/v1/conversations/");
    conversations = Array.isArray(conversations) ? conversations : [];
    console.log(`AppLoader: Found ${conversations.length} conversations.`);

    // 3. Fetch messages for the most recent conversation CONDITIONALLY
  
    if (conversations.length > 0 && !fromLogin) { // Ne charge les messages que si on ne vient PAS du login
      const latestConversationUid = conversations[0].uid;
      console.log(`AppLoader: Fetching messages for latest conversation ${latestConversationUid}...`);
      try {
          initialMessages = await fetchWithAuth(`/api/v1/conversations/${latestConversationUid}/messages`);
          initialMessages = Array.isArray(initialMessages) ? initialMessages : [];
          console.log(`AppLoader: Found ${initialMessages.length} initial messages.`);
      } catch (messageError) {
          console.error(`AppLoader: Error fetching initial messages for ${latestConversationUid}:`, messageError);
          initialMessages = [];
      }
    } else if (fromLogin) {
        console.log("AppLoader: Coming from login, skipping initial message fetch.");
        initialMessages = []; // Assurer que c'est vide si on vient du login
    } else {
        console.log("AppLoader: No conversations found or error fetching, skipping initial message fetch.");
        initialMessages = []; // Assurer que c'est vide s'il n'y a pas de conversations
    }

    console.log("AppLoader: Data loading complete.");

    // Retourner les données nécessaires pour App.jsx
    return {
      user: { // S'assurer de ne retourner que les données nécessaires/sécurisées
        uid: user.uid,
        first_name: user.first_name,
        username: user.username,
        email: user.email,
      },
      conversations,
      initialMessages // Sera un tableau vide si fromLogin=true ou si pas de conversations/erreur
    };

  } catch (error) {
    if (error instanceof Response && error.redirect) {
         throw error; // Laisser passer les redirections
    }
    console.error("AppLoader critical error:", error);
    localStorage.removeItem("awesomeLeadsToken");
    localStorage.removeItem("awesomeLeadsRefreshToken");
    return redirect('/login'); // Redirection de sécurité en cas d'erreur grave
  }
};

export default appLoader;