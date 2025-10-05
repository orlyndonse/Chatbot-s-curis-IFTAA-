---
sidebar_position: 5
title: Comprendre le Contexte Documentaire du Système
---

# Comprendre le Contexte Documentaire de l'Assistant RAG Fiqh

L'Assistant RAG Fiqh utilise les documents qui vous sont assignés par l'administrateur pour enrichir ses réponses et fournir des informations contextualisées spécifiquement à partir de ces ressources documentaires sur le Fiqh Maliki.

## Un Contexte Documentaire Privé et Sécurisé

* **Documents Privés par Utilisateur :** Chaque utilisateur a accès à ses propres documents assignés par l'administrateur. Les documents qui vous sont assignés sont accessibles dans toutes vos conversations et à vous seul.
* **Isolation Complète des Utilisateurs :** L'IA ne peut accéder qu'aux documents qui vous ont été **personnellement assignés** par l'administrateur. Elle n'a accès à aucun document d'autres utilisateurs.
* **Sécurité Renforcée :** Le système vérifie systématiquement que vous êtes bien autorisé à accéder aux documents avant de les utiliser.

![Diagramme simple illustrant une base de connaissance globale](/img/rag_context_diagram.svg)

## Qu'est-ce que cela signifie pour vos discussions ?

1. **Réponses Basées sur Vos Documents Assignés :** Quand vous posez une question, l'IA consulte exclusivement :
   - Les documents qui vous ont été assignés par l'administrateur
   - Les documents que vous avez marqués comme "actifs" pour vos conversations
   - L'historique de vos échanges précédents dans la conversation courante

2. **Contrôle Granulaire des Sources :**
   - Vous pouvez activer ou désactiver individuellement chaque document assigné pour le contexte RAG
   - Seuls les documents marqués comme "actifs" sont utilisés pour générer les réponses
   - Vous gardez un contrôle total sur quelles informations l'IA peut consulter

3. **Disponibilité Transversale :**
   - Les documents assignés sont disponibles dans toutes vos conversations
   - Vous n'avez pas besoin de re-téléverser des documents pour chaque nouvelle conversation
   - Vos documents assignés restent complètement privés et accessibles uniquement par vous

4. **Gestion de l'Historique Contextuel :**
   - L'IA prend en compte l'historique complet de la conversation courante
   - Les messages précédents dans la même conversation informent les nouvelles réponses
   - L'historique d'autres conversations n'influence pas les réponses

## Comment Gérer Vos Documents dans ce Contexte ?

* **Gestion Administrative :** Les documents sont assignés à votre compte par l'administrateur selon vos besoins spécifiques.
* **Activation Sélective :** Utilisez les boutons d'activation/désactivation pour contrôler précisément quels documents assignés l'IA doit consulter pour chaque réponse.
* **Disponibilité Continue :** Vos documents assignés sont disponibles dans toutes vos conversations sans besoin de les re-téléverser.
* **Confidentialité Assurée :** Vous pouvez utiliser vos documents assignés en toute sécurité, sachant qu'ils ne seront jamais accessibles à d'autres utilisateurs.

## Fonctionnalités de Sécurité

* **Vérification d'Assignation :** Le système vérifie que les documents vous sont bien assignés avant chaque opération.
* **Isolation des Données :** Aucun croisement de données entre utilisateurs différents.
* **Contrôle d'Accès :** Seuls les documents qui vous ont été explicitement assignés et que vous avez activés sont consultés.
* **Paths Sécurisés :** Les chemins de fichiers sont validés pour éviter tout accès non autorisé.

La [Liste des Documents Chargés](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341) dans votre interface vous montre tous les fichiers qui vous ont été assignés, avec la possibilité de les activer ou désactiver selon vos besoins.

---

Maintenant que vous comprenez comment le système de contexte documentaire privé fonctionne, passons à la section suivante : [Poser des Questions et Obtenir des Réponses](../rag-usage/formulating-questions.md).