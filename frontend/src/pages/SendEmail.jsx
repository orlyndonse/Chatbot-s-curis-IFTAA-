/**
 * @copyright 2025 isetsfax
 */

import { Form, useActionData, useLoaderData, useNavigation } from "react-router-dom";
import { useEffect } from "react";
import { useSnackbar } from "../hooks/useSnackbar";
import PageTitle from "../components/PageTitle";
import { Button } from "../components/Button";
import Logo from "../components/Logo";

const SendEmail = () => {
    const { email } = useLoaderData();
    const actionData = useActionData();
    const { showSnackbar } = useSnackbar();
    const navigation = useNavigation();
    const isSubmitting = navigation.state === "submitting";

    useEffect(() => {
        if (actionData?.message) {
            showSnackbar({
                message: actionData.message,
                type: actionData.ok ? "success" : "error",
                duration: 8000,
            });
        }
    }, [actionData, showSnackbar]);

    return (
        <>
            <PageTitle title="Vérification requise" />
            
            <div className="relative w-screen h-dvh p-2 grid grid-cols-1 lg:grid-cols-[1fr,1.2fr] lg:gap-2">
                {/* Partie Gauche - Contenu */}
                <div className="flex flex-col p-4">
                    <Logo classes="mb-auto mx-auto lg:mx-0" />
                    
                    <div className="flex flex-col gap-2 max-w-[480px] w-full mx-auto my-auto">
                        {/* Section d'en-tête */}
                        <div className="text-center mb-8">
                            <div className="inline-flex items-center justify-center w-20 h-20 bg-light-primaryContainer dark:bg-dark-primaryContainer rounded-full mb-6">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-light-primary dark:text-dark-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                </svg>
                            </div>
                            
                            <h2 className="text-headlineMedium font-semibold text-light-onBackground dark:text-dark-onBackground mb-3">
                                Vérification requise
                            </h2>
                            
                            <p className="text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
                                Nous avons envoyé un lien de vérification à :
                            </p>
                        </div>
                        
                        {/* Email display */}
                        <div className="bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh rounded-xl p-5 mb-6 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-light-primary dark:text-dark-primary mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                            <p className="text-bodyLarge text-light-primary dark:text-dark-primary font-medium break-all">
                                {email || "example@example.com"}
                            </p>
                        </div>

                        {/* Message important */}
                        <div className="bg-light-surfaceContainerLow dark:bg-dark-surfaceContainerLow rounded-xl p-4 mb-8">
                            <div className="flex items-start">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-light-tertiary dark:text-dark-tertiary mr-2 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                                <div>
                                    <p className="text-bodyMedium font-medium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                                        Vérifiez vos spams
                                    </p>
                                    <p className="text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
                                        Le lien expire dans 24 heures. Si vous ne le trouvez pas dans votre boîte de réception, vérifiez votre dossier de courriers indésirables.
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Bouton d'action */}
                        <Form method="POST" className="w-full">
                            <input type="hidden" name="email" value={email} />
                            <Button 
                                type="submit" 
                                disabled={isSubmitting}
                                className="w-full btn filled primary"
                            >
                                {isSubmitting ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <span className="animate-spin">⟳</span>
                                        Envoi en cours...
                                    </span>
                                ) : 'Renvoyer l\'email'}
                            </Button>
                        </Form>

                        <div className="text-center mt-6">
                            <a 
                                href="/login" 
                                className="text-labelLarge text-light-primary dark:text-dark-primary hover:underline"
                            >
                                Retour à la connexion
                            </a>
                        </div>
                    </div>

                    <p className="mt-auto mx-auto text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-bodyMedium lg:mx-0">
                        &copy; 2025 isetsfax. Tous droits réservés.
                    </p>
                </div>

                {/* Partie Droite - Style unifié */}
                <div className="hidden lg:block lg:relative lg:rounded-large bg-gradient-to-br from-gray-900 to-gray-800">
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-12">
                        <div className="w-24 h-24 rounded-full bg-gray-800 flex items-center justify-center mb-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-light-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19M3 19a2 2 0 002 2h14a2 2 0 002-2M3 19l6.75-4.5M21 19l-6.75-4.5M3 10l6.75 4.5M21 10l-6.75 4.5m0 0l-1.14.76a2 2 0 01-2.22 0l-1.14-.76" />
                            </svg>
                        </div>
                        
                        <h2 className="text-3xl font-bold text-white mb-4 text-center">
                            Vérification en attente
                        </h2>
                        
                        <p className="text-gray-300 text-center max-w-md">
                            Pour accéder à votre compte, veuillez confirmer votre adresse email en cliquant sur le lien que nous vous avons envoyé.
                        </p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default SendEmail;