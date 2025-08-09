/**
 * @copyright 2025 isetsfax
 */

export const emailVerifiedLoader = async ({ request }) => {
    const url = new URL(request.url);
    const email = url.searchParams.get('email');
    
    if (!email) {
        throw new Response("Email manquant", { status: 400 });
    }

    return { email };
};