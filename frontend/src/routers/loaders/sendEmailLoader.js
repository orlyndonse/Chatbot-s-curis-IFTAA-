/**
 * @copyright 2025 isetsfax
 */

import { redirect } from "react-router-dom";

export const sendEmailLoader = async ({ request }) => {
    const url = new URL(request.url);
    const email = url.searchParams.get('email');

    // 1. Redirige si l'email est manquant ou invalide
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return redirect('/register?error=invalid_email');
    }

    return { email }; // Passe l'email au composant via `useLoaderData()`
};