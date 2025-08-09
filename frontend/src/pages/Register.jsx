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

const Register = () => {
    const actionData = useActionData();
    const { showSnackbar } = useSnackbar();
    const navigation = useNavigation();
    const isSubmitting = navigation.state === "submitting";
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: ''
    });

    useEffect(() => {
        // Amélioration de la gestion des erreurs
        if (actionData && !actionData.ok) {
            let errorMessage = "Une erreur est survenue lors de l'inscription";
            
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

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const isFormValid = formData.username && formData.email && 
                       formData.first_name && formData.last_name && 
                       formData.password;

    return (
        <>
            <PageTitle title='Créer un compte'/>

            <div className='relative w-screen h-dvh p-2 grid grid-cols-1 lg:grid-cols-[1fr,1.2fr] lg:gap-2'>
                {/* Partie Gauche - Formulaire */}
                <div className='flex flex-col p-4'>
                    <Logo classes='mb-auto mx-auto lg:mx-0'/>

                    <div className='flex flex-col gap-2 max-w-[480px] w-full mx-auto'>
                        <h2 className='text-displaySmall font-semibold text-light-onBackground dark:text-dark-onBackground text-center'>
                            Créer un compte
                        </h2>
                        <p className='text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mt-1 mb-5 text-center px-2'>
                            Inscrivez-vous aujourd'hui
                        </p>

                        <Form method='POST' className='grid grid-cols-1 gap-4'>
                            <TextField
                                type='text'
                                name='username'
                                label='Nom d&apos;utilisateur'
                                placeholder='Nom d&apos;utilisateur'
                                required
                                autoFocus
                                onChange={handleInputChange}
                                value={formData.username}
                            />
                            <TextField
                                type='email'
                                name='email'
                                label='Email'
                                placeholder='Email'
                                required
                                onChange={handleInputChange}
                                value={formData.email}
                            />
                            <TextField
                                type='text'
                                name='first_name'
                                label='Prénom'
                                placeholder='Prénom'
                                required
                                onChange={handleInputChange}
                                value={formData.first_name}
                            />
                            <TextField
                                type='text'
                                name='last_name'
                                label='Nom'
                                placeholder='Nom'
                                required
                                onChange={handleInputChange}
                                value={formData.last_name}
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
                            
                            <Button 
                                type='submit' 
                                disabled={isSubmitting || !isFormValid}
                                className="w-full btn filled primary"
                            >
                                {isSubmitting ? (
                                    <div className="flex items-center justify-center gap-2">
                                        <CircularProgress size="small" />
                                        <span>Inscription en cours...</span>
                                    </div>
                                ) : 'Créer un compte'}
                            </Button>
                        </Form>

                        <p className='text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-center mt-4'>
                            Vous avez déjà un compte ?{' '}
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

                <div className='hidden lg:block lg:relative lg:rounded-large bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900'>
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-12">
                        <div className="w-24 h-24 rounded-full bg-gray-800 flex items-center justify-center mb-8">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-light-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                            </svg>
                        </div>
                        
                        <h2 className="text-3xl font-bold text-white mb-6 text-center">Rejoignez notre communauté</h2>
                        

                            
                            <div className="bg-gray-800 bg-opacity-50 p-4 rounded-lg">
                                <div className="flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <p className="text-gray-300 text-sm">
                                        En créant un compte, vous acceptez nos conditions d'utilisation et notre politique de confidentialité.
                                    </p>
                                </div>
                            </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Register;