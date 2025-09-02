---
sidebar_position: 1
title: Phase d'Ingestion des Documents
---

# Phase d'Ingestion des Documents

La phase d'ingestion des documents est la première étape cruciale du pipeline RAG (Retrieval Augmented Generation). Elle consiste à prendre les fichiers sources fournis par l'utilisateur, à les traiter et à les stocker d'une manière qui permette une récupération d'information efficace par la suite. Ce processus est principalement géré par la méthode `process_and_index_files` du `ConversationService`, qui s'appuie sur les modules `src/rag/loader.py` et `src/rag/vectorstore.py`.

## Étapes Clés de l'Ingestion

Lorsqu'un utilisateur téléverse un ou plusieurs fichiers via l'endpoint `/conversations/{conversation_uid}/upload`, les étapes suivantes sont exécutées :

1.  **Sauvegarde Physique des Fichiers**:
    * Les fichiers téléversés sont d'abord sauvegardés sur le serveur.
    * Un répertoire spécifique à la conversation est créé (s'il n'existe pas) dans le dossier `Config.UPLOAD_DIR` (par exemple, `uploaded_files/{conversation_uid}/`).
    * Les noms de fichiers sont "sanétisés" (nettoyés) pour éviter les caractères invalides ou les tentatives de traversée de répertoire, améliorant ainsi la sécurité.
    * Le contenu de chaque fichier est écrit dans son emplacement persistant.

2.  **Enregistrement des Métadonnées en Base de Données (PostgreSQL)**:
    * Pour chaque fichier sauvegardé, un enregistrement est créé dans la table `Document` de la base de données relationnelle.
    * Ces métadonnées incluent :
        * `uid`: Un identifiant unique pour l'enregistrement du document.
        * `filename`: Le nom sanétisé du fichier.
        * `conversation_uid`: L'UID de la conversation à laquelle le document est associé.
        * `file_path`: Le chemin relatif du fichier par rapport à `Config.UPLOAD_DIR`.
        * `upload_date`: La date et l'heure du téléversement.
        * `size`: La taille du fichier en octets.
        * `mime_type`: Le type MIME du fichier (détecté ou fourni).

3.  **Préparation pour le Traitement RAG**:
    * Une copie de chaque fichier est également placée dans un répertoire temporaire (`temp_dir_for_rag_processing`). Cela permet aux chargeurs de documents Langchain de traiter un ensemble de fichiers à partir d'un emplacement unique.

4.  **Chargement des Documents (`charger_documents`)**:
    * La fonction `charger_documents` de `src/rag/loader.py` est appelée avec le chemin du répertoire temporaire.
    * Cette fonction utilise `DirectoryLoader` de Langchain et des chargeurs spécifiques (comme `PyPDFLoader`, `CSVLoader`, et le `ArabicTextLoader` personnalisé) pour lire le contenu des différents types de fichiers et les convertir en une liste d'objets `Document` de Langchain.
    * Le `ArabicTextLoader` applique un prétraitement au texte arabe (normalisation, remodelage, gestion bidi).

5.  **Découpage des Documents (`split_documents`)**:
    * Si des documents ont été chargés avec succès, la fonction `split_documents` de `src/rag/loader.py` est appelée.
    * Elle utilise `RecursiveCharacterTextSplitter` de Langchain pour découper le contenu de chaque `Document` en segments (chunks) plus petits et gérables.
    * Les paramètres `chunk_size` (taille des segments) et `chunk_overlap` (chevauchement entre segments) sont configurés pour optimiser la récupération d'informations tout en maintenant le contexte.

6.  **Création des Embeddings et Stockage dans ChromaDB (`add_documents_to_vectorstore`)**:
    * Les segments de documents découpés sont ensuite passés à la fonction `add_documents_to_vectorstore` de `src/rag/vectorstore.py`.
    * Cette fonction :
        * Récupère l'instance du VectorStore Langchain (`Chroma`) qui est configurée avec le modèle d'embedding HuggingFace (`paraphrase-multilingual-mpnet-base-v2`).
        * Pour chaque segment de document, le modèle d'embedding génère un vecteur numérique (embedding) qui capture sa signification sémantique.
        * Ces embeddings, ainsi que le texte original des segments et leurs métadonnées (comme la source), sont stockés dans la collection spécifiée (`COLLECTION_NAME`) de ChromaDB.

7.  **Nettoyage**:
    * Le répertoire temporaire (`temp_dir_for_rag_processing`) utilisé pour le traitement RAG est supprimé après l'indexation.

8.  **Réponse à l'Utilisateur**:
    * Le frontend reçoit une réponse indiquant le succès du traitement, la liste des métadonnées des documents traités, et les erreurs éventuelles survenues lors du traitement de fichiers spécifiques.

Ce processus d'ingestion garantit que les documents sont non seulement stockés de manière persistante, mais aussi transformés et indexés de manière à pouvoir être interrogés efficacement par le système RAG pour la génération de réponses.

---

Après l'ingestion, l'étape suivante est la [Phase de Génération de Réponse](./generation.md), où le système utilise ces documents indexés pour répondre aux questions des utilisateurs.