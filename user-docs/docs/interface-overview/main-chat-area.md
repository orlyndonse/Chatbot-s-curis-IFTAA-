---
sidebar_position: 2
title: La Zone de Chat Principale
---

# La Zone de Chat Principale : Vos Interactions avec l'IA

La zone de chat principale est l'espace central de l'Assistant RAG Fiqh. C'est ici que vous verrez vos questions (prompts) que vous envoyez à l'intelligence artificielle (IA) et les réponses qu'elle génère.

![Vue générale de la zone de chat principale avec des messages](/img/screenshot-main-chat-area-messages.png)
## Que Voyez-Vous dans la Zone de Chat ?

### 1. Message de Bienvenue (Point 2.3.2 de l'outline, réf.)

Lorsque vous démarrez une nouvelle discussion ou que vous vous connectez pour la première fois sans conversation active, un message d'accueil s'affiche. Il vous invite généralement à poser votre première question.

* Ce message peut ressembler à : "مرحبا، [Votre Prénom] كيف يمكنني مساعدتك؟" (Bonjour [Votre Prénom], comment puis-je vous aider ?)

    ![Message de bienvenue dans la zone de chat](/img/screenshot-chat-greeting.png) 

### 2. Vos Questions (Prompts) (Point 3.2.1)

Chaque fois que vous tapez une question dans le [Champ de Saisie de Prompt](./prompt-field.md) et que vous l'envoyez, votre question apparaît dans cette zone de chat.

* **Identification :** Vos questions sont généralement alignées d'un côté de la zone de chat (par exemple, à gauche) et peuvent avoir un style visuel distinct (par exemple, une bulle de couleur spécifique).

    ![Exemple de question utilisateur dans le chat](/img/screenshot-user-prompt-bubble.png) 

### 3. Les Réponses de l'IA (Point 3.2.2)

Après avoir envoyé votre question, l'IA prendra un moment pour la traiter et générer une réponse basée sur les documents que vous avez fournis.

* **Identification :** Les réponses de l'IA apparaissent généralement sous votre question, souvent alignées du côté opposé (par exemple, à droite) et avec un style visuel différent de vos questions (par exemple, une bulle d'une autre couleur).
* **Contenu :** La réponse sera en langue arabe et visera à répondre à votre interrogation en se basant sur le contexte des documents de Fiqh Maliki que vous avez téléversés pour la discussion en cours.

    ![Exemple de réponse de l'IA dans le chat](/img/screenshot-ai-response-bubble.png) 
    
### 4. Indicateurs de Chargement (Point 3.2.3)

Pendant que l'IA traite votre question et génère une réponse, ou pendant que les messages d'une conversation existante sont chargés, vous verrez un indicateur de chargement.

* **Lors de l'envoi d'un message :** Après avoir envoyé un prompt, une petite animation de chargement (comme un cercle qui tourne - `CircularProgress`) peut apparaître à côté de votre question ou à l'endroit où la réponse de l'IA est attendue, indiquant que le système travaille.
* **Lors du chargement d'une conversation :** Si vous sélectionnez une conversation depuis l'[Historique](./sidebar.md), un indicateur de chargement plus général peut s'afficher brièvement pendant que les messages de cette conversation sont récupérés.

    ![Indicateur de chargement pendant la génération de la réponse](/img/screenshot-chat-loading-indicator.png) Comprendre ces éléments vous aidera à suivre le déroulement de vos interactions avec l'Assistant RAG Fiqh.

---

Ensuite, apprenons en détail comment [Utiliser le Champ de Saisie de Prompt](./prompt-field.md) pour poser vos questions.