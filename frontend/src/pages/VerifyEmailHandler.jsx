// src/pages/VerifyEmailHandler.jsx
import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { useSnackbar } from '../hooks/useSnackbar';
import PageTitle from '../components/PageTitle';
import Logo from '../components/Logo';
import { CircularProgress } from '../components/Progress';
import { Button } from '../components/Button';

const VerifyEmailHandler = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { showSnackbar } = useSnackbar();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isVerified, setIsVerified] = useState(false);

  const token = searchParams.get('token');

  useEffect(() => {
    // Exécute la vérification seulement si un token est présent
    if (!token) {
      setError("Token de vérification manquant dans l'URL.");
      setIsLoading(false);
      showSnackbar({ message: "Lien de vérification invalide ou manquant.", type: 'error', duration: 6000 });
      return;
    }

    const verifyTokenOnBackend = async () => {
      setIsLoading(true);
      setError(null);
      setIsVerified(false); // Reset verification state

      try {
        // Adaptez l'URL si votre proxy Vite n'est pas configuré pour /api/v1/auth
        const response = await fetch("http://localhost:8000/api/v1/auth/verify-email", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          // Le backend attend un objet JSON { "token": "..." }
          body: JSON.stringify({ token: token }),
        });

        const data = await response.json();

        if (!response.ok) {
          // Utilise le message d'erreur du backend s'il existe
          throw new Error(data.detail || `Erreur ${response.status}: Échec de la vérification.`);
        }

        // Succès !
        setIsVerified(true);
        showSnackbar({ message: "Email vérifié avec succès ! Vous pouvez maintenant vous connecter.", type: 'success', duration: 6000 });
        // Optionnel : Rediriger automatiquement vers login après un délai
        // const timer = setTimeout(() => navigate('/login'), 4000);
        // return () => clearTimeout(timer); // Nettoyage du timer

      } catch (err) {
        console.error("Verification Error:", err);
        setError(err.message || "Une erreur inconnue est survenue.");
        showSnackbar({ message: err.message || "Une erreur inconnue est survenue.", type: 'error', duration: 6000 });
      } finally {
        setIsLoading(false);
      }
    };

    verifyTokenOnBackend();
    // Dépendances : exécuter seulement si le token change (ne devrait pas arriver mais bonne pratique)
  }, [token, navigate, showSnackbar]);

  // --- Affichage ---
  let pageContent;
  if (isLoading) {
    pageContent = (
      <>
        <CircularProgress size="large" className="mb-4" />
        <p className="text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">Vérification en cours...</p>
      </>
    );
  } else if (isVerified) {
    pageContent = (
      <>
         <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 dark:bg-green-900 rounded-full mb-6 text-green-600 dark:text-green-400">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
         </div>
        <h2 className="text-headlineMedium font-semibold text-light-onBackground dark:text-dark-onBackground mb-3">
          Email Vérifié !
        </h2>
        <p className="text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-6 max-w-md">
          Votre adresse email a été confirmée avec succès. Vous êtes prêt à vous connecter.
        </p>
        <Button onClick={() => navigate('/login')} className="btn filled primary mt-4">
          Se Connecter Maintenant
        </Button>
      </>
    );
  } else { // Cas d'erreur
    pageContent = (
      <>
         <div className="inline-flex items-center justify-center w-20 h-20 bg-red-100 dark:bg-red-900 rounded-full mb-6 text-red-600 dark:text-red-400">
             <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
             </svg>
         </div>
        <h2 className="text-headlineMedium font-semibold text-light-onBackground dark:text-dark-onBackground mb-3">
          Erreur de Vérification
        </h2>
        <p className="text-bodyLarge text-light-error dark:text-dark-error mb-6 max-w-md">
          {error || "Impossible de vérifier l'email. Le lien est peut-être invalide ou expiré."}
        </p>
        <p className="text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
           <Link to="/login" className="text-light-primary dark:text-dark-primary hover:underline">Retour à la page de connexion</Link>
           {/* Vous pourriez ajouter un bouton pour renvoyer l'email ici si nécessaire */}
        </p>
      </>
    );
  }

  return (
    <>
      <PageTitle title={isLoading ? "Vérification..." : (isVerified ? "Email Vérifié" : "Erreur Vérification")} />
      <div className="flex flex-col items-center justify-center min-h-dvh p-4 text-center bg-light-background dark:bg-dark-background">
        <Logo classes="mb-12" />
        {pageContent}
        <p className="absolute bottom-4 text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
           &copy; 2025 isetsfax. Tous droits réservés.
        </p>
      </div>
    </>
  );
};

export default VerifyEmailHandler;