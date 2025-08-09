---
sidebar_position: 2
title: Problèmes de Téléversement de Documents
---

# Dépannage : Problèmes de Téléversement (Upload) de Documents

Voici des solutions aux problèmes courants que vous pourriez rencontrer lors du téléversement de documents dans l'Assistant RAG Fiqh.

## Que faire si...

### ... Mon fichier ne se téléverse pas ou une erreur s'affiche ? (Point 8.2.1)

Si vous rencontrez des difficultés pour téléverser un document, voici plusieurs points à vérifier :

1.  **Vérifiez le Type de Fichier :**
    * L'application accepte des formats de fichiers spécifiques. Assurez-vous que votre document est l'un des types supportés :
        * PDF (`.pdf`)
        * Texte brut (`.txt`)
        * Microsoft Word (`.doc`, `.docx`)
        * CSV (`.csv`)
        * HTML (`.html`)
    * Vous pouvez trouver la liste des formats supportés dans la section [Comment Téléverser des Documents](../documents/how-to-upload.md#formats-de-fichiers-supportés-point-623).

2.  **Vérifiez la Taille du Fichier et la Taille Totale du Contexte :**
    * **Taille du Fichier Individuel :** Bien que l'interface n'affiche pas de limite stricte par fichier, des fichiers extrêmement volumineux (par exemple, plusieurs centaines de Mégaoctets) peuvent être difficiles à téléverser ou à traiter. Essayez avec des fichiers de taille plus raisonnable si possible.
    * **Taille Totale du Contexte :** Gardez un œil sur l'[Indicateur de Taille du Contexte](../interface-overview/document-management-pane.md#2-indicateur-de-taille-du-contexte-point-342). Si vous approchez de la limite indicative (par exemple, 100 Ko), cela pourrait affecter le traitement de nouveaux documents volumineux pour cette discussion. Référez-vous à [Comprendre les Limites des Documents](../documents/document-limits.md).

3.  **Connexion Internet :**
    * Une connexion Internet stable est nécessaire pour téléverser des fichiers. Vérifiez que votre connexion est active et fonctionnelle.
    * Si votre connexion est lente, le téléversement de fichiers volumineux peut prendre du temps ou échouer.

4.  **Nom du Fichier :**
    * Essayez d'utiliser des noms de fichiers simples, sans caractères spéciaux complexes ou très longs.

5.  **Message d'Erreur :**
    * Si un message d'erreur spécifique s'affiche lors de la tentative de téléversement, notez-le. Il pourrait donner une indication sur la nature du problème (par exemple, "Type de fichier non supporté", "Fichier trop volumineux" si des limites serveur existent, ou une erreur réseau). Votre application utilise un `Snackbar` pour afficher de tels messages.

6.  **Essayez à Nouveau :**
    * Parfois, des problèmes temporaires de réseau ou de serveur peuvent causer un échec. Essayez de téléverser le fichier à nouveau après quelques instants.

7.  **Navigateur Web :**
    * Assurez-vous que votre navigateur web est à jour. Dans de rares cas, des extensions de navigateur pourraient interférer ; essayez de téléverser dans une fenêtre de navigation privée pour voir si cela change quelque chose.

### ... Comment savoir si mon document a été correctement traité et est utilisé par l'IA ? (Point 8.2.2)

1.  **Apparition dans la Liste :**
    * Une fois le téléversement réussi, votre document devrait apparaître dans la liste des "**Documents chargés**" dans le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341) pour la discussion active. C'est la première indication que le fichier a été reçu par l'application.

2.  **Mise à Jour de la Taille du Contexte :**
    * L'[Indicateur de Taille du Contexte](../interface-overview/document-management-pane.md#2-indicateur-de-taille-du-contexte-point-342) devrait augmenter pour refléter l'ajout de votre nouveau document.

3.  **Qualité des Réponses de l'IA :**
    * La meilleure indication que vos documents sont utilisés est lorsque vous posez des questions relatives à leur contenu et que l'IA fournit des réponses précises et spécifiques basées sur ces documents.
    * Si l'IA mentionne explicitement des informations qui ne pourraient provenir que de vos fichiers téléversés, c'est un bon signe.

4.  **Absence d'Erreurs :**
    * Si le téléversement avait échoué ou si le fichier n'avait pas pu être traité par le backend, vous auriez probablement reçu un message d'erreur (via le `Snackbar`). L'absence d'erreur après le téléversement et l'apparition du fichier dans la liste sont généralement de bons signes.

5.  **Note sur le Traitement Backend :**
    * Le téléversement vers l'interface utilisateur est la première étape. Ensuite, le système backend doit "indexer" le document (le lire, le découper, et le transformer pour que l'IA puisse l'utiliser). Ce processus est géré par des fonctions comme `process_and_index_files` dans le service de conversation du backend. Bien que vous ne voyiez pas directement ce processus d'indexation dans l'interface, le fait que le document soit listé et que l'IA commence à utiliser son contenu pour répondre à vos questions indique que cela s'est bien passé.

Si vous avez suivi les étapes de téléversement correctement et que le fichier apparaît dans votre liste sans message d'erreur, il est très probable qu'il soit pris en compte par l'IA pour la discussion en cours.

---

La section suivante de la FAQ abordera les [Problèmes liés au Chat et aux Réponses de l'IA](./chat-ai-response-issues.md).