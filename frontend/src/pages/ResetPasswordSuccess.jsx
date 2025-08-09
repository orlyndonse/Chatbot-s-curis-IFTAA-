/**
 * @copyright 2025 isetsfax
 */

import { Form, useActionData, useLoaderData, useNavigation } from "react-router-dom";
import { useEffect } from "react";
import { useSnackbar } from "../hooks/useSnackbar";
import { banner } from '../assets/assets';
import PageTitle from "../components/PageTitle";
import { Button } from "../components/Button";
import Logo from "../components/Logo";

const ResetPasswordSuccess = () => {
    const { email } = useLoaderData(); // Récupère l'email du loader
    const actionData = useActionData();
    const { showSnackbar } = useSnackbar();
    const navigation = useNavigation();
    const isSubmitting = navigation.state === "submitting";

    useEffect(() => {
        if (actionData?.message) {
            showSnackbar({
                message: actionData.message,
                type: actionData.ok ? "success" : "error",
                timeOut: 8000,
            });
        }
    }, [actionData, showSnackbar]);

    return (
        <>
            <PageTitle title="Réinitialisation du mot de passe" />

            <div className="relative w-screen h-dvh p-2 grid grid-cols-1 lg:grid-cols-[1fr,1.2fr] lg:gap-2">
                {/* Partie Gauche - Contenu */}
                <div className="flex flex-col p-4">
                    <Logo classes="mb-auto mx-auto lg:mx-0" />

                    <div className="flex flex-col gap-2 max-w-[480px] w-full mx-auto">

                        <h2 className="text-displaySmall font-semibold text-light-onBackground dark:text-dark-onBackground text-center">
                            Un lien de réinitialisation a été envoyé à :
                        </h2>
                        
                        <p className="text-bodyLarge text-center text-light-primary dark:text-dark-primary font-medium break-all px-4 py-2 bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh rounded-full">
                            {email || "example@example.com"}
                        </p>

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

                        <Form method="POST" className="mt-6">
                            <input type="hidden" name="email" value={email} />
                            <Button 
                                type="submit" 
                                disabled={isSubmitting}
                                className="w-full btn filled primary"
                            >
                                {isSubmitting ? 'Envoi en cours...' : 'Renvoyer l\'email'}
                            </Button>
                        </Form>
                    </div>

                    <p className="mt-auto mx-auto text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-bodyMedium lg:mx-0">
                        &copy; 2025 isetsfax. Tous droits réservés.
                    </p>
                </div>

                <div className="hidden lg:block lg:relative lg:rounded-large bg-gradient-to-br from-gray-900 to-gray-800">
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-12">
                        <div className="w-24 h-24 rounded-full bg-gray-800 flex items-center justify-center mb-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-light-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                        </div>
                        
                        <h2 className="text-3xl font-bold text-white mb-4 text-center">
                            Vérification en attente !
                        </h2>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ResetPasswordSuccess;