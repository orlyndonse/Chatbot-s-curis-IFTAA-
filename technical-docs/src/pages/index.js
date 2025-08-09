import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css'; // Nous créerons ce fichier CSS ensuite

// Assurez-vous que les chemins vers vos logos sont corrects
// Ils pointent vers static/img/ par défaut
import LogoLight from '@site/static/img/logo-light.svg';
import LogoDark from '@site/static/img/logo-dark.svg';
import { useColorMode } from '@docusaurus/theme-common';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const {colorMode} = useColorMode();

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroLogoContainer}>
          {colorMode === 'dark' ? (
            <LogoDark className={styles.heroLogo} role="img" />
          ) : (
            <LogoLight className={styles.heroLogo} role="img" />
          )}
        </div>
        <h1 className={clsx('hero__title', styles.heroTitleGradient)}>
          {siteConfig.title}
        </h1>
        <p className={clsx('hero__subtitle', styles.heroSubtitle)}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
              className={clsx('button button--lg', styles.heroButtonPrimary)}
              to="/guide/introduction-technique"> {/* MODIFIÉ: Pointe vers le nouveau slug */}
              Explorer la Documentation
            </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Accueil - ${siteConfig.title}`}
      description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <section className={styles.mainContentSection}>
          <div className="container">
            <div className="row">
              <div className={clsx('col col--10 col--offset-1', styles.promoSection)}>
                <h2>Plongez au Cœur du Système</h2>
                <p>
                  Cette documentation technique fournit une analyse approfondie de chaque composant de l'Assistant RAG Fiqh,
                  des API backend aux interactions frontend, en passant par le pipeline RAG et la gestion des données.
                  Elle est destinée aux développeurs et aux contributeurs souhaitant comprendre ou étendre le projet.
                </p>
                <p>
                  Commencez par explorer les sections clés :
                </p>
                <div className={styles.quickLinks}>
                  <Link className={clsx('button button--outline button--md', styles.quickLinkButton)} to="/architecture/overview">
                    Architecture
                  </Link>
                  <Link className={clsx('button button--outline button--md', styles.quickLinkButton)} to="/backend/structure">
                    Détails du Backend
                  </Link>
                  <Link className={clsx('button button--outline button--md', styles.quickLinkButton)} to="/frontend/structure">
                    Détails du Frontend
                  </Link>
                  <Link className={clsx('button button--outline button--md', styles.quickLinkButton)} to="/rag-pipeline/ingestion">
                    Pipeline RAG
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}