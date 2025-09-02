import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Assistant RAG Fiqh - Guide Utilisateur', 
  tagline: 'Votre guide pour poser des questions et obtenir des réponses à partir de textes du Fiqh Maliki',
  favicon: 'img/favicon.svg',

  url: 'https://YOUR_SITE_URL_HERE.com', 
  baseUrl: '/my-docs/',
  organizationName: 'YOUR_GITHUB_ORG_OR_USERNAME_HERE', 
  projectName: 'YOUR_DOCS_REPO_NAME_HERE', 

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  
  i18n: {
    defaultLocale: 'fr',
    locales: ['fr'],
  },

  stylesheets: [ 
    'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap',
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Guide Assistant RAG Fiqh', 
        logo: {
          alt: 'Logo Assistant RAG Fiqh',
          src: 'img/logo-light.svg',    
          srcDark: 'img/logo-dark.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar', 
            position: 'left',
            label: 'Manuel Utilisateur',
          },
          {
            href: 'https://github.com/orlyndonse/Chatbot-s-curis-IFTAA-',
            label: 'Projet GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Guide', 
            items: [
              {
                label: 'Introduction',
                to: '/docs/introduction/welcome', 
              },
            ],
          },
          {
            title: 'Communauté',
            items: [
              {
                label: 'Signaler un Problème (App)',
                href: 'https://github.com/orlyndonse/Chatbot-s-curis-IFTAA-/issues', 
              },
            ],
          },
          {
            title: 'Plus',
            items: [
              {
                label: 'Projet de l\'Application (GitHub)', 
                href: 'https://github.com/orlyndonse/Chatbot-s-curis-IFTAA-', 
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Assistant RAG Fiqh. Créé avec Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;