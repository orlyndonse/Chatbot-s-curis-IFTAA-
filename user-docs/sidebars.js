// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    // Section 1: Introduction
    {
      type: 'doc',
      id: 'introduction/welcome',
    },
    // Section 2: Getting Started
    {
      type: 'category',
      label: 'Getting Started',
      link: {
        type: 'generated-index',
      },
      items: [
        'getting-started/creating-account',
        'getting-started/logging-in',
        'getting-started/quick-tour',
      ],
    },
    // Section 3: Understanding the Interface
    {
      type: 'category',
      label: 'Understanding the Interface',
      link: {type: 'generated-index'},
      items: [
        'interface-overview/sidebar',
        'interface-overview/main-chat-area',
        'interface-overview/prompt-field',
        'interface-overview/document-management-pane',
        'interface-overview/top-bar',
      ],
    },
    // Section 4: Working with Conversations (Chats)
    {
      type: 'category',
      label: 'Working with Conversations',
      link: {type: 'generated-index'},
      items: [
        'conversations/starting-new',
        'conversations/switching',
        'conversations/renaming',
        'conversations/deleting',
        'conversations/conversation-context',
      ],
    },
    // Section 5: Asking Questions and Getting Answers
    {
      type: 'category',
      label: 'Asking Questions & Getting Answers',
      link: {type: 'generated-index'},
      items: [
        'rag-usage/formulating-questions',
        'rag-usage/sending-prompt',
        'rag-usage/understanding-responses',
        'rag-usage/editing-prompt',
      ],
    },
    // Section 6: Managing Documents for Context
    {
      type: 'category',
      label: 'Managing Documents for Context',
      link: {type: 'generated-index'},
      items: [
        'documents/why-upload',
        'documents/how-to-upload',
        'documents/viewing-uploaded',
        'documents/previewing-documents',
        'documents/deleting-documents',
        'documents/document-limits',
      ],
    },
    // Section 7: Account Management
    {
      type: 'category',
      label: 'Account Management',
      link: {type: 'generated-index'},
      items: [
        'account/logging-out',
        'account/changing-password',  // Assuming you created these explanatory pages
        'account/managing-profile',   // Assuming you created these explanatory pages
      ],
    },
    // Section 8: Troubleshooting & FAQ
    {
      type: 'category',
      label: 'Troubleshooting & FAQ',
      link: {type: 'generated-index'},
      items: [
        'faq/login-account-issues',
        'faq/document-upload-issues',
        'faq/chat-ai-response-issues',
        'faq/general-usage-faq',
      ],
    },
    // Section 9: Glossary (Our new addition)
    {
      type: 'doc',
      id: 'glossary', // This must match the filename `glossary.md` in the `docs` root
      label: 'Glossaire', // This is the text that will appear in the sidebar
    },
  ],
};

export default sidebars; // or module.exports = sidebars;