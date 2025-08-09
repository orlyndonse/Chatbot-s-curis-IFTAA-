/**
 * @copyright 2025 isetsfax
 */

import { Form, Link, useNavigation, useActionData, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useSnackbar } from "../hooks/useSnackbar";
import { banner } from '../assets/assets';
import PageTitle from "../components/PageTitle";
import TextField from "../components/TextField";
import { Button } from "../components/Button";
import Logo from "../components/Logo";
import { CircularProgress } from "../components/Progress";

const Login = () => {
  const navigation = useNavigation();
  const actionData = useActionData();
  const [searchParams] = useSearchParams();
  const { showSnackbar } = useSnackbar();
  const isSubmitting = navigation.state === 'submitting';
  const [formData, setFormData] = useState({ email: '', password: '' });
  
  // Récupérer le paramètre reset de l'URL si présent
  const resetSuccess = searchParams.get('reset');

  useEffect(() => {
    // Afficher les erreurs de login
    if (actionData?.error) {
      showSnackbar({
        message: actionData.error,
        type: 'error',
        duration: 5000
      });
    }
    
    // Afficher un message de succès si l'utilisateur vient de réinitialiser son mot de passe
    if (resetSuccess === 'success') {
      showSnackbar({
        message: "Mot de passe réinitialisé avec succès! Vous pouvez maintenant vous connecter.",
        type: 'success',
        duration: 5000
      });
    }
  }, [actionData, showSnackbar, resetSuccess]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const isFormValid = formData.email && formData.password;

  return (
    <>
      <PageTitle title='Se connecter'/>
      <div className='relative w-screen h-dvh p-2 grid grid-cols-1 lg:grid-cols-[1fr,1.2fr] lg:gap-2'>
        {/* Partie Gauche - Formulaire */}
        <div className='flex flex-col p-4'>
          <Logo classes='mb-auto mx-auto lg:mx-0'/>
          
          <div className='flex flex-col gap-2 max-w-[480px] w-full mx-auto'>
            <h2 className='text-displaySmall font-semibold text-light-onBackground dark:text-dark-onBackground text-center'>
              Bienvenue à notre application
            </h2>
            <p className='text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mt-1 mb-5 text-center px-2'>
              Veuillez vous identifier!
            </p>

            <Form method='POST' className='grid grid-cols-1 gap-4'>
              <TextField
                type='email'
                name='email'
                label='Email'
                placeholder='Email'
                required={true} 
                autoFocus={true}
                onChange={handleInputChange}
                value={formData.email}
              />
              <TextField
                type='password'
                name='password'
                label='Mot de passe'
                placeholder='Entrez votre mot de passe'
                required
                minLength={8}
                helperText="Minimum 8 caractères"
                onChange={handleInputChange}
                value={formData.password}
              />
              
              <div className='text-right'>
                <Link
                  to='/reset-link'
                  className='text-labelLarge text-light-primary dark:text-dark-primary hover:underline inline-block'
                >
                  Mot de passe oublié?
                </Link>
              </div>
              
              <Button 
                type='submit'
                disabled={isSubmitting || !isFormValid}
                className="w-full btn filled primary"
              >
                {isSubmitting ? (
                  <div className="flex items-center justify-center gap-2">
                    <CircularProgress size="small" />
                    <span>Connexion...</span>
                  </div>
                ) : 'Se connecter'}
              </Button>
            </Form>

            <p className='text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-center mt-4'>
              Vous n'avez pas de compte ?{' '}
              <Link
                to='/register'
                className='text-labelLarge text-light-primary dark:text-dark-primary hover:underline inline-block'
              >
                S'enregistrer
              </Link>
            </p>
          </div>

          <div className='mt-auto mx-auto lg:mx-0'>
            <a 
              href="http://localhost:3001/my-docs/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-light-surfaceVariant dark:bg-dark-surfaceVariant text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant hover:bg-light-primary hover:text-light-onPrimary dark:hover:bg-dark-primary dark:hover:text-dark-onPrimary transition-all duration-200 text-bodyMedium font-medium mb-3 hover:shadow-md transform hover:scale-105"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Documentation
            </a>
            <p className='text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-bodyMedium'>
              &copy; 2025 isetsfax. Tous droits réservés.
            </p>
          </div>
        </div>

        <div className='hidden lg:block lg:relative lg:rounded-large bg-gradient-to-br from-gray-900 to-gray-800'>
          <div className="absolute inset-0 flex flex-col items-center justify-center p-12">
            <div className="w-24 h-24 rounded-full bg-gray-800 flex items-center justify-center mb-8">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-light-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </div>
            
            <h2 className="text-3xl font-bold text-white mb-6 text-center">Connectez-vous à votre espace personnel</h2>
            
          </div>
        </div>
      </div>
    </>
  );
};

export default Login;