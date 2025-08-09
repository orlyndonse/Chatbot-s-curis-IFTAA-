import { createBrowserRouter } from "react-router-dom";
import App from '../App.jsx'
import Register from "../pages/Register.jsx";
import Login from "../pages/Login.jsx";
import ResetLink from "../pages/ResetLink.jsx";
import ResetPassword from "../pages/ResetPassword.jsx";
import SendEmail from "../pages/SendEmail.jsx";
// import EmailVerified from "../pages/EmailVerified"; // On n'utilise plus l'ancien directement ici
import ResetPasswordSuccess from "../pages/ResetPasswordSuccess.jsx";
import VerifyEmailHandler from "../pages/VerifyEmailHandler.jsx"; // <-- Importer le nouveau composant

/**
 * Actions
 */
import { registerAction } from "./actions/registerAction.js";
import { loginAction } from "./actions/loginAction.js";
import { resetLinkAction } from "./actions/resetLinkAction.js";
import { resetPasswordAction } from "./actions/resetPassword.js";
// import appAction from "./actions/appAction.js"; // Supprimé comme discuté précédemment
import { sendEmailAction } from "./actions/sendEmailAction.js";
// import { emailVerifiedAction } from "./actions/EmailVerifiedAction.js"; // Probablement plus nécessaire
import { resetPasswordSuccessAction } from "./actions/resetPasswordSuccessAction.js";

/**
* Loaders
*/
import { registerLoader } from './loaders/registerLoader.js';
import { sendEmailLoader } from './loaders/sendEmailLoader.js';
import { loginLoader } from './loaders/loginLoader.js';
import { resetLinkReloader }   from './loaders/resetLinkLoader.js';
import { resetPasswordLoader } from "./loaders/resetPasswordLoader.js";
import appLoader from './loaders/appLoader.js';
// import { emailVerifiedLoader } from "./loaders/EmailVerifiedLoader.js"; // Probablement plus nécessaire
import { resetPasswordSuccessReloader } from "./loaders/resetPasswordSuccessReloader.js";


const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        loader: appLoader,
        // action: appAction // Supprimé
    },
    // --- Nouvelle Route pour la Vérification ---
    {
        path: '/verify-email', // <-- Route activée par le lien email
        element: <VerifyEmailHandler />, // <-- Utilise le nouveau composant
        // Pas de loader/action ici, le composant gère l'appel API
    },
    // --- Routes Auth existantes ---
    {
        path: '/register',
        element: <Register />,
        loader: registerLoader,
        action: registerAction,
    },
    {
        path: '/login',
        element: <Login />,
        action: loginAction,
        loader: loginLoader,
      },
    {
        path: '/reset-link',
        element: <ResetLink />,
        loader: resetLinkReloader,
        action: resetLinkAction,
    },
    {
        path: '/reset-password/',
        element: <ResetPassword />,
        loader: resetPasswordLoader,
        action: resetPasswordAction,
    },
    {
        path: '/send-email', // Page "Veuillez vérifier votre email"
        element: <SendEmail />, // Garder ce composant tel quel
        loader: sendEmailLoader, // Garder
        action: sendEmailAction   // Garder (pour renvoyer l'email)
    },
    // { // L'ancienne route /email-verified devient redondante
    //     path: "/email-verified",
    //     element: <EmailVerified />,
    //     loader: emailVerifiedLoader,
    //     action: emailVerifiedAction
    // },
    {
        path: "/resetpasswordsuccess",
        element: <ResetPasswordSuccess />,
        loader: resetPasswordSuccessReloader,
        action: resetPasswordSuccessAction
    },

]);
export default router;