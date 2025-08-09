/**
 * @copyright 2025 isetsfax
 */

import { Form, useLoaderData, useNavigation } from "react-router-dom";
import { useSnackbar } from "../hooks/useSnackbar";
import { banner } from '../assets/assets';
import PageTitle from "../components/PageTitle";
import { Button } from "../components/Button";
import Logo from "../components/Logo";

const EmailVerified = () => {
    const { email } = useLoaderData();
    const navigation = useNavigation();
    const { showSnackbar } = useSnackbar();
    const isSubmitting = navigation.state === "submitting";

    return (
        <>
            <PageTitle title="Email vérifié" />

            <div className="relative w-screen h-dvh p-2 grid grid-cols-1 lg:grid-cols-[1fr,1.2fr] lg:gap-2">
                <div className="flex flex-col p-4">
                    <Logo classes="mb-auto mx-auto lg:mx-0" />

                    <div className="flex flex-col gap-2 max-w-[480px] w-full mx-auto">
                        <h2 className="text-displaySmall font-semibold text-light-onBackground dark:text-dark-onBackground text-center">
                            Vérification réussie !
                        </h2>
                        
                        <p className="text-bodyLarge text-center text-light-primary dark:text-dark-primary font-medium">
                            Votre email {email} a été confirmé.
                        </p>

                        <Form method="POST" className="mt-8">
                            <Button 
                                type="submit"
                                className="w-full btn filled primary"
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? 'Redirection...' : 'Se connecter maintenant'}
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
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                        </div>
                        
                        <h2 className="text-3xl font-bold text-white mb-4 text-center">
                            Compte vérifié
                        </h2>
                    </div>
                </div>
            </div>
        </>
    );
};

export default EmailVerified;