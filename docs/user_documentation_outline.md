# User Documentation Outline for Fiqh RAG System

This document outlines the structure and topics to be covered in the user manual, tailored for the Fiqh RAG System and its users, Omar (student) and Fatima (community educator).

## 1. Introduction
    1.1. Welcome to the Fiqh RAG System!
    1.2. What is this system for? (Brief, non-technical explanation: e.g., "Helping you ask questions and get answers from your uploaded Fiqh documents in Arabic.")
    1.3. Who is this guide for? (Referencing Omar and Fatima, emphasizing ease of use for non-programmers with an interest in Maliki Fiqh.)
    1.4. System Requirements (e.g., modern web browser, internet connection).

## 2. Getting Started
    2.1. Creating Your Account
        2.1.1. Step-by-step guide to the registration form (`Register.jsx`).
        2.1.2. Understanding the email verification process (what to expect, checking spam, link validity as handled by `VerifyEmailHandler.jsx`).
    2.2. Logging In
        2.2.1. How to log in with your email and password (`Login.jsx`).
        2.2.2. Using the "Forgot Password?" / "Mot de passe oublié?" feature (`ResetLink.jsx`, `ResetPassword.jsx`).
    2.3. Quick Tour of the Main Interface (`App.jsx`)
        2.3.1. The Sidebar: Accessing your conversation history and starting new chats (`Sidebar.jsx`).
        2.3.2. The Main Chat Area: Where your interactions happen. Includes initial greeting (`Greetings.jsx`).
        2.3.3. The Prompt Input Field: Where you type your questions (`PromptField.jsx`).
        2.3.4. The Document Management Area: Managing files for your conversations (`DocumentList.jsx` displayed within `App.jsx`).
        2.3.5. The Top Bar: Navigation and account options (`TopAppBar.jsx`).

## 3. Understanding the Interface
    3.1. The Sidebar (`Sidebar.jsx`): Your Conversation Hub
        3.1.1. Understanding the "Historique" (History) list.
        3.1.2. Using the "Nouvelle Discussion" (New Chat) button.
        3.1.3. How the sidebar can be toggled on smaller screens (menu icon in `TopAppBar.jsx`).
    3.2. The Main Chat Area (`App.jsx`): Where Questions and Answers Appear
        3.2.1. Identifying your questions (prompts).
        3.2.2. Identifying the AI's answers (visual distinction).
        3.2.3. Recognizing loading indicators (e.g., `CircularProgress` while AI is generating a response or messages are loading).
    3.3. The Prompt Field (`PromptField.jsx`): Asking Your Questions
        3.3.1. How to type your question (emphasize using Arabic for Fiqh topics).
        3.3.2. Using the "Send" (Envoyer) button.
        3.3.3. Using the "Upload" (Uploader des documents) button.
    3.4. Document Management Pane (`DocumentList.jsx` rendered in `App.jsx`)
        3.4.1. Viewing currently loaded documents for the active conversation.
        3.4.2. Understanding the "Taille du contexte" (Context Size) indicator.
    3.5. Top Bar (`TopAppBar.jsx`)
        3.5.1. User avatar and accessing the user menu.
        3.5.2. Using the "Se déconnecter" (Logout) option.

## 4. Working with Conversations (Chats)
    4.1. Starting a New Conversation
        4.1.1. Clicking "Nouvelle Discussion" in the sidebar.
        4.1.2. How the system automatically titles new conversations (based on the first prompt, as per `App.jsx` logic).
    4.2. Switching Between Conversations
        4.2.1. Clicking a conversation in the "Historique" (History) list in the sidebar.
        4.2.2. What happens: messages for the selected conversation are loaded.
    4.3. Renaming a Conversation
        4.3.1. Finding the rename icon (drive_file_rename_outline) on a conversation item in the sidebar (appears on hover).
        4.3.2. Step-by-step: clicking the icon, typing the new name, saving, or canceling.
    4.4. Deleting a Conversation
        4.4.1. Finding the delete icon on a conversation item in the sidebar (appears on hover).
        4.4.2. Understanding the action (no explicit confirmation dialog in current `App.jsx` logic, deletion is direct).
        4.4.3. What happens: conversation is removed, and the next available one (or none) becomes active.
    4.5. Understanding Conversation Context
        4.5.1. Explaining that documents are uploaded *within the context of the currently active conversation*.
        4.5.2. AI responses in one conversation are primarily based on documents uploaded to *that specific conversation*.

## 5. Asking Questions and Getting Answers (Using the RAG System)
    5.1. How to Formulate Effective Questions (Prompts) in Arabic for Fiqh Topics (General advice, not a UI feature).
    5.2. Sending Your Prompt (Recap of using the prompt field and send button).
    5.3. Understanding the AI's Response
        5.3.1. Where the answer appears in the chat area.
        5.3.2. Identifying answers based on your documents vs. general AI knowledge (explaining the significance of the "هذه الإجابة من معرفة النموذج اللغوي..." message if the backend provides it).
        5.3.3. Understanding Source Attribution:
            5.3.3.1. Explain that the "Documents chargés" list in the `DocumentList` shows all files currently considered as context for the AI's answers in *that conversation*.
            5.3.3.2. *(If applicable based on backend output)* If the AI response itself mentions specific source filenames (like the original notebook did), explain how to interpret this.
    5.4. Editing Your Prompt (`App.jsx` logic: `handleStartEdit`, `handleSaveEdit`)
        5.4.1. How to find and use the "Edit" icon (appears on hover for the last user prompt).
        5.4.2. Modifying your text in the editing interface.
        5.4.3. Saving changes and how the AI will regenerate its response based on the edited prompt and subsequent messages.
        5.4.4. How to cancel editing.

## 6. Managing Documents for Context
    6.1. Why Upload Documents? (Explaining simply: "Provide the AI with specific Fiqh texts so it can answer your questions accurately based on that information.")
    6.2. How to Upload Documents
        6.2.1. Using the "Uploader des documents" button (paperclip icon) in the Prompt Field (`PromptField.jsx`).
        6.2.2. Using the drag-and-drop area or "cliquez pour parcourir" in the Document List section (`DocumentList.jsx`).
        6.2.3. Supported file types (PDF, TXT, DOC, DOCX, CSV, HTML, as per `DocumentList.jsx` and `PromptField.jsx` accept props).
        6.2.4. Understanding that multiple files can be uploaded.
    6.3. Viewing Uploaded Documents (`DocumentList.jsx`)
        6.3.1. Locating the "Documents chargés" list.
        6.3.2. Information displayed: filename, icon (description, picture_as_pdf, file_present), and size.
    6.4. Previewing Documents (`DocumentList.jsx` and `DocumentPreview.jsx`)
        6.4.1. Clicking the "Aperçu" (Preview) button for a document.
        6.4.2. How different file types (text, PDF) are displayed in the preview modal.
        6.4.3. Closing the preview.
        6.4.4. Note: The "Ajouter au contexte" button in `DocumentPreview.jsx` is not currently active for adding after preview; documents are added upon initial upload. (Adjust if this button becomes functional for re-adding or a similar purpose).
    6.5. Deleting Documents from a Conversation's Context (`DocumentList.jsx` and `App.jsx`)
        6.5.1. Clicking the "Supprimer" (Delete) button for a document.
        6.5.2. Effect: The document is removed from the context of the current conversation and will no longer be used by the AI for answers in this chat.
    6.6. Understanding Document Limits (`DocumentList.jsx`)
        6.6.1. Explaining the "Taille du contexte" (Context Size) indicator and `maxContextSize`.

## 7. Account Management
    7.1. Logging Out (via user menu in `TopAppBar.jsx`).
    7.2. Changing Your Password (Currently, this is done via the "Forgot Password" flow when logged out. No in-app feature to change password while logged in seems present).
    7.3. Managing Profile Information (Currently, no feature seems present for users to update their first name, last name, or username after registration).

## 8. Troubleshooting & FAQ
    8.1. **Login & Account Issues**
        8.1.1. "I can't log in." (Check credentials, internet connection).
        8.1.2. "I didn't receive the verification email." (Check spam, try resending from the "Vérification requise" page).
        8.1.3. "I forgot my password." (Guide to "Mot de passe oublié?" link).
    8.2. **Document Upload Issues**
        8.2.1. "My file won't upload." (Check supported types, size limits if any are enforced visibly, internet connection).
        8.2.2. "How do I know if my document was processed correctly by the AI?" (Explain that if it appears in "Documents chargés," it's available to the AI for that conversation. The AI's answers referencing it are the main feedback).
    8.3. **Chat & AI Response Issues**
        8.3.1. "The AI's answer doesn't seem related to my documents." (Ensure correct conversation is active, documents are uploaded to *that* conversation, prompt is clear).
        8.3.2. "The AI says it can't find an answer or gives a generic response." (Documents might not contain the info, question might be too broad/ambiguous, try rephrasing or uploading more relevant docs).
        8.3.3. "The AI's answer is not in clear Arabic / has formatting issues." (Note: This might be a system limitation to mention briefly).
    8.4. **General Usage**
        8.4.1. "How do I save my chat?" (Explain conversations and messages are automatically saved as part of the history).
        8.4.2. "Can I export my conversation or specific answers?" (If this feature is not present, state that it's not currently available).
        8.4.3. "What does 'Ce système RAG peut afficher des informations inexactes' mean?" (Briefly explain that AI can make mistakes and users should cross-verify critical information, especially in a Fiqh context).