---
sidebar_position: 3
title: Problèmes avec le Chat et les Réponses de l'IA
---

# Dépannage : Problèmes avec le Chat et les Réponses de l'IA

Il peut arriver que les réponses de l'intelligence artificielle (IA) ne correspondent pas exactement à vos attentes. Voici quelques scénarios courants et des pistes pour y remédier.

## Que faire si...

### ... La réponse de l'IA ne semble pas liée à mes documents ? (Point 8.3.1)

Si l'IA fournit une réponse qui vous paraît générique ou sans rapport avec les documents que vous avez téléversés pour la discussion en cours :

1.  **Vérifiez la Discussion Active :**
    * Assurez-vous que vous êtes bien dans la [discussion (conversation)](../conversations/switching.md) pour laquelle vous avez téléversé les documents pertinents. Le contexte documentaire est spécifique à chaque discussion.

2.  **Vérifiez les Documents Chargés pour CETTE Discussion :**
    * Consultez le [Panneau de Gestion des Documents](../interface-overview/document-management-pane.md#3-liste-des-documents-chargés-documents-chargés-point-341) pour la discussion active. Les documents que vous vouliez que l'IA utilise y figurent-ils ?
    * Il est possible que les documents aient été téléversés dans une autre discussion par erreur.

3.  **Clarté de Votre Prompt (Question) :**
    * Votre question est-elle suffisamment précise ? Fait-elle référence, même indirectement, aux concepts ou termes présents dans vos documents ? Consultez nos conseils pour [Formuler des Questions Efficaces](../rag-usage/formulating-questions.md).

4.  **Pertinence des Documents :**
    * Les documents téléversés contiennent-ils réellement l'information nécessaire pour répondre à votre question spécifique ? L'IA ne peut pas inventer des informations qui ne sont pas dans son contexte.

5.  **Comportement Actuel du Système (Contexte Global) :**
    * Rappelez-vous que, comme expliqué dans [Comprendre le Contexte Documentaire du Système](../conversations/conversation-context.md), l'IA puise ses informations dans une base de connaissances partagée. Si votre question est très générale, ou si un document téléversé par un autre utilisateur (ou par vous dans une autre session) est jugé très pertinent par l'IA, la réponse pourrait s'en inspirer.
    * Si la réponse est accompagnée du message `"هذه الإجابة من معرفة النموذج اللغوي وليست من النصوص المتوفرة"` (Cette réponse provient des connaissances du modèle linguistique et non des textes fournis), cela confirme que l'IA n'a pas trouvé la réponse dans les documents qu'elle a jugés les plus pertinents pour votre question (ce qui inclut potentiellement tous les documents du système).

### ... L'IA dit qu'elle ne peut pas trouver de réponse ou donne une réponse très générique ? (Point 8.3.2)

Cela peut arriver pour plusieurs raisons :

1.  **Information Absente des Documents :**
    * L'information que vous recherchez n'est peut-être tout simplement pas présente dans les documents que l'IA a à sa disposition (que ce soit les vôtres ou ceux de la base globale).
2.  **Question Trop Vague ou Ambiguë :**
    * Si votre question est trop large, l'IA pourrait avoir du mal à la cibler. Essayez de la [reformuler de manière plus précise](../rag-usage/formulating-questions.md).
3.  **Documents Non Pertinents :**
    * Les documents actuellement dans le contexte de la discussion (ou dans la base globale) ne traitent pas du sujet de votre question. Pensez à [téléverser des documents plus pertinents](../documents/how-to-upload.md) pour cette discussion spécifique.
4.  **Limitations de l'IA :**
    * L'IA n'est pas omnisciente. Même avec les documents, elle peut parfois ne pas réussir à établir les bonnes connexions ou à extraire l'information souhaitée.

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