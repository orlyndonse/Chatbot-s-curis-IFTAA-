/**
 * @copyright 2025 isetsfax
 */

import { redirect } from "react-router-dom";

export const emailVerifiedAction = async () => {
    // Ici vous pourrez ajouter une logique supplémentaire si nécessaire
    // comme marquer le compte comme actif dans la base de données
    return redirect("/login");
};