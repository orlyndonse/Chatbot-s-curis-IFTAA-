// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Documentation Technique - Assistant RAG Fiqh',
  tagline: 'Description technique détaillée de l\'architecture et du fonctionnement de l\'Assistant RAG Fiqh.',
  favicon: 'img/favicon.svg', 

  url: 'https://URL_DE_DEPLOYEMENT.com',
  baseUrl: '/doc-technique-rag-fiqh/',

  organizationName: 'VOTRE_NOM_UTILISATEUR_GITHUB',
  projectName: 'assistant-rag-fiqh-docs-technique',

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
          routeBasePath: '/',
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
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Doc Technique RAG Fiqh',
        logo: {
          alt: 'Logo Assistant RAG Fiqh',
          src: 'img/logo-light.svg',     
          srcDark: 'img/logo-dark.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Documentation Technique',
          },
          {
            href: 'https://github.com/orlyndonse/Chatbot-s-curis-IFTAA-',
            label: 'Projet Principal (GitHub)',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Navigation',
            items: [
              {
                label: 'Introduction',
                to: '/',
              },
              {
                label: 'Architecture',
                to: '/architecture',
              },
            ],
          },
          {
            title: 'Liens Utiles',
            items: [
              {
                label: 'Documentation Utilisateur',
                href: 'http://localhost:3001/my-docs/', 
              },
              {
                label: 'Signaler un Problème (Doc Technique)',
                href: 'https://github.com/orlyndonse/Chatbot-s-curis-IFTAA-/issues', 
              },
            ],
          },
          {
            title: 'Plus',
            items: [
              {
                label: 'Projet Principal (GitHub)',
                href: 'https://github.com/orlyndonse/Chatbot-s-curis-IFTAA-',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Assistant RAG Fiqh - Documentation Technique. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'json', 'bash', 'sql'],
      },
    }),
};

export default config;