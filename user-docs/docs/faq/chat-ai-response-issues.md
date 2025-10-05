---
sidebar_position: 3
title: Problèmes avec le Chat et les Réponses de l'IA
---

# Dépannage : Problèmes avec le Chat et les Réponses de l'IA

Il peut arriver que les réponses de l'intelligence artificielle (IA) ne correspondent pas exactement à vos attentes. Voici quelques scénarios courants et des pistes pour y remédier.

## Que faire si...

### ... La réponse de l'IA ne semble pas liée aux documents qui me sont assignés ? (Point 8.3.1)

Si l'IA fournit une réponse qui vous paraît générique ou sans rapport avec les documents qui vous ont été assignés par l'administrateur :

1.  **Vérifiez les Documents Assignés à Votre Compte :**
    * Consultez le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341) pour voir quels documents vous ont été assignés par l'administrateur.
    * Les documents pertinents pour votre domaine d'étude ou vos besoins spécifiques y figurent-ils ?

2.  **Clarté de Votre Prompt (Question) :**
    * Votre question est-elle suffisamment précise ? Fait-elle référence, même indirectement, aux concepts ou termes présents dans les documents qui vous sont assignés ? Consultez nos conseils pour [Formuler des Questions Efficaces](../rag-usage/formulating-questions.md).

3.  **Pertinence des Documents Assignés :**
    * Les documents qui vous ont été assignés par l'administrateur contiennent-ils réellement l'information nécessaire pour répondre à votre question spécifique ? L'IA ne peut accéder qu'aux documents qui vous ont été explicitement assignés.

4.  **Contactez l'Administrateur :**
    * Si vous pensez qu'il manque des documents pertinents pour vos recherches, contactez l'administrateur pour demander l'ajout de documents supplémentaires à votre compte.
    * L'administrateur peut également vérifier si les bons documents vous ont été assignés selon vos besoins.

5.  **Limitation d'Accès aux Documents :**
    * Contrairement aux systèmes où tous les utilisateurs partagent une base commune, vous n'avez accès qu'aux documents spécifiquement assignés à votre compte par l'administrateur.
    * Si la réponse est accompagnée du message `"هذه الإجابة من معرفة النموذج اللغوي وليست من النصوص المتوفرة"` (Cette réponse provient des connaissances du modèle linguistique et non des textes fournis), cela confirme que l'IA n'a pas trouvé la réponse dans les documents qui vous sont assignés.

### ... L'IA dit qu'elle ne peut pas trouver de réponse ou donne une réponse très générique ? (Point 8.3.2)

Cela peut arriver pour plusieurs raisons :

1.  **Information Absente des Documents Assignés :**
    * L'information que vous recherchez n'est peut-être pas présente dans les documents qui vous ont été spécifiquement assignés par l'administrateur.

2.  **Question Trop Vague ou Ambiguë :**
    * Si votre question est trop large, l'IA pourrait avoir du mal à la cibler. Essayez de la [reformuler de manière plus précise](../rag-usage/formulating-questions.md).

3.  **Documents Assignés Non Pertinents :**
    * Les documents actuellement assignés à votre compte ne traitent peut-être pas du sujet de votre question. Dans ce cas, contactez l'administrateur pour :
      * Demander l'assignation de documents plus pertinents
      * Vérifier que les bons documents correspondent à vos besoins de recherche

4.  **Limitations de l'IA :**
    * L'IA n'est pas omnisciente. Même avec les documents assignés, elle peut parfois ne pas réussir à établir les bonnes connexions ou à extraire l'information souhaitée.

### ... La réponse de l'IA n'est pas dans un arabe clair ou a des problèmes de formatage ? (Point 8.3.3)

L'Assistant RAG Fiqh est conçu pour interagir en langue arabe. Cependant :

1.  **Clarté et Style :**
    * L'IA s'efforce de produire un arabe standard et clair. Si le style vous semble inhabituel ou si la clarté n'est pas au rendez-vous, cela peut être une limitation du modèle linguistique actuel.
    * Essayer de reformuler votre question peut parfois influencer le style de la réponse.

2.  **Problèmes de Formatage :**
    * Des problèmes mineurs de formatage (espacements, alignements inhabituels, etc.) peuvent occasionnellement survenir. Cela est généralement dû à la manière dont le texte est généré et affiché.

3.  **Support Linguistique :**
    * Le système est optimisé pour l'arabe. Si vous posez des questions dans une autre langue, la qualité et la pertinence des réponses pourraient être affectées, et l'IA pourrait quand même tenter de répondre en arabe ou de basculer vers la langue de la question si elle la détecte et la supporte (bien que l'objectif principal soit l'arabe pour le Fiqh Maliki).

**Rappel Important :** Comme indiqué dans l'interface, "Ce système RAG peut afficher des informations inexactes". Pour des sujets aussi importants que le Fiqh, il est toujours recommandé de **vérifier les informations critiques** en consultant les textes originaux ou des savants qualifiés.

---

La dernière partie de notre FAQ couvrira des [Questions Générales sur l'Utilisation](./general-usage-faq.md).