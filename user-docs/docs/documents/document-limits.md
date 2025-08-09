---
sidebar_position: 6
title: Comprendre les Limites des Documents
---

# Comprendre les Limites des Documents et la Taille du Contexte

Pour assurer un fonctionnement optimal de l'Assistant RAG Fiqh, il est utile de connaître certaines limites potentielles concernant les documents que vous téléversez et comment la "taille du contexte" est gérée.

## Indicateur de "Taille du Contexte" (Point 6.6.1)

Dans le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md), vous remarquerez un indicateur de "Taille du contexte".

* **Affichage :** Il se présente souvent sous la forme d'une barre de progression et d'un texte. Ce texte ressemblera à quelque chose comme : "**Taille du contexte : _X_ Ko / _Y_ Ko**" (par exemple, "Taille du contexte : 25 Ko / 100 Ko").
* **Signification :**
    * **Taille Actuelle :** La première valeur (par exemple, "25 Ko") représente la taille combinée approximative des documents que vous avez actuellement chargés dans la discussion active.
    * **Taille Maximale Recommandée/Supportée :** La seconde valeur (par exemple, "100 Ko") indique une limite indicative ou maximale de la quantité de données textuelles que le système est optimisé pour traiter efficacement pour une seule discussion. Dans votre application, cette valeur est actuellement fixée à titre d'exemple à 100KB (ce qui correspond à `maxContextSize = 100000` dans le code de l'interface).
    
    ![Indicateur de Taille du Contexte dans le panneau des documents](/img/screenshot-document-context-size.png) 

## Pourquoi y a-t-il des Limites ?

Les systèmes d'intelligence artificielle, en particulier ceux qui analysent du texte (comme les modèles RAG), fonctionnent de manière optimale avec une quantité gérable d'informations contextuelles :

* **Performance :** Traiter de très grandes quantités de texte peut ralentir le temps de réponse de l'IA.
* **Pertinence :** Un contexte trop vaste et non ciblé peut parfois "noyer" l'information la plus pertinente, rendant plus difficile pour l'IA de trouver la meilleure réponse.
* **Coûts et Ressources :** L'analyse de grandes quantités de texte consomme des ressources informatiques.

## Limites Actuelles (Exemples)

Bien que le système puisse évoluer, voici les types de limites que vous pourriez rencontrer (basé sur l'indicateur actuel) :

* **Taille Totale du Contexte par Discussion :**
    * L'indicateur "Taille du contexte" vous donne une idée de cette limite. Votre application affiche actuellement une limite indicative de **100 Ko** par discussion (basée sur la valeur `maxContextSize` dans l'interface).
    * Essayer de dépasser cette limite pourrait ne pas être optimal, mais l'interface vous montre votre utilisation actuelle.

* **Taille Maximale par Fichier / Nombre Maximum de Fichiers :**
    * **Actuellement, l'interface utilisateur n'impose pas de limites strictes visibles par l'utilisateur sur la taille de chaque fichier individuel ou sur le nombre total de fichiers, *au-delà de l'impact sur la limite globale de la taille du contexte*.**
    * Cependant, il est toujours de bonne pratique de téléverser des fichiers de taille raisonnable et pertinents pour votre sujet de discussion. Des fichiers extrêmement volumineux (par exemple, des centaines de Mo) pourraient être lents à téléverser ou à traiter par le backend.

## Que Faire si Vous Approchez des Limites ?

* **Soyez Sélectif :** Choisissez les documents les plus pertinents pour votre question ou sujet de discussion actuel.
* **Divisez les Sujets :** Si vous avez beaucoup de documents sur des sujets très différents, envisagez de [créer des discussions séparées](../conversations/starting-new.md) pour chaque sujet, chacune avec son propre ensemble de documents contextuels.
* **Supprimez les Documents Non Essentiels :** Si vous avez téléversé des documents qui ne sont plus nécessaires pour la discussion en cours, vous pouvez les [retirer de la liste](./deleting-documents.md) pour libérer de l'espace dans le contexte.

En gardant un œil sur l'indicateur de taille du contexte et en étant judicieux dans le choix des documents que vous téléversez, vous contribuerez à une expérience plus fluide et à des réponses plus ciblées de l'IA.

---

Ceci conclut notre section sur la gestion des documents. La section suivante portera sur la [Gestion de Votre Compte Utilisateur](../account/logging-out.md).