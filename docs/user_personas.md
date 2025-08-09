# User Personas for Fiqh RAG System UI

This document outlines the primary user personas for our RAG (Retrieval Augmented Generation) system's user interface, which specializes in providing answers based on texts related to Maliki Fiqh. The goal is to ensure user documentation is targeted, clear, and helpful for non-technical users interacting with this specialized content.

## Persona 1: Omar - The Islamic Studies Student

* **Name:** Omar (عمر)
* **Age:** 22
* **Occupation:** University Student specializing in Islamic Law (Sharia), with a focus on Maliki Fiqh.
* **Quote:** "أحتاج إلى طريقة سريعة للبحث في نصوص الفقه المالكي لمساعدتي في واجباتي وأبحاثي." (I need a quick way to search Maliki Fiqh texts to help with my assignments and research.)

### Background & Goals:
Omar is dedicated to his studies and often needs to consult numerous classical and contemporary texts on Maliki Fiqh. He finds manually searching through physical books or fragmented digital PDFs time-consuming.
His primary goals for using the system are:
    1.  To upload his personal collection of Fiqh e-books, articles, and lecture notes (likely PDFs, TXT, and possibly DOCX).
    2.  To ask specific questions about rulings (Ahkam), definitions, and opinions of scholars within the Maliki school based on *his uploaded documents*.
    3.  To quickly find evidence (Daleel) or different scholarly opinions on a particular Fiqh issue from his context.
    4.  To get summaries or explanations of complex Fiqh concepts from his texts.
    5.  To save and organize different research sessions/topics using the conversation history.

### Technical Comfort Level:
* Comfortable using web applications for research, online libraries, and university portals.
* Familiar with uploading and downloading files.
* Understands how to use a chat interface effectively.
* While he understands the subject matter (Fiqh), he is not a programmer and is unfamiliar with terms like "RAG," "LLM," "vector database."
* He expects the system to "understand" Arabic queries accurately and search within the documents he provides.

### Key Tasks in Your Application:
* Creating an account and logging in.
* Starting new conversations (e.g., " مسائل الطهارة - كتاب X" - Issues of Purity - Book X, "فتاوى متعلقة بالمعاملات المالية" - Fatwas related to Financial Transactions).
* Uploading his Fiqh texts.
* Asking questions in Arabic, such as: "ما هو دليل المالكية في مسألة Y؟" (What is the Maliki evidence for issue Y?) or "لخص رأي القرافي في كتاب Z حول موضوع كذا." (Summarize Al-Qarafi's opinion in Book Z on topic X).
* Reviewing the AI's answers and the source documents cited.
* Renaming conversations for better organization.
* Deleting conversations that are no longer needed.

### Potential Frustrations & Documentation Needs:
* **Language Accuracy:** Will be frustrated if the AI misunderstands nuances in Arabic Fiqh terminology or if the interface itself is not clear in Arabic (your UI is in French, but the interaction with RAG is Arabic – this is a point to consider for overall UX, though your current task is docs for the existing UI).
* **Context Reliance:** Needs clear explanation that the AI primarily answers from *his uploaded documents* and how to ensure the right documents are part_of_the_current_conversation's context. The UI should clearly show which documents are active.
* **Source Transparency:** Will highly value the ability to see which part of which document the AI used for its answer.
* **Upload Process:** Needs a simple and reliable document upload feature. Clarity on supported file types is crucial.
* **Understanding Limitations:** Needs to understand that the AI might not always find an answer or might sometimes make mistakes, especially if the documents are complex or the question is ambiguous. The "هذه الإجابة من معرفة النموذج اللغوي وليست من النصوص المتوفرة" (This answer is from the LLM's knowledge and not from the provided texts) message needs to be understood.

---

## Persona 2: Fatima - The Fiqh Enthusiast / Community Educator

* **Name:** Fatima (فاطمة)
* **Age:** 45
* **Occupation:** Active community member who gives informal religious classes/talks; may not have formal advanced Islamic degrees but is a dedicated learner.
* **Quote:** "أريد أن أتحقق من بعض المسائل الفقهية وأجد إجابات مبسطة وموثقة لأسئلة تطرح علي في مجتمعي." (I want to verify some Fiqh issues and find simplified, documented answers for questions asked in my community.)

### Background & Goals:
Fatima often prepares for discussions or answers questions from friends and family on matters of daily religious practice according to the Maliki school. She uses various resources, including simplified Fiqh books and articles.
Her primary goals for using the system are:
    1.  To upload a curated set of Fiqh materials she trusts (PDFs of articles, summaries, possibly some specific Fatwa collections).
    2.  To ask practical, everyday Fiqh questions and get answers based on her uploaded content.
    3.  To find explanations of Fiqh terms or rulings in simple Arabic.
    4.  To quickly check the basis or source for a particular ruling she has read about or been asked about.

### Technical Comfort Level:
* Uses common web applications and social media.
* Can manage file uploads and downloads but prefers straightforward interfaces.
* May not be as technically adept as Omar but is motivated to learn tools that help her religious understanding and teaching.
* Needs very clear, step-by-step instructions for using the application.
* Relies on the system to present information clearly and highlight sources.

### Key Tasks in Your Application:
* Creating an account and logging in.
* Starting conversations based on topics (e.g., "أحكام الصلاة للنساء" - Rulings on Prayer for Women, "الزكاة وشروطها" - Zakat and its Conditions).
* Uploading her selected Fiqh resources.
* Asking questions like: "ما هي شروط صحة الوضوء للمرأة في المذهب المالكي؟" (What are the conditions for the validity of ablution for women in the Maliki school?) or "هل يجوز دفع الزكاة للأقارب المحتاجين؟" (Is it permissible to give Zakat to needy relatives?).
* Reading and understanding the AI's answers and the cited sources.
* Potentially copying answers or parts of answers for her notes or to share.

### Potential Frustrations & Documentation Needs:
* **Simplicity of Use:** Will abandon the tool if it's too complex to use. The UI needs to be very intuitive.
* **Trustworthiness:** Needs reassurance that the answers are based on the documents she provided. The "source documents" feature will be critical.
* **Clarity of Answers:** Hopes for answers that are easy to understand, even if the underlying Fiqh texts are dense. (This is more an LLM/prompt engineering aspect, but the UI should display answers clearly).
* **Managing Uploaded Files:** Needs to easily see what's been uploaded and how it relates to the current chat.
* **Arabic Input/Display:** Expects seamless handling of Arabic text.

---