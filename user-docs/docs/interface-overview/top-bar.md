---
sidebar_position: 5
title: La Barre Supérieure (Top Bar)
---

# La Barre Supérieure (Top Bar)

La barre supérieure (Top Bar), située tout en haut de l'interface de l'Assistant RAG Fiqh, contient des éléments de navigation importants, des options de personnalisation de l'affichage, et l'accès aux fonctionnalités de votre compte.

![Vue générale de la Barre Supérieure](/img/screenshot-topbar-new-overview.png)

## Éléments de la Barre Supérieure

La barre supérieure est organisée avec des éléments à gauche (principalement pour la navigation sur mobile) et des actions à droite.

### 1. Section Gauche (Navigation Mobile)

Ces éléments sont principalement visibles sur les écrans plus petits (smartphones, tablettes).

* **Icône Menu :**
    * **Affichage :** Représentée par une icône `menu` (☰).
    * **Visibilité :** Apparaît uniquement sur les écrans de petite et moyenne taille (`lg:hidden`).
    * **Fonction :** Cliquer sur cette icône permet d'afficher ou de masquer la [Barre Latérale (Sidebar)](./sidebar.md), qui contient votre historique de conversations et le bouton "Nouvelle Discussion".

* **Logo de l'Application :**
    * **Affichage :** Le logo de l'application est affiché à côté de l'icône Menu.
    * **Visibilité :** Également caché sur les grands écrans (`lg:hidden`).
    * **Fonction :** Élément visuel représentant l'identité de l'application.

    ![Section gauche mobile avec icône menu et logo](/img/screenshot-topbar-mobile-left-section.png)

### 2. Section Droite (Actions et Compte)

Ces éléments sont généralement visibles sur toutes les tailles d'écran et regroupent plusieurs fonctionnalités.

* **Bouton d'accès au Panneau de Contexte (Context Hub) :**
    * **Icône :** Représenté par l'icône `topic`.
    * **Titre/Infobulle :** "Toggle Context Hub".
    * **Fonction :** Ouvre ou ferme le panneau latéral droit appelé "Context Hub". Ce panneau vous permet de [gérer les documents](./document-management-pane.md) (téléverser, voir la liste, etc.) qui fournissent le contexte à l'IA pour la conversation active.

    ![Bouton Context Hub](/img/screenshot-topbar-Contexte.png)

* **Menu Utilisateur (Avatar) :**
    * **Affichage :** Votre avatar utilisateur est affiché. Il est généré à partir de votre nom d'utilisateur (`user?.username`) ou de votre prénom (`user?.first_name`).
    * **Fonction :** Cliquer sur votre avatar ouvre un menu déroulant avec plusieurs options.

    ![Avatar utilisateur](/img/screenshot-topbar-user-menu.png)

    **Menu Déroulant :**
    
    Le menu utilisateur contient les options suivantes :

    * **Langue (Language) :**
        * **Icône :** `language`
        * **Fonction :** Permet de basculer entre les langues disponibles dans l'application.
        
    * **Thème (Theme) :**
        * **Icône :** L'icône change dynamiquement - `dark_mode` pour passer au mode sombre si le thème actuel est clair, ou `light_mode` pour passer au mode clair si le thème actuel est sombre.
        * **Fonction :** Permet de basculer l'apparence de l'application entre un thème clair et un thème sombre. Votre préférence est sauvegardée dans le `localStorage` de votre navigateur.
        
    * **Documentation :**
        * **Icône :** `help_outline`
        * **Fonction :** Ouvre la documentation de l'application dans un nouvel onglet (localhost:3001/my-docs/).
        
    * **Se déconnecter (Logout) :**
        * **Icône :** `logout`
        * **Fonction :** Met fin à votre session. Les tokens d'authentification sont retirés du `localStorage`, et vous êtes redirigé vers la page de connexion (`/login`).

    ![Menu utilisateur déroulant](/img/placeholder-topbar-user-menu.png)

### 3. Gestion des Clics Extérieurs

Le menu utilisateur se ferme automatiquement lorsque vous cliquez en dehors de celui-ci, offrant une expérience utilisateur fluide et intuitive.

---

Vous avez maintenant exploré tous les éléments principaux de l'interface ! La section suivante, [Travailler avec les Conversations](./../conversations/starting-new.md), vous expliquera en détail comment gérer vos discussions.