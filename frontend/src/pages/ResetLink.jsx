/**
 * @copyright 2025 isetsfax
 */

import { Form, Link, useActionData, useNavigation } from "react-router-dom";
import { useEffect, useState } from "react";
import { useSnackbar } from "../hooks/useSnackbar";
import { banner } from '../assets/assets';
import PageTitle from "../components/PageTitle";
import TextField from "../components/TextField";
import { Button } from "../components/Button";
import Logo from "../components/Logo";
import { CircularProgress } from "../components/Progress";

const ResetLink = () => {
    const actionData = useActionData();
    const { showSnackbar } = useSnackbar();
    const navigation = useNavigation();
    const isSubmitting = navigation.state === "submitting";
    const [email, setEmail] = useState('');

    useEffect(() => {
        // Amélioration de la gestion des erreurs
        if (actionData && !actionData.ok) {
            let errorMessage = "Une erreur est survenue lors de l'envoie";
            
            // S'assurer que nous avons une chaîne de caractères pour le message d'erreur
            if (typeof actionData.message === 'string') {
                errorMessage = actionData.message;
            } else if (actionData.message && typeof actionData.message.toString === 'function') {
                errorMessage = actionData.message.toString();
            }
            
            showSnackbar({ 
                message: errorMessage, 
                type: "error",
                timeOut: 8000 
            });
        }
    }, [actionData, showSnackbar]);

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const isFormValid = email.trim() !== '';

    return (
        <>
            <PageTitle title='Réinitialisation du mot de passe'/>

            <div className='relative w-screen h-dvh p-2 grid grid-cols-1 lg:grid-cols-[1fr,1.2fr] lg:gap-2'>
                {/* Partie Gauche - Formulaire */}
                <div className='flex flex-col p-4'>
                    <Logo classes='mb-auto mx-auto lg:mx-0'/>

                    <div className='flex flex-col gap-2 max-w-[480px] w-full mx-auto'>
                        <h2 className='text-displaySmall font-semibold text-light-onBackground dark:text-dark-onBackground text-center'>
                            Mot de passe oublié
                        </h2>
                        <p className='text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mt-1 mb-5 text-center px-2'>
                            Entrez votre adresse e-mail
                        </p>

                        <Form method='POST' className='grid grid-cols-1 gap-4'>
                            <TextField
                                type='email'
                                name='email'
                                label='Email'
                                placeholder='Email'
                                required
                                onChange={handleEmailChange}
                                value={email}
                            />
                            
                            <Button 
                                type='submit' 
                                disabled={isSubmitting || !isFormValid}
                                className="w-full btn filled primary"
                            >
                                {isSubmitting ? (
                                    <div className="flex items-center justify-center gap-2">
                                        <CircularProgress size="small" />
                                        <span>Envoi en cours...</span>
                                    </div>
                                ) : 'Envoyer le lien'}
                            </Button>
                        </Form>

                        <p className='text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-center mt-4'>
                            
                            <Link 
                                to='/login' 
                                className='text-labelLarge text-light-primary dark:text-dark-primary hover:underline'
                            >
                                Se connecter
                            </Link>
                        </p>
                    </div>

                    <p className='mt-auto mx-auto text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-bodyMedium lg:mx-0'>
                        &copy; 2025 isetsfax. Tous droits réservés.
                    </p>
                </div>

                <div className='hidden lg:block lg:relative lg:rounded-large bg-gradient-to-br from-gray-900 to-gray-800'>
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-12">
                        <div className="w-24 h-24 rounded-full bg-gray-800 flex items-center justify-center mb-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-light-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </div>
                        
                        <h2 className="text-3xl font-bold text-white mb-6 text-center">
                            Réinitialisez votre mot de passe en toute sécurité
                        </h2>
                        
                        <p className="text-gray-300 text-center max-w-md">
                            Nous vous enverrons un lien sécurisé pour créer un nouveau mot de passe.
                        </p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ResetLink;