/**
 * @copyright 2025 isetsfax
 */

import { Form, useActionData, useNavigation, useLoaderData } from "react-router-dom";
import { useEffect, useState } from "react";
import { useSnackbar } from "../hooks/useSnackbar";
import PageTitle from "../components/PageTitle";
import TextField from "../components/TextField";
import { Button } from "../components/Button";
import Logo from "../components/Logo";
import { CircularProgress } from "../components/Progress";

const ResetPassword = () => {
    const { token } = useLoaderData();
    const navigation = useNavigation();
    const actionData = useActionData();
    const { showSnackbar } = useSnackbar();
    const isSubmitting = navigation.state === "submitting";
    const [formData, setFormData] = useState({
        new_password: '',
        confirm_password: ''
    });

    useEffect(() => {
        if (actionData?.error) {
            showSnackbar({
                message: actionData.error,
                type: 'error',
                duration: 5000
            });
        }
    }, [actionData, showSnackbar]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const isFormValid = formData.new_password && 
                       formData.confirm_password && 
                       formData.new_password === formData.confirm_password;

    return (
        <>
            <PageTitle title="Réinitialiser votre mot de passe" />
            
            <div className="relative w-screen h-dvh p-2 grid grid-cols-1 lg:grid-cols-[1fr,1.2fr] lg:gap-2">
                {/* Partie Gauche - Contenu */}
                <div className="flex flex-col p-4">
                    <Logo classes="mb-auto mx-auto lg:mx-0" />
                    
                    <div className="flex flex-col gap-2 max-w-[480px] w-full mx-auto">
                        <div className="mb-4 mt-6">
                            <h2 className="text-titleLarge font-semibold text-light-onBackground dark:text-dark-onBackground">
                                Réinitialiser votre mot de passe
                            </h2>
                            
                            <p className="text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mt-2 mb-6">
                                Veuillez entrer votre nouveau mot de passe
                            </p>
                        </div>
                        
                        <Form method="post" className="space-y-4">
                            <input type="hidden" name="token" value={token} />
                            
                            <div className="space-y-4">
                                <TextField
                                    name="new_password"
                                    label="Nouveau mot de passe"
                                    type="password"
                                    required
                                    autoFocus
                                    onChange={handleInputChange}
                                    value={formData.new_password}
                                    minLength={8}
                                    helperText="Minimum 8 caractères"
                                />
                                
                                <TextField
                                    name="confirm_password"
                                    label="Confirmer le mot de passe"
                                    type="password"
                                    required
                                    minLength={8}
                                    onChange={handleInputChange}
                                    value={formData.confirm_password}
                                    helperText={formData.new_password !== formData.confirm_password ? 
                                        "Les mots de passe ne correspondent pas" : 
                                        "Minimum 8 caractères"}
                                />
                            </div>
                            
                            <Button 
                                type="submit" 
                                disabled={isSubmitting || !isFormValid}
                                className="w-full btn filled primary"
                            >
                                {isSubmitting ? (
                                    <span className="flex items-center justify-center">
                                        <CircularProgress size="small" className="mr-2" />
                                        En cours...
                                    </span>
                                ) : 'Valider'}
                            </Button>
                        </Form>
                        
                        <div className="mt-4 text-center">
                            <a 
                                href="/login" 
                                className="text-light-primary dark:text-dark-primary hover:underline text-bodyMedium"
                            >
                                Retour à la page de connexion
                            </a>
                        </div>
                    </div>
                    
                    <p className="mt-auto mx-auto text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-bodyMedium lg:mx-0">
                        &copy; 2025 isetsfax. Tous droits réservés.
                    </p>
                </div>
                
                <div className="hidden lg:block lg:relative lg:rounded-large bg-gradient-to-br from-gray-900 to-gray-800">
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-12">
                        <div className="w-24 h-24 rounded-full bg-light-surfaceContainerHigh dark:bg-gray-700 flex items-center justify-center mb-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-light-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                            </svg>
                        </div>
                        
                        <h2 className="text-3xl font-bold text-white mb-6 text-center">Sécurisez votre compte</h2>
                        
                        <div className="space-y-6 text-gray-300 text-center max-w-md">
                            <p>
                                Choisissez un mot de passe fort et unique pour protéger votre compte. Nous vous recommandons d'utiliser un mélange de lettres, chiffres et caractères spéciaux.
                            </p>
                            
                            <div className="bg-gray-800 bg-opacity-50 p-4 rounded-lg">
                                <div className="flex items-center mb-3">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-light-primary mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span className="font-medium">Conseil de sécurité</span>
                                </div>
                                <p className="text-sm">
                                    Évitez d'utiliser des informations personnelles comme votre date de naissance ou votre nom dans votre mot de passe.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default ResetPassword;