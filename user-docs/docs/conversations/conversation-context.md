---
sidebar_position: 5
title: Comprendre le Contexte Documentaire du Système
---

# Comprendre le Contexte Documentaire de l'Assistant RAG Fiqh

L'Assistant RAG Fiqh utilise les documents que vous téléversez pour enrichir ses réponses et fournir des informations contextualisées spécifiquement à partir de vos propres ressources documentaires sur le Fiqh Maliki.

## Un Contexte Documentaire Privé et Sécurisé

* **Documents Privés par Conversation :** Chaque conversation dispose de son propre contexte documentaire. Les documents que vous téléversez dans une conversation spécifique ne sont accessibles qu'à cette conversation et à vous seul.
* **Isolation Complète des Utilisateurs :** L'IA ne peut accéder qu'aux documents que **vous** avez personnellement téléversés dans la conversation active. Elle n'a accès à aucun document d'autres utilisateurs ou d'autres conversations.
* **Sécurité Renforcée :** Le système vérifie systématiquement que vous êtes bien le propriétaire de la conversation et des documents avant d'y accéder.

![Diagramme simple illustrant une base de connaissance globale](/img/rag_context_diagram.svg)

## Qu'est-ce que cela signifie pour vos discussions ?

1. **Réponses Basées sur Vos Documents Uniquement :** Quand vous posez une question, l'IA consulte exclusivement :
   - Les documents que vous avez téléversés dans cette conversation spécifique
   - Les documents que vous avez marqués comme "actifs" pour cette conversation
   - L'historique de vos échanges précédents dans cette même conversation

2. **Contrôle Granulaire des Sources :**
   - Vous pouvez activer ou désactiver individuellement chaque document pour le contexte RAG
   - Seuls les documents marqués comme "actifs" sont utilisés pour générer les réponses
   - Vous gardez un contrôle total sur quelles informations l'IA peut consulter

3. **Isolation Stricte des Conversations :**
   - Les documents téléversés dans "Discussion A" ne sont pas accessibles dans "Discussion B"
   - Chaque conversation maintient son propre contexte documentaire indépendant
   - Vos conversations et documents restent complètement privés

4. **Gestion de l'Historique Contextuel :**
   - L'IA prend en compte l'historique complet de la conversation courante
   - Les messages précédents dans la même conversation informent les nouvelles réponses
   - L'historique d'autres conversations n'influence pas les réponses

## Comment Gérer Vos Documents dans ce Contexte ?

* **Téléversement Ciblé :** Téléversez dans chaque conversation les documents spécifiquement pertinents pour les sujets que vous souhaitez aborder.
* **Activation Sélective :** Utilisez les boutons d'activation/désactivation pour contrôler précisément quels documents l'IA doit consulter pour chaque réponse.
* **Organisation par Conversation :** Organisez vos documents par thématique en créant des conversations dédiées avec les ressources appropriées.
* **Confidentialité Assurée :** Vous pouvez téléverser des documents personnels en toute sécurité, sachant qu'ils ne seront jamais accessibles à d'autres utilisateurs.

## Fonctionnalités de Sécurité

* **Vérification d'Appartenance :** Le système vérifie que vous êtes bien le propriétaire de la conversation avant chaque opération.
* **Isolation des Données :** Aucun croisement de données entre utilisateurs ou entre conversations différentes.
* **Contrôle d'Accès :** Seuls les documents que vous avez explicitement téléversés et activés sont consultés.
* **Paths Sécurisés :** Les chemins de fichiers sont validés pour éviter tout accès non autorisé.

La [Liste des Documents Chargés](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341) dans votre interface vous montre tous les fichiers que vous avez téléversés dans la conversation courante, avec la possibilité de les activer ou désactiver selon vos besoins.

---

Maintenant que vous comprenez comment le système de contexte documentaire privé fonctionne, passons à la section suivante : [Poser des Questions et Obtenir des Réponses](../rag-usage/formulating-questions.md).