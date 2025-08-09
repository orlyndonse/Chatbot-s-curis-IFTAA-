---
sidebar_position: 1
title: Formuler des Questions Efficaces
---

# Formuler des Questions (Prompts) Efficaces en Arabe

Pour obtenir les réponses les plus précises et utiles de l'Assistant RAG Fiqh, la manière dont vous formulez vos questions (appelées "prompts") en langue arabe est importante. Voici quelques conseils pour vous aider, en particulier pour des sujets liés au Fiqh Maliki :

## 1. Soyez Clair et Spécifique

* **Précision :** Plus votre question est précise, mieux l'IA pourra la comprendre et chercher des informations pertinentes dans les documents que vous avez fournis.
    * *Moins efficace :* "ما هو حكم الصلاة؟" (Quel est le jugement sur la prière ?) - C'est trop vague.
    * *Plus efficace :* "ما هي شروط صحة صلاة الجمعة في المذهب المالكي للمسافر؟" (Quelles sont les conditions de validité de la prière du Vendredi dans l'école Maliki pour le voyageur ?)
* **Contexte :** Si votre question se réfère à un concept ou un terme spécifique mentionné dans un document que vous avez téléversé, essayez de l'inclure ou de le contextualiser dans votre prompt.

## 2. Utilisez la Terminologie Fiqh Appropriée (si connue)

* Si vous connaissez les termes techniques du Fiqh Maliki relatifs à votre question (par exemple, `مكروه`, `مندوب`, `شروط الأركان`), leur utilisation peut aider l'IA à mieux cibler sa recherche.
* Cependant, le système est conçu pour comprendre également le langage naturel. N'hésitez pas à poser votre question comme vous le feriez à une personne.

## 3. Posez une Seule Question Principale par Prompt

* Évitez de poser plusieurs questions distinctes dans un seul prompt. Cela peut embrouiller l'IA ou conduire à des réponses incomplètes.
    * *Moins efficace :* "ما حكم صلاة الوتر وكيفية قضائها وما هو وقتها المفضل؟" (Quel est le jugement sur la prière Witr, comment la rattraper, et quel est son temps préférable ?)
    * *Plus efficace :* Posez chaque question dans un prompt séparé au sein de la même discussion.

## 4. Fournissez le Contexte Documentaire Adéquat

* **Rappel :** L'IA se base principalement sur les [documents que vous avez téléversés](../documents/how-to-upload.md) pour la [discussion active](../conversations/conversation-context.md).
* Assurez-vous que les documents contenant les informations que vous recherchez sont bien présents dans le contexte de la discussion en cours.

## 5. Soyez Conscient de la Langue

* **Arabe Standard/Classique :** Privilégiez l'arabe standard (الفصحى) pour vos questions, car les textes de Fiqh sont généralement rédigés dans cette langue.
* **Dialectes :** L'IA pourrait avoir plus de difficultés à comprendre des questions formulées en dialectes arabes très spécifiques si les documents de référence ne les utilisent pas.

## 6. Itérer et Reformuler

* Si la première réponse de l'IA n'est pas satisfaisante ou semble hors sujet :
    * **Reformulez votre question :** Essayez d'utiliser des synonymes, d'être plus précis, ou d'aborder la question sous un angle légèrement différent.
    * **Vérifiez vos documents :** L'information que vous cherchez est-elle réellement présente dans les documents téléversés pour cette discussion ?
    * **Posez des questions de suivi :** Vous pouvez poser des questions complémentaires pour affiner la recherche ou demander des clarifications sur une réponse précédente.

**Exemples de Prompts Efficaces (pour Omar et Fatima) :**

* Pour Omar (étudiant) :
    * "ما هو تعريف 'الاستحسان' عند الأصوليين المالكية مع ذكر مثال من كتاب الموافقات للشاطبي؟" (Quelle est la définition de 'l'Istihsan' chez les Usulistes Malikites, avec un exemple du livre Al-Muwafaqat d'Al-Shatibi ?) - *S'il a téléversé "الموافقات".*
    * "لخص الفروق الأساسية بين شروط صحة البيع وأركانه في المذهب المالكي بناءً على الوثيقة المرفوعة 'ملخص فقه المعاملات'." (Résumez les différences fondamentales entre les conditions de validité de la vente et ses piliers dans l'école Maliki, basé sur le document téléversé 'Résumé de Fiqh des Transactions'.)
* Pour Fatima (éducatrice communautaire) :
    * "هل يجوز للمرأة الحائض قراءة القرآن دون مس المصحف في المذهب المالكي؟" (Est-il permis à une femme en état de menstruation de lire le Coran sans toucher le Mushaf dans l'école Maliki ?)
    * "ما هي أنواع المياه التي يصح بها الوضوء وفقاً لما ورد في 'الرسالة' لابن أبي زيد القيرواني؟" (Quels sont les types d'eau avec lesquels l'ablution est valide selon ce qui est mentionné dans 'Al-Risala' d'Ibn Abi Zayd Al-Qayrawani ?) - *Si elle a téléversé "الرسالة".*

En suivant ces conseils, vous augmenterez vos chances d'obtenir des réponses pertinentes et utiles de l'Assistant RAG Fiqh.

---

Une fois que vous avez formulé votre question, il est temps de l'[Envoyer à l'IA](./sending-prompt.md).