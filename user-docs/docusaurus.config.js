// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  // --- Site Metadata ---
  title: 'Assistant RAG Fiqh - Guide Utilisateur', // French Title
  tagline: 'Votre guide pour poser des questions et obtenir des réponses à partir de textes du Fiqh Maliki', // French Tagline
  favicon: 'img/favicon.svg',

  url: 'https://YOUR_SITE_URL_HERE.com', 
  baseUrl: '/my-docs/', // As per your current setup
  organizationName: 'YOUR_GITHUB_ORG_OR_USERNAME_HERE', 
  projectName: 'YOUR_DOCS_REPO_NAME_HERE', 

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  
  i18n: {
    defaultLocale: 'fr',
    locales: ['fr'],
  },

  stylesheets: [ // Assuming DM Sans is still desired
    'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap',
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // editUrl: 'YOUR_EDIT_URL_HERE', // Optional
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
        title: 'Guide Assistant RAG Fiqh', // French Navbar Title
        logo: {
          alt: 'Logo Assistant RAG Fiqh', // French Alt Text
          src: 'img/logo-light.svg',    
          srcDark: 'img/logo-dark.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar', 
            position: 'left',
            label: 'Manuel Utilisateur', // French Label
          },
          {
            href: 'https://github.com/YOUR_USERNAME/YOUR_MAIN_PROJECT_REPO_NAME', // Keep as your actual link
            label: 'Projet GitHub', // French Label
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Guide', // Already French-friendly
            items: [
              {
                label: 'Introduction', // Already French-friendly
                to: '/docs/introduction/welcome', // Adjusted to match sidebar
              },
            ],
          },
          {
            title: 'Communauté', // French Title
            items: [
              {
                label: 'Signaler un Problème (App)', // French Label
                href: 'https://github.com/YOUR_USERNAME/YOUR_MAIN_PROJECT_REPO_NAME/issues', // Keep as your actual link
              },
            ],
          },
          {
            title: 'Plus', // French Title
            items: [
              {
                label: 'Projet de l\'Application (GitHub)', // French Label
                href: 'https://github.com/YOUR_USERNAME/YOUR_MAIN_PROJECT_REPO_NAME', // Keep as your actual link
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Assistant RAG Fiqh. Créé avec Docusaurus.`, // French Copyright
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;