import React from 'react';
import PropTypes from 'prop-types';
import { IconBtn } from '../Button';
import Icon from '../Icon'; 

const DocumentItemCard = ({ 
  document, 
  onDelete, 
  onPreview, 
  isDeleting,
  isActive,
  onToggleActive
}) => {
  const getFileIcon = (mimeType) => {
    if (!mimeType) return 'document'; 
    if (mimeType.includes('pdf')) return 'document-text';
    if (mimeType.includes('text')) return 'document';
    if (mimeType.includes('word')) return 'document-word'; 
    if (mimeType.includes('csv') || mimeType.includes('spreadsheet')) return 'table';
    if (mimeType.includes('presentation')) return 'slideshow';
    if (mimeType.includes('image')) return 'photo';
    if (mimeType.includes('zip') || mimeType.includes('archive')) return 'archive';
    return 'document';
  };

  const fileSizeInKB = document.size ? (document.size / 1024).toFixed(1) : 'N/A';
  const displayName = document.filename && document.filename.length > 35 
    ? `${document.filename.substring(0, 32)}...` 
    : document.filename;

  return (
    <div 
      className={`document-item-card flex items-center p-3 bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh 
                  rounded-lg shadow-sm hover:shadow-md transition-all duration-200 ease-out
                  ${isDeleting ? 'opacity-50 pointer-events-none' : ''}
                  ${isActive ? 'ring-2 ring-light-primary dark:ring-dark-primary' : 'ring-1 ring-transparent'}`}
    >
      {onToggleActive && (
        <button
          title={isActive ? "Désactiver du contexte" : "Activer dans le contexte"}
          className={`mr-2 p-1 rounded ${isActive ? 'text-light-primary dark:text-dark-primary' : 'text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant'}`}
          onClick={() => onToggleActive(document.uid)}
          disabled={isDeleting}
        >
          <Icon name={isActive ? "toggle_on" : "toggle_off"} size={20} />
        </button>
      )}

      <div className="mr-3 flex-shrink-0 text-light-primary dark:text-dark-primary">
        <Icon name={getFileIcon(document.mime_type)} size={28} />
      </div>

      <div className="flex-grow overflow-hidden mr-2">
        <p className="text-bodyMedium font-medium text-light-onSurface dark:text-dark-onSurface truncate" title={document.filename}>
          {displayName}
        </p>
        <p className="text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
          {fileSizeInKB} Ko 
          {document.upload_date && ` - ${new Date(document.upload_date).toLocaleDateString('fr-FR')}`}
        </p>
      </div>

      <div className="flex flex-shrink-0 items-center gap-1">
        {onPreview && (
          <button
            title="Prévisualiser le document"
            className="p-1 rounded hover:bg-light-surfaceContainerHigh dark:hover:bg-dark-surfaceContainerHigh"
            onClick={() => onPreview(document)}
            disabled={isDeleting}
          >
            <Icon name="visibility" size={20} />
          </button>
        )}
        {onDelete && (
          isDeleting ? (
            <div className="w-7 h-7 flex items-center justify-center"> 
              <Icon name="progress_activity" size={20} />
            </div>
          ) : (
            <button
              title="Supprimer le document"
              className="p-1 rounded hover:bg-light-surfaceContainerHigh dark:hover:bg-dark-surfaceContainerHigh hover:text-light-error dark:hover:text-dark-error"
              onClick={() => onDelete(document.uid)}
              disabled={isDeleting}
            >
              <Icon name="delete" size={20} />
            </button>
          )
        )}
      </div>
    </div>
  );
};

DocumentItemCard.propTypes = {
  document: PropTypes.shape({
    uid: PropTypes.string.isRequired,
    filename: PropTypes.string.isRequired,
    mime_type: PropTypes.string,
    size: PropTypes.number,
    upload_date: PropTypes.string,
    isActive: PropTypes.bool,
  }).isRequired,
  onDelete: PropTypes.func,
  onPreview: PropTypes.func,
  isDeleting: PropTypes.bool,
  isActive: PropTypes.bool.isRequired,
  onToggleActive: PropTypes.func.isRequired
};

export default DocumentItemCard;
