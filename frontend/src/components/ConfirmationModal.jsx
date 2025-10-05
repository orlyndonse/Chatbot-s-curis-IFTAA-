// src/components/ConfirmationModal.jsx

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Icon from './Icon';
import { CircularProgress } from './Progress';

const ConfirmationModal = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = "Confirmer",
  cancelText = "Annuler",
  isLoading = false,
  confirmVariant = 'primary', // 'primary' ou 'destructive'
}) => {

  const confirmButtonClasses = {
    primary: 'bg-light-primary text-light-onPrimary dark:bg-dark-primary dark:text-dark-onPrimary',
    destructive: 'bg-light-error text-light-onError dark:bg-dark-error dark:text-dark-onError',
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh p-6 rounded-xl shadow-xl max-w-md w-full"
            onClick={(e) => e.stopPropagation()} // Empêche la fermeture en cliquant sur la modale
          >
            <div className="flex items-start">
              <div className={`mr-4 flex-shrink-0 grid place-items-center w-10 h-10 rounded-full ${confirmVariant === 'destructive' ? 'bg-light-errorContainer dark:bg-dark-errorContainer' : 'bg-light-primaryContainer dark:bg-dark-primaryContainer'}`}>
                <Icon name={confirmVariant === 'destructive' ? 'delete' : 'help'} size={24} className={confirmVariant === 'destructive' ? 'text-light-error dark:text-dark-error' : 'text-light-primary dark:text-dark-primary'} />
              </div>
              <div className="flex-grow">
                <h2 className="text-titleLarge text-light-onSurface dark:text-dark-onSurface mb-2">{title}</h2>
                <p className="text-bodyMedium text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">{message}</p>
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-6">
              <button
                onClick={onClose}
                className="btn text text-light-primary dark:text-dark-primary"
                disabled={isLoading}
              >
                {cancelText}
                <div className="state-layer"></div>
              </button>
              <button
                onClick={onConfirm}
                className={`btn filled ${confirmButtonClasses[confirmVariant]}`}
                disabled={isLoading}
              >
                {isLoading ? <CircularProgress size="small" /> : confirmText}
                <div className="state-layer"></div>
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ConfirmationModal;