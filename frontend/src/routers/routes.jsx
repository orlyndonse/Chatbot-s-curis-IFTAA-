import { createBrowserRouter } from "react-router-dom";
import App from '../App.jsx'
import Register from "../pages/Register.jsx";
import Login from "../pages/Login.jsx";
import ResetLink from "../pages/ResetLink.jsx";
import ResetPassword from "../pages/ResetPassword.jsx";
import SendEmail from "../pages/SendEmail.jsx";
import ResetPasswordSuccess from "../pages/ResetPasswordSuccess.jsx";
import VerifyEmailHandler from "../pages/VerifyEmailHandler.jsx";

/**
 * Actions
 */
import { registerAction } from "./actions/registerAction.js";
import { loginAction } from "./actions/loginAction.js";
import { resetLinkAction } from "./actions/resetLinkAction.js";
import { resetPasswordAction } from "./actions/resetPassword.js";
import { sendEmailAction } from "./actions/sendEmailAction.js";
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
import { resetPasswordSuccessReloader } from "./loaders/resetPasswordSuccessReloader.js";


const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        loader: appLoader,
        
    },
    {
        path: '/verify-email',
        element: <VerifyEmailHandler />, 
    },
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
        path: '/send-email', 
        element: <SendEmail />, 
        loader: sendEmailLoader, 
        action: sendEmailAction   
    },
    
    {
        path: "/resetpasswordsuccess",
        element: <ResetPasswordSuccess />,
        loader: resetPasswordSuccessReloader,
        action: resetPasswordSuccessAction
    },

]);
export default router;