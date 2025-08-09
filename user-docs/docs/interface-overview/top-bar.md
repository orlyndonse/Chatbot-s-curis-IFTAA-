---
sidebar_position: 5
title: La Barre Supérieure (Top Bar)
---

# La Barre Supérieure (Top Bar)

La barre supérieure (Top Bar), située tout en haut de l'interface de l'Assistant RAG Fiqh, contient des éléments de navigation importants, des options de personnalisation de l'affichage, et l'accès aux fonctionnalités de votre compte.

![Vue générale de la Barre Supérieure avec nouveaux éléments](/img/screenshot-topbar-new-overview.png)

## Éléments de la Barre Supérieure

La barre supérieure est organisée avec des éléments à gauche (principalement pour la navigation sur mobile) et des actions à droite.

### 1. Section Gauche (Navigation Mobile)

Ces éléments sont principalement visibles sur les écrans plus petits (smartphones, tablettes).

* **Icône Menu :**
    * **Affichage :** Représentée par une icône `menu` (☰).
    * **Visibilité :** Apparaît sur les écrans de petite et moyenne taille.
    * **Fonction :** Cliquer sur cette icône permet d'afficher ou de masquer la [Barre Latérale (Sidebar)](./sidebar.md), qui contient votre historique de conversations et le bouton "Nouvelle Discussion".

    ![Icône Menu et Logo sur mobile/tablette](/img/screenshot-topbar-mobile-left-section.png)
* **Logo de l'Application :**
    * **Affichage :** Le logo de l'application est affiché à côté de l'icône Menu.
    * **Visibilité :** Également caché sur les grands écrans (`lg:hidden`).
    * **Fonction :** Cliquer sur le logo vous redirige vers la page d'accueil de l'application (chemin "/").


### 2. Section Droite (Actions et Compte)

Ces éléments sont généralement visibles sur toutes les tailles d'écran et regroupent plusieurs fonctionnalités.

* **Bouton de Thème (Clair/Sombre) :**
    * **Icône :** L'icône change dynamiquement pour refléter le passage au mode opposé : `dark_mode` (passer au mode sombre) si le thème actuel est clair, ou `light_mode` (passer au mode clair) si le thème actuel est sombre.
    * **Titre/Infobulle :** Indique l'action (par exemple, "Switch to dark mode" ou "Switch to light mode").
    * **Fonction :** Permet de basculer l'apparence de l'application entre un thème clair et un thème sombre. Votre préférence est sauvegardée dans le `localStorage` de votre navigateur.

    ![Icône Thème](/img/screenshot-topbar-Theme.png)

* **Bouton d'accès au Panneau de Contexte (Context Hub) :**
    * **Icône :** Représenté par l'icône `topic`.
    * **Titre/Infobulle :** "Toggle Context Hub".
    * **Fonction :** Ouvre ou ferme le panneau latéral droit appelé "Context Hub". Ce panneau vous permet de [gérer les documents](./document-management-pane.md) (téléverser, voir la liste, etc.) qui fournissent le contexte à l'IA pour la conversation active.


    ![Icône Contexte](/img/screenshot-topbar-Contexte.png)

* **Menu Utilisateur (Avatar) :**
    * **Affichage :** Votre avatar utilisateur est affiché. Il est généré à partir de votre nom d'utilisateur (`user?.username`) ou de votre prénom (`user?.first_name`).
    * **Fonction :** Cliquer sur votre avatar ouvre un petit menu déroulant.
    * **Menu Déroulant :**
        * **Option "Se déconnecter" (Logout) :**
            * **Accès :** Unique option dans le menu déroulant actuel.
            * **Fonction :** Cliquer sur "**Se déconnecter**" mettra fin à votre session. Les tokens d'authentification sont retirés du `localStorage`, et vous êtes redirigé vers la page de connexion (`/login`).

    ![Boutons d'action et menu utilisateur](/img/screenshot-topbar-right-section.png)

---

Vous avez maintenant exploré tous les éléments principaux de l'interface ! La section suivante, [Travailler avec les Conversations](./../conversations/starting-new.md), vous expliquera en détail comment gérer vos discussions.