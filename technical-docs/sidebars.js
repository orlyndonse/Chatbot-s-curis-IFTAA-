// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  techDocSidebar: [ // ID de votre sidebar, utilisé dans docusaurus.config.js
    'intro',      // Référence à /docs/intro.md (grâce au slug: /guide/introduction-technique)
    {
      type: 'category',
      label: 'Architecture Générale',
      link: {
        type: 'generated-index',
        title: 'Architecture Générale du Système',
        description: "Vue d'ensemble des composants majeurs et des principaux flux de données de l'application.",
        slug: '/architecture', // URL pour la page d'index de cette catégorie
        keywords: ['architecture', 'flux de données', 'overview'],
      },
      items: [
        'architecture/overview',       // Référence à /docs/architecture/overview.md
        'architecture/data-flows',     // Référence à /docs/architecture/data-flows.md
      ],
    },
    {
      type: 'category',
      label: 'Composant Backend (FastAPI)',
      link: {
        type: 'generated-index',
        title: 'Composant Backend',
        description: "Détails sur l'implémentation du serveur backend avec Python et FastAPI.",
        slug: '/backend',
        keywords: ['backend', 'fastapi', 'python', 'api'],
      },
      items: [
        'backend/structure',
        'backend/entry-point',
        'backend/configuration',
        'backend/middleware',
        'backend/error-handling',
        {
          type: 'category',
          label: 'Modules API Principaux',
          link: {
            type: 'generated-index',
            title: 'Modules API Principaux',
            description: "Description des modules API pour l'authentification et les conversations.",
            slug: '/backend/api-modules',
          },
          items: [
            'backend/api-modules/auth',
            'backend/api-modules/conversations',
          ],
        },
        {
          type: 'category',
          label: 'Interaction Base de Données',
          link: {
            type: 'generated-index',
            title: 'Interaction Base de Données',
            description: "Gestion de la base de données relationnelle (PostgreSQL) et non relationnelle (Redis).",
            slug: '/backend/database-interaction',
          },
          items: [
            'backend/database-interaction/connection-session',
            'backend/database-interaction/models',
            'backend/database-interaction/migrations',
            'backend/database-interaction/redis',
          ],
        },
        {
          type: 'category',
          label: 'Composants RAG',
          link: {
            type: 'generated-index',
            title: 'Composants RAG',
            description: "Détails des modules constituant le pipeline RAG (Retrieval Augmented Generation).",
            slug: '/backend/rag-components',
          },
          items: [
            'backend/rag-components/chain',
            'backend/rag-components/loader',
            'backend/rag-components/vectorstore',
            'backend/rag-components/utils',
          ],
        },
        'backend/dependencies',
      ],
    },
    {
      type: 'category',
      label: 'Composant Frontend (React)',
      link: {
        type: 'generated-index',
        title: 'Composant Frontend',
        description: "Détails sur l'implémentation de l'interface utilisateur avec React et Vite.",
        slug: '/frontend',
        keywords: ['frontend', 'react', 'vite', 'ui'],
      },
      items: [
        'frontend/structure',
        'frontend/config-build',
        'frontend/entry-point',
        'frontend/main-component',
        'frontend/routing',
        'frontend/state-management',
        'frontend/ui-components',
        'frontend/api-communication',
        'frontend/styling',
        'frontend/dependencies',
      ],
    },
    // La section "Base de Données Approfondie" est couverte dans backend/database-interaction
    // et backend/rag-components/vectorstore.md. Si vous voulez toujours une catégorie séparée,
    // décommentez et ajustez. Pour l'instant, je la considère comme intégrée.
    /*
    {
      type: 'category',
      label: 'Base de Données Approfondie',
      link: { type: 'generated-index', slug: '/database-deep-dive' },
      items: [
        'database-deep-dive/relational-db', // Pointe vers un fichier qui pourrait récapituler ou lier vers backend/database-interaction/models.md
        'database-deep-dive/vector-db',     // Pointe vers un fichier qui pourrait récapituler ou lier vers backend/rag-components/vectorstore.md
      ],
    },
    */
    {
      type: 'category',
      label: 'Pipeline RAG Détaillé',
      link: {
        type: 'generated-index',
        title: 'Pipeline RAG Détaillé',
        description: "Explication du fonctionnement du pipeline RAG, de l'ingestion des documents à la génération des réponses.",
        slug: '/rag-pipeline',
      },
      items: [
        'rag-pipeline/ingestion',
        'rag-pipeline/generation',
        'rag-pipeline/initial-indexing',
      ],
    },
    {
      type: 'category',
      label: 'Installation et Configuration',
      link: {
        type: 'generated-index',
        title: 'Installation et Configuration',
        description: "Guides pour mettre en place l'environnement de développement.",
        slug: '/setup-installation',
      },
      items: [
        'setup-installation/prerequisites',
        'setup-installation/backend-setup',
        'setup-installation/frontend-setup',
        'setup-installation/external-services',
      ],
    },
    {
      type: 'category',
      label: 'Déploiement',
      link: {
        type: 'generated-index',
        title: 'Déploiement',
        description: "Considérations pour le déploiement de l'application en production.",
        slug: '/deployment',
      },
      items: ['deployment/general-considerations'],
    },
    {
      type: 'category',
      label: 'Tests',
      link: {
        type: 'generated-index',
        title: 'Tests',
        description: "Informations sur la stratégie de test et l'exécution des tests.",
        slug: '/tests',
      },
      items: ['tests/overview'],
    },
    {
      type: 'category',
      label: 'Documentation Utilisateur',
      link: {
        type: 'generated-index',
        title: 'Documentation Utilisateur',
        description: "Référence et lien vers la documentation destinée aux utilisateurs finaux.",
        slug: '/user-documentation',
      },
      items: ['user-documentation/overview'],
    },
    'future-improvements', // Référence à /docs/future-improvements.md
    'conclusion',          // Référence à /docs/conclusion.md
    {
      type: 'category',
      label: 'Annexe',
      link: {
        type: 'generated-index',
        title: 'Annexe',
        description: "Informations supplémentaires et glossaire.",
        slug: '/appendix',
      },
      items: ['appendix/glossary'], // Référence à /docs/appendix/glossary.md
    },
  ],
};

export default sidebars;