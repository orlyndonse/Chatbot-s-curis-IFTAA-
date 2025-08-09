// source code/frontend/src/components/contextHub/DocumentUploadArea.jsx
import React, { useCallback } from 'react';
import PropTypes from 'prop-types';
import { useDropzone } from 'react-dropzone';
import { IconBtn } from '../Button'; // Assuming Button.jsx is in src/components/
import { CircularProgress } from '../Progress'; // Assuming Progress.jsx is in src/components/
import Icon from '../Icon';

const DocumentUploadArea = ({ onFilesAdded, isUploading, supportedFormats = ".pdf,.txt,.docx,.csv,.html" }) => {
  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      onFilesAdded(acceptedFiles);
    }
  }, [onFilesAdded]);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    noClick: true, // We'll use our own button to open the dialog
    noKeyboard: true,
    disabled: isUploading,
    accept: supportedFormats ? supportedFormats.split(',').reduce((acc, ext) => {
        // Basic mapping, you might need more specific MIME types for robust validation
        if (ext === '.pdf') acc['application/pdf'] = [];
        else if (ext === '.txt') acc['text/plain'] = [];
        else if (ext === '.docx') acc['application/vnd.openxmlformats-officedocument.wordprocessingml.document'] = [];
        else if (ext === '.doc') acc['application/msword'] = [];
        else if (ext === '.csv') acc['text/csv'] = [];
        else if (ext === '.html') acc['text/html'] = [];
        else acc[ext] = []; // Fallback for other extensions
        return acc;
    }, {}) : undefined,
  });

  return (
    <div
      {...getRootProps()}
      className={`document-upload-area p-4 border-2 border-dashed rounded-lg text-center cursor-pointer
        transition-colors duration-200 ease-out
        ${isUploading ? 'opacity-60 cursor-not-allowed' : ''}
        ${isDragActive 
          ? 'border-light-primary dark:border-dark-primary bg-light-primaryContainer/30 dark:bg-dark-primaryContainer/30' 
          : 'border-light-outline dark:border-dark-outline hover:border-light-primary/70 dark:hover:border-dark-primary/70'
        }`}
    >
      <input {...getInputProps()} />
      {isUploading ? (
        <div className="flex flex-col items-center justify-center py-6">
          <CircularProgress size="large" />
          <p className="mt-3 text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
            Traitement des fichiers...
          </p>
        </div>
      ) : (
        <div className="flex flex-col items-center">
          <Icon name="cloud_upload" size={48} className="text-4xl text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-2" />
          {isDragActive ? (
            <p className="text-bodyLarge text-light-primary dark:text-dark-primary">Déposez les fichiers ici...</p>
          ) : (
            <>
              <p className="text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-2">
                Glissez-déposez les fichiers ou
              </p>
              <button
                type="button"
                onClick={open} // Trigger file dialog
                className="btn text text-light-primary dark:text-dark-primary mb-2 text-labelLarge" // Using your button styles
                disabled={isUploading}
              >
                Parcourir les fichiers
                <div className="state-layer"></div>
              </button>
              <p className="text-bodySmall text-light-onSurfaceVariant/70 dark:text-dark-onSurfaceVariant/70">
                Formats pris en charge : {supportedFormats.replace(/,/g, ', ')}
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
};

DocumentUploadArea.propTypes = {
  onFilesAdded: PropTypes.func.isRequired,
  isUploading: PropTypes.bool,
  supportedFormats: PropTypes.string,
};

export default DocumentUploadArea;