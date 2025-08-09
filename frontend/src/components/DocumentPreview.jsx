// Fixed version of DocumentPreview.jsx
import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { CircularProgress } from './Progress';
import { Button } from './Button';
import { IconBtn } from './Button';

const DocumentPreview = ({ document, isLoading: isLoadingContent, onClose, onAdd }) => {
  const [objectUrl, setObjectUrl] = useState(null);

  useEffect(() => {
    let currentObjectUrl = null;
    if (document && document.type && document.type.includes('pdf') && document.file instanceof Blob) {
      currentObjectUrl = URL.createObjectURL(document.file);
      setObjectUrl(currentObjectUrl);
    } else if (document && document.url) {
        setObjectUrl(document.url);
    } else {
        setObjectUrl(null);
    }

    return () => {
      if (currentObjectUrl) {
        URL.revokeObjectURL(currentObjectUrl);
        setObjectUrl(null);
      }
    };
  }, [document]);

  let previewContentElement = null;

  if (isLoadingContent) {
    previewContentElement = (
      <div className="flex flex-col justify-center items-center h-full text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
        <CircularProgress size="large" />
        <p className="mt-3 text-bodyMedium">Chargement de l'aperçu...</p>
      </div>
    );
  } else if (document && document.error) {
    previewContentElement = (
        <div className="flex flex-col justify-center items-center h-full text-center p-4">
          <Icon name="error" size={48} className="text-5xl text-light-error dark:text-dark-error mb-3" />
          <p className="text-bodyLarge text-light-error dark:text-dark-error">{document.error}</p>
        </div>
      );
  } else if (document && document.type) {
    if (document.type.includes('text/')) {
      previewContentElement = (
        <div className="prose prose-sm dark:prose-invert max-w-full overflow-y-auto h-full p-2 bg-light-surfaceContainer dark:bg-dark-surfaceContainer rounded">
          <pre className="whitespace-pre-wrap break-words text-sm text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
            {document.previewContent || document.name || "Contenu texte non disponible."}
          </pre>
        </div>
      );
    } else if (document.type.includes('pdf') && objectUrl) {
      // FIXED: Better PDF iframe handling with proper container sizing
      previewContentElement = (
        <div className="h-full w-full bg-white dark:bg-gray-800 rounded overflow-hidden">
          <iframe 
            src={`${objectUrl}#view=FitH&toolbar=1&navpanes=1&scrollbar=1`}
            type="application/pdf" 
            width="100%" 
            height="100%" 
            title={`Aperçu de ${document.name || 'document'}`} 
            className="border-0 block"
            style={{ 
              border: 'none',
              outline: 'none'
            }}
            frameBorder="0"
          >
            <div className="flex flex-col justify-center items-center h-full p-4 text-center">
              <span className="material-symbols-rounded text-5xl text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-3">
                picture_as_pdf
              </span>
              <p className="text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-2">
                Votre navigateur ne supporte pas l'affichage des PDF intégrés.
              </p>
              <a 
                href={objectUrl} 
                download={document.name}
                className="text-light-primary dark:text-dark-primary underline"
              >
                Télécharger le PDF pour le voir
              </a>
            </div>        
          </iframe>
        </div>
      );
    } else if (document.type.startsWith('image/') && objectUrl) {
        previewContentElement = (
            <div className="h-full w-full overflow-hidden flex justify-center items-center bg-gray-200 dark:bg-gray-700 rounded">
                <img 
                    src={objectUrl} 
                    alt={`Aperçu de ${document.name || 'image'}`} 
                    className="max-w-full max-h-full object-contain"
                />
            </div>
        );
    } else {
      previewContentElement = (
        <div className="flex flex-col justify-center items-center h-full text-center p-4">
           <span className="material-symbols-rounded text-5xl text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-3">
            visibility_off
          </span>
          <p className="text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
            Aperçu non disponible pour '{document.name || 'ce type de document'}' ({document.type || 'type inconnu'}).
          </p>
        </div>
      );
    }
  } else {
    previewContentElement = (
        <div className="flex justify-center items-center h-full">
          <p className="text-bodyLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">Aucun document sélectionné pour l'aperçu.</p>
        </div>
      );
  }
  
  const actionButtonText = document?.isActiveInContext ? "Désactiver du Contexte" : "Activer dans le Contexte";

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4 backdrop-blur-sm" onClick={onClose}>
      <div 
        className="bg-light-surfaceContainerLow dark:bg-dark-surfaceContainerLow p-4 sm:p-6 rounded-xl shadow-2xl w-full max-w-4xl h-[85vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4 pb-3 border-b border-light-outline/20 dark:border-dark-outline/20 flex-shrink-0">
          <h3 className="text-titleLarge font-medium text-light-onSurface dark:text-dark-onSurface truncate pr-2" title={document?.name}>
            {document?.name || "Aperçu du Document"}
          </h3>
          <IconBtn icon="close" title="Fermer" onClick={onClose} size="small"/>
        </div>
        
        {/* FIXED: Properly sized preview area */}
        <div className="flex-1 overflow-hidden bg-light-surface dark:bg-dark-surface rounded-md">
            {previewContentElement}
        </div>
        
        <div className="mt-4 pt-4 border-t border-light-outline/20 dark:border-dark-outline/20 flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-3 flex-shrink-0">
          <Button 
            onClick={onAdd} 
            variant={document?.isActiveInContext ? "outlined" : "filled"}
            color="primary"
            disabled={isLoadingContent || !document || !!document.error || !document.uid}
            classes="w-full sm:w-auto"
          >
            {actionButtonText}
          </Button>
          <Button
            onClick={onClose}
            variant="filled"
            color="primary"
            classes="w-full sm:w-auto"
          >
            Fermer
          </Button>
        </div>
      </div>
    </div>
  );
};

DocumentPreview.propTypes = {
  document: PropTypes.shape({
    uid: PropTypes.string,
    name: PropTypes.string,
    type: PropTypes.string,
    file: PropTypes.instanceOf(Blob),
    url: PropTypes.string,
    previewContent: PropTypes.string,
    error: PropTypes.string,
    isActiveInContext: PropTypes.bool,
    objectUrl: PropTypes.string,
  }),
  isLoading: PropTypes.bool,
  onClose: PropTypes.func.isRequired,
  onAdd: PropTypes.func.isRequired,
};

export default DocumentPreview;
