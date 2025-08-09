// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Documentation Technique - Assistant RAG Fiqh',
  tagline: 'Description technique détaillée de l\'architecture et du fonctionnement de l\'Assistant RAG Fiqh.',
  favicon: 'img/favicon.svg', // Confirm this path is correct (static/img/favicon.svg)

  url: 'https://VOTRE_URL_DE_DEPLOYEMENT.com', // **MODIFIEZ CECI**
  baseUrl: '/doc-technique-rag-fiqh/', // **MODIFIEZ CECI** (ex: si déployé sur GitHub Pages, ce sera /nom-du-repo/)

  organizationName: 'VOTRE_NOM_UTILISATEUR_GITHUB', // **MODIFIEZ CECI**
  projectName: 'assistant-rag-fiqh-docs-technique', // **MODIFIEZ CECI** (le nom de votre dépôt pour cette doc)

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
          sidebarPath: './sidebars.js', // Ce fichier doit exister
          routeBasePath: '/', // La documentation sera à la racine du site
        },
        blog: false, // Pas de blog pour la doc technique
        theme: {
          customCss: './src/css/custom.css', // Pour les styles personnalisés
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg', // Optionnel: remplacez par une image pour les partages sociaux
      navbar: {
        title: 'Doc Technique RAG Fiqh',
        logo: {
          alt: 'Logo Assistant RAG Fiqh',
          src: 'img/logo-light.svg',     // Doit être dans static/img/logo-light.svg
          srcDark: 'img/logo-dark.svg', // Doit être dans static/img/logo-dark.svg
        },
        items: [
          {
            type: 'doc', // MODIFIÉ: type changé
            docId: 'intro', // MODIFIÉ: Fait référence à l'ID du document (qui est le nom du fichier sans extension, ou défini par le slug)
            position: 'left',
            label: 'Documentation Technique',
          },
          {
            href: 'https://github.com/VOTRE_NOM_UTILISATEUR_GITHUB/VOTRE_REPO_PROJET_PRINCIPAL', // **MODIFIEZ CECI**
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
                href: 'URL_DE_VOTRE_DOC_UTILISATEUR_SI_DISPONIBLE', // **MODIFIEZ CECI**
              },
              {
                label: 'Signaler un Problème (Doc Technique)',
                href: 'https://github.com/VOTRE_NOM_UTILISATEUR_GITHUB/assistant-rag-fiqh-docs-technique/issues', // **MODIFIEZ CECI**
              },
            ],
          },
          {
            title: 'Plus',
            items: [
              {
                label: 'Projet Principal (GitHub)',
                href: 'https://github.com/VOTRE_NOM_UTILISATEUR_GITHUB/VOTRE_REPO_PROJET_PRINCIPAL', // **MODIFIEZ CECI**
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Assistant RAG Fiqh - Documentation Technique. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'json', 'bash', 'sql'], // Ajout de langages pour la coloration syntaxique
      },
    }),
};

export default config;