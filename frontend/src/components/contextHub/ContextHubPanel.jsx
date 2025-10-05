import React, { useState, useMemo, useContext } from 'react';
import PropTypes from 'prop-types';
import { IconBtn } from '../Button';
import Icon from '../Icon';
import ContextSizeIndicator from './ContextSizeIndicator';
import DocumentUploadArea from './DocumentUploadArea';
import DocumentItemCard from './DocumentItemCard';
import { CircularProgress } from '../Progress';
import DocumentFilters from './DocumentFilters';
import { useLanguage } from '../../contexts/LanguageContext';


const ContextHubPanel = ({
  isOpen,
  onClose,
  title = "Hub de Contexte",
  activeConversationId,
  documents = [],
  onDeleteDocument,
  onPreviewDocument,
  deletingDocumentId,
  isLoading,
  onToggleDocumentActive,
  onFilesAdded,
  isUploading,
  userRole,
  currentContextSize,
  maxContextSize
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOption, setSortOption] = useState('upload_date_desc');
  const { language } = useLanguage();

  const handleSearchTermChange = (term) => {
    setSearchTerm(term);
  };

  const handleSortOptionChange = (option) => {
    setSortOption(option);
  };

  const filteredAndSortedDocuments = useMemo(() => {
    let processedDocs = [...documents];

    if (searchTerm) {
      processedDocs = processedDocs.filter(doc =>
        doc.filename.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    switch (sortOption) {
      case 'filename_asc':
        processedDocs.sort((a, b) => a.filename.localeCompare(b.filename));
        break;
      case 'filename_desc':
        processedDocs.sort((a, b) => b.filename.localeCompare(a.filename));
        break;
      case 'size_asc':
        processedDocs.sort((a, b) => (a.size || 0) - (b.size || 0));
        break;
      case 'size_desc':
        processedDocs.sort((a, b) => (b.size || 0) - (a.size || 0));
        break;
      case 'upload_date_asc':
        processedDocs.sort((a, b) => new Date(a.upload_date) - new Date(b.upload_date));
        break;
      case 'upload_date_desc':
      default:
        processedDocs.sort((a, b) => new Date(b.upload_date) - new Date(a.upload_date));
        break;
    }
    return processedDocs;
  }, [documents, searchTerm, sortOption]);

  const activeDocumentsCount = filteredAndSortedDocuments.filter(doc => doc.isActiveInContext).length;

  const isRTL = language === 'ar';
  const panelPositionClass = isRTL ? 'left-0' : 'right-0';
  const panelTransformClass = isRTL ? 
    (isOpen ? 'translate-x-0' : '-translate-x-full') : 
    (isOpen ? 'translate-x-0' : 'translate-x-full');

  return (
    <div className={`context-hub-panel ${panelPositionClass} ${panelTransformClass}`}>
      <div className="context-hub-header">
        <h2 className="text-titleLarge font-medium truncate pr-2" title={title}>{title}</h2>
        <button
          title="Fermer le panneau"
          className="p-2 rounded hover:bg-light-surfaceContainerHigh dark:hover:bg-dark-surfaceContainerHigh"
          onClick={onClose}
        >
          <Icon name="close" size={20} />
        </button>
      </div>
      
      <div className="context-hub-content">
        {/* Zone d'upload - visible seulement pour les admins avec une conversation active */}
        {userRole === 'admin' && activeConversationId && onFilesAdded && (
          <div className="px-4 pt-4">
            <DocumentUploadArea
              onFilesAdded={onFilesAdded}
              isUploading={isUploading}
              supportedFormats=".pdf,.txt,.docx,.csv,.html"
            />
          </div>
        )}

        {/* Indicateur de taille du contexte pour les admins */}
        {userRole === 'admin' && currentContextSize !== undefined && maxContextSize !== undefined && (
          <div className="px-4">
            <ContextSizeIndicator
              currentSize={currentContextSize}
              maxSize={maxContextSize}
            />
          </div>
        )}

        {/* Filtres - affichés seulement s'il y a des documents et pas de loading initial */}
        {activeConversationId && documents.length > 0 && !isLoading && (
          <div className="px-4 pt-4">
            <DocumentFilters
              searchTerm={searchTerm}
              onSearchTermChange={handleSearchTermChange}
              sortOption={sortOption}
              onSortOptionChange={handleSortOptionChange}
            />
          </div>
        )}

        {/* Liste des documents */}
        <div className="px-4 pb-4 pt-3 flex-grow overflow-y-auto space-y-3">
          {isLoading && !filteredAndSortedDocuments.length ? (
            <div className="flex flex-col justify-center items-center h-full">
              <CircularProgress size="large" />
              <p className="mt-3 text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
                Chargement des documents...
              </p>
            </div>
          ) : filteredAndSortedDocuments.length > 0 ? (
            filteredAndSortedDocuments.map(doc => (
              <DocumentItemCard
                key={doc.uid}
                document={doc}
                isActive={doc.isActiveInContext}
                onToggleActive={onToggleDocumentActive}
                onDelete={onDeleteDocument}
                onPreview={onPreviewDocument}
                isDeleting={deletingDocumentId === doc.uid}
              />
            ))
          ) : !isLoading && activeConversationId && searchTerm && documents.length > 0 ? (
            <p className="text-bodyMedium text-center text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant pt-10">
              Aucun document ne correspond à votre recherche pour "{searchTerm}".
            </p>
          ) : !isLoading && activeConversationId && documents.length === 0 ? (
            <div className="text-center pt-10">
              <p className="text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
                Aucun document disponible pour cette conversation.
              </p>
              {userRole === 'admin' && (
                <p className="text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mt-2">
                  Utilisez la zone d'upload ci-dessus pour ajouter des documents.
                </p>
              )}
            </div>
          ) : !isLoading && !activeConversationId ? (
            <p className="text-bodyMedium text-center text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant pt-10">
              Sélectionnez une conversation pour voir ses documents.
            </p>
          ) : null}
        </div>

        {/* Footer avec statistiques */}
        {documents.length > 0 && (
          <div className="p-4 border-t border-light-outline/20 dark:border-dark-outline/20">
            <p className="text-bodySmall text-center text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
              {activeDocumentsCount} sur {filteredAndSortedDocuments.length} document(s) actif(s) (affichage de {filteredAndSortedDocuments.length} sur {documents.length} au total).
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

ContextHubPanel.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  title: PropTypes.string,
  currentContextSize: PropTypes.number,
  maxContextSize: PropTypes.number,
  onFilesAdded: PropTypes.func,
  isUploading: PropTypes.bool,
  activeConversationId: PropTypes.string,
  documents: PropTypes.arrayOf(PropTypes.shape({
    uid: PropTypes.string.isRequired,
    filename: PropTypes.string,
    mime_type: PropTypes.string,
    size: PropTypes.number,
    upload_date: PropTypes.string,
    isActiveInContext: PropTypes.bool
  })),
  onDeleteDocument: PropTypes.func,
  onPreviewDocument: PropTypes.func,
  deletingDocumentId: PropTypes.string,
  isLoading: PropTypes.bool,
  onToggleDocumentActive: PropTypes.func,
  userRole: PropTypes.string,
};

export default ContextHubPanel;