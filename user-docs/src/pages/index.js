import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css'; // Uses the CSS module you created

// Import your logos
import LogoLight from '@site/static/img/logo-light.svg';
import LogoDark from '@site/static/img/logo-dark.svg';
import { useColorMode } from '@docusaurus/theme-common';


function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const {colorMode} = useColorMode();

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner, styles.customHeroBanner)}>
      <div className="container">
        <div className={styles.heroLogoContainer}>
          {colorMode === 'dark' ? (
            <LogoDark className={styles.heroLogo} role="img" />
          ) : (
            <LogoLight className={styles.heroLogo} role="img" />
          )}
        </div>
        {/* siteConfig.title and tagline will be pulled from your French docusaurus.config.js */}
        <h1 className={clsx('hero__title', styles.heroTitleGradient)}>
          {siteConfig.title}
        </h1>
        <p className={clsx('hero__subtitle', styles.heroSubtitle)}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className={clsx('button button--lg', styles.heroButtonPrimary)}
            to="/docs/introduction/welcome"> {/* Ensure this path matches your first doc page */}
            Commencer le Guide
          </Link>
          {/* Optional: Link to your main application
          <Link
            className={clsx('button button--secondary button--lg', styles.heroButtonSecondary)}
            to="YOUR_MAIN_APP_URL_HERE">
            Accéder à l'Application
          </Link>
          */}
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      // title will be "Accueil - [Your Site Title in French]"
      title={`Accueil - ${siteConfig.title}`} 
      description={siteConfig.tagline}> {/* Tagline should also be in French from config */}
      <HomepageHeader />
      <main>
        <section className={styles.featuresPlaceholder}>
          <div className="container">
            <div className="row">
              <div className={clsx('col col--10 col--offset-1', styles.promoSection)}>
                <h2>Explorer le Fiqh Maliki avec Clarté</h2>
                <p>
                  Notre assistant RAG est conçu pour vous aider à naviguer et à comprendre vos textes de Fiqh Maliki.
                  Téléversez vos documents, posez vos questions en arabe, et obtenez des réponses contextuelles.
                  Ce guide est là pour vous accompagner à chaque étape.
                </p>
                <p>
                  Plongez dans les sections principales :
                </p>
                <div className={styles.quickLinks}>
                  <Link className={clsx('button button--outline button--md', styles.quickLinkButton)} to="/docs/getting-started/creating-account">Création de Compte</Link>
                  <Link className={clsx('button button--outline button--md', styles.quickLinkButton)} to="/docs/rag-usage/formulating-questions">Poser des Questions Efficaces</Link>
                  <Link className={clsx('button button--outline button--md', styles.quickLinkButton)} to="/docs/documents/how-to-upload">Téléverser des Documents</Link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}