import React, { useState, useCallback } from 'react';
import { useLoaderData } from 'react-router-dom';
import PageTitle from '../components/PageTitle';
import { useSnackbar } from '../hooks/useSnackbar';
import { fetchWithAuth } from '../utils/fetchWithAuth';
import Icon from '../components/Icon';
import { CircularProgress } from '../components/Progress';
import ConfirmationModal from '../components/ConfirmationModal';

// Composant pour la zone d'upload de documents
const DocumentUploadArea = ({ onFilesAdded, isUploading }) => {
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      onFilesAdded(files);
    }
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      onFilesAdded(files);
    }
  };

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
        dragOver
          ? 'border-light-primary dark:border-dark-primary bg-light-primaryContainer/20 dark:bg-dark-primaryContainer/20'
          : 'border-light-outline dark:border-dark-outline'
      } ${isUploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:border-light-primary dark:hover:border-dark-primary'}`}
      onDrop={handleDrop}
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onClick={() => !isUploading && document.getElementById('file-upload-admin').click()}
    >
      <input
        id="file-upload-admin"
        type="file"
        multiple
        className="hidden"
        onChange={handleFileSelect}
        disabled={isUploading}
        accept=".pdf,.doc,.docx,.txt,.md,.json,.csv,.xlsx,.xls"
      />
      
      {isUploading ? (
        <div className="flex flex-col items-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-light-primary dark:border-dark-primary mb-2"></div>
          <p className="text-light-onSurface dark:text-dark-onSurface">Upload en cours...</p>
        </div>
      ) : (
        <div>
          <p className="text-light-onSurface dark:text-dark-onSurface mb-2">
            Glissez vos fichiers ici ou cliquez pour sélectionner
          </p>
          <p className="text-sm text-light-onSurface/60 dark:text-dark-onSurface/60">
            PDF, DOC, TXT, MD, JSON, CSV, XLSX acceptés
          </p>
        </div>
      )}
    </div>
  );
};

// Modale pour lister et gérer les documents
const ManageDocsModal = ({ isOpen, onClose, user, documents, isLoading, onDeleteDocument }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-light-surface dark:bg-dark-surface p-6 rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-titleLarge text-light-onSurface dark:text-dark-onSurface">Documents de {user?.email}</h2>
          <button 
            onClick={onClose} 
            className="text-light-onSurface dark:text-dark-onSurface hover:bg-light-surfaceContainer dark:hover:bg-dark-surfaceContainer p-2 rounded-full transition-colors"
          >
            <Icon name="close" size={20} />
          </button>
        </div>
        <div className="flex-grow overflow-y-auto pr-2">
          {isLoading ? (
            <div className="flex justify-center items-center h-48">
              <CircularProgress size="large" />
            </div>
          ) : documents.length === 0 ? (
            <p className="text-center text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant py-10">Cet utilisateur n'a aucun document.</p>
          ) : (
            <ul className="space-y-2">
              {documents.map(doc => (
                <li key={doc.uid} className="flex items-center justify-between p-3 bg-light-surfaceContainer dark:bg-dark-surfaceContainer rounded-lg">
                  <div className="flex-grow overflow-hidden">
                    <p className="font-medium truncate text-light-onSurface dark:text-dark-onSurface" title={doc.filename}>{doc.filename}</p>
                    <p className="text-sm text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant">
                      {(doc.size / 1024).toFixed(1)} Ko - Ajouté le {new Date(doc.upload_date).toLocaleDateString('fr-FR')}
                    </p>
                  </div>
                  <button 
                    onClick={() => onDeleteDocument(doc.uid, doc.filename)} 
                    className="ml-4 flex-shrink-0 p-2 text-light-error dark:text-dark-error hover:bg-light-errorContainer/50 dark:hover:bg-dark-errorContainer/50 rounded-full transition-colors"
                  >
                    <Icon name="delete" size={20} />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

// Composant pour afficher une ligne utilisateur
const UserRow = ({ user, onDelete, onUpdateRole, onOpenUpload, onManageDocs }) => {
  return (
    <tr className="border-b border-light-outline/20 dark:border-dark-outline/20 hover:bg-light-surfaceContainer dark:hover:bg-dark-surfaceContainer">
      <td className="p-3">{user.first_name} {user.last_name}</td>
      <td className="p-3">{user.email}</td>
      <td className="p-3">{user.role}</td>
      <td className="p-3">{new Date(user.created_at).toLocaleDateString('fr-FR')}</td>
      <td className={`p-3 ${user.is_verified ? 'text-green-600' : 'text-yellow-600'}`}>
        {user.is_verified ? 'Oui' : 'Non'}
      </td>
      <td className="p-3">
        <div className="flex gap-2 flex-wrap">
          {/* Bouton Gérer Documents */}
          <button
            onClick={onManageDocs}
            className="text-sm px-3 py-1 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors"
          >
            Gérer Docs
          </button>
          
          {/* Bouton Ajouter Documents */}
          <button 
            onClick={onOpenUpload} 
            className="text-sm px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors"
          >
            Ajouter Docs
          </button>
          
          <button 
            onClick={onUpdateRole}
            className="text-sm px-3 py-1 rounded-full bg-light-primaryContainer dark:bg-dark-primaryContainer text-light-primary dark:text-dark-primary hover:bg-light-primaryContainer/80 dark:hover:bg-dark-primaryContainer/80 transition-colors"
          >
            Changer Rôle
          </button>
          
          <button 
            onClick={onDelete}
            className="text-sm px-3 py-1 rounded-full bg-light-errorContainer dark:bg-dark-errorContainer text-light-error dark:text-dark-error hover:bg-light-errorContainer/80 dark:hover:bg-dark-errorContainer/80 transition-colors"
          >
            Supprimer
          </button>
        </div>
      </td>
    </tr>
  );
};

const AdminUserManagement = () => {
  const { users: initialUsers } = useLoaderData();
  const [users, setUsers] = useState(initialUsers);
  const { showSnackbar } = useSnackbar();
  
  // États pour la modale d'upload
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedUserForUpload, setSelectedUserForUpload] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  // États pour la gestion des documents
  const [isDocsModalOpen, setIsDocsModalOpen] = useState(false);
  const [selectedUserForDocs, setSelectedUserForDocs] = useState(null);
  const [userDocuments, setUserDocuments] = useState([]);
  const [isLoadingDocs, setIsLoadingDocs] = useState(false);

  // la modale de confirmation
  const [confirmationState, setConfirmationState] = useState({
    isOpen: false,
    title: '',
    message: '',
    onConfirm: () => {},
    isLoading: false,
    confirmVariant: 'primary',
    confirmText: 'Confirmer',
  });

  const closeConfirmationModal = useCallback(() => {
    setConfirmationState({
      isOpen: false,
      title: '',
      message: '',
      onConfirm: () => {},
      isLoading: false,
      confirmVariant: 'primary',
      confirmText: 'Confirmer',
    });
  }, []);

  // LOGIQUE DE SUPPRESSION D'UTILISATEUR
  const performDeleteUser = async (userUid) => {
    setConfirmationState(prev => ({ ...prev, isLoading: true }));
    try {
      await fetchWithAuth(`/api/v1/admin/users/${userUid}`, { method: 'DELETE' });
      setUsers(prev => prev.filter(u => u.uid !== userUid));
      showSnackbar({ message: "Utilisateur supprimé avec succès.", type: 'success' });
    } catch (error) {
      showSnackbar({ message: "Erreur lors de la suppression.", type: 'error' });
    } finally {
      closeConfirmationModal();
    }
  };

  const handleDeleteUser = (userUid, userEmail) => {
    setConfirmationState({
      isOpen: true,
      title: "Supprimer l'utilisateur ?",
      message: `Vous êtes sur le point de supprimer définitivement "${userEmail}". Toutes ses données seront effacées. Cette action est irréversible.`,
      onConfirm: () => performDeleteUser(userUid),
      isLoading: false,
      confirmVariant: 'destructive',
      confirmText: 'Supprimer',
    });
  };

  // LOGIQUE DE CHANGEMENT DE RÔLE
  const performUpdateRole = async (userUid, newRole) => {
    setConfirmationState(prev => ({ ...prev, isLoading: true }));
    try {
      const updatedUser = await fetchWithAuth(`/api/v1/admin/users/${userUid}/role`, {
        method: 'PATCH',
        body: JSON.stringify({ role: newRole }),
      });
      setUsers(prev => prev.map(u => u.uid === userUid ? updatedUser : u));
      showSnackbar({ message: `Rôle mis à jour en "${newRole}".`, type: 'success' });
    } catch (error) {
      showSnackbar({ message: "Erreur lors de la mise à jour du rôle.", type: 'error' });
    } finally {
      closeConfirmationModal();
    }
  };

  const handleUpdateRole = (userUid, userEmail, newRole) => {
    setConfirmationState({
      isOpen: true,
      title: "Changer le rôle ?",
      message: `Voulez-vous vraiment changer le rôle de "${userEmail}" en "${newRole}" ?`,
      onConfirm: () => performUpdateRole(userUid, newRole),
      isLoading: false,
      confirmVariant: 'primary',
      confirmText: 'Confirmer',
    });
  };

  // LOGIQUE DE SUPPRESSION DE DOCUMENT
  const performDeleteDocument = async (docUid) => {
    setConfirmationState(prev => ({ ...prev, isLoading: true }));
    try {
      await fetchWithAuth(`/api/v1/admin/users/${selectedUserForDocs.uid}/documents/${docUid}`, { method: 'DELETE' });
      setUserDocuments(prev => prev.filter(d => d.uid !== docUid));
      showSnackbar({ message: "Document supprimé avec succès.", type: 'success' });
    } catch (error) {
      showSnackbar({ message: "Erreur lors de la suppression du document.", type: 'error' });
    } finally {
      closeConfirmationModal();
    }
  };
  
  const handleDeleteDocument = (docUid, docFilename) => {
    setConfirmationState({
      isOpen: true,
      title: "Supprimer le document ?",
      message: `Le document "${docFilename}" sera supprimé de manière permanente. Cette action est irréversible.`,
      onConfirm: () => performDeleteDocument(docUid),
      isLoading: false,
      confirmVariant: 'destructive',
      confirmText: 'Supprimer',
    });
  };

  // Fonctions pour la gestion des documents
  const openDocsModal = useCallback(async (user) => {
    setSelectedUserForDocs(user);
    setIsDocsModalOpen(true);
    setIsLoadingDocs(true);
    try {
      const docs = await fetchWithAuth(`/api/v1/admin/users/${user.uid}/documents`);
      setUserDocuments(Array.isArray(docs) ? docs : []);
    } catch (error) {
      showSnackbar({ message: "Erreur lors du chargement des documents.", type: 'error' });
      setUserDocuments([]);
    } finally {
      setIsLoadingDocs(false);
    }
  }, [showSnackbar]);

  const closeDocsModal = () => {
    setIsDocsModalOpen(false);
    setSelectedUserForDocs(null);
    setUserDocuments([]);
  };

  // Fonctions existantes pour l'upload
  const openUploadModal = (user) => {
    setSelectedUserForUpload(user);
    setIsUploadModalOpen(true);
  };

  const closeUploadModal = () => {
    setIsUploadModalOpen(false);
    setSelectedUserForUpload(null);
    setIsUploading(false);
  };

  const handleFilesAdded = async (files) => {
    if (!selectedUserForUpload || files.length === 0) return;
    
    setIsUploading(true);
    
    try {
      const formData = new FormData();
      files.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetchWithAuth(
        `/api/v1/admin/users/${selectedUserForUpload.uid}/upload`,
        {
          method: 'POST',
          body: formData,
        }
      );

      if (response.errors && response.errors.length > 0) {
        showSnackbar({ 
          message: `Upload partiellement réussi. Erreurs: ${response.errors.join(', ')}`, 
          type: 'warning' 
        });
      } else {
        showSnackbar({ 
          message: `${files.length} document(s) ajouté(s) avec succès pour ${selectedUserForUpload.email}`, 
          type: 'success' 
        });
      }

      closeUploadModal();
    } catch (error) {
      console.error('Erreur lors de l\'upload:', error);
      showSnackbar({ 
        message: `Erreur lors de l'upload: ${error.message}`, 
        type: 'error' 
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="p-6">
      <PageTitle title="Gestion des Utilisateurs" />
      <h1 className="text-headlineSmall mb-4">Gestion des Utilisateurs</h1>
      
      <div className="overflow-x-auto rounded-lg border border-light-outline/20 dark:border-dark-outline/20">
        <table className="w-full text-left text-bodyMedium text-light-onSurface dark:text-dark-onSurface">
          <thead className="bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh">
            <tr>
              <th className="p-3">Nom</th>
              <th className="p-3">Email</th>
              <th className="p-3">Rôle</th>
              <th className="p-3">Inscrit le</th>
              <th className="p-3">Vérifié</th>
              <th className="p-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <UserRow 
                key={user.uid} 
                user={user} 
                onDelete={() => handleDeleteUser(user.uid, user.email)} 
                onUpdateRole={() => handleUpdateRole(user.uid, user.email, user.role === 'admin' ? 'user' : 'admin')}
                onOpenUpload={() => openUploadModal(user)}
                onManageDocs={() => openDocsModal(user)}
              />
            ))}
          </tbody>
        </table>
      </div>

      {/* Modale d'Upload */}
      {isUploadModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-light-surface dark:bg-dark-surface p-6 rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-titleLarge text-light-onSurface dark:text-dark-onSurface">
                Ajouter des documents pour
              </h2>
              <button
                onClick={closeUploadModal}
                className="text-light-onSurface dark:text-dark-onSurface hover:bg-light-surfaceContainer dark:hover:bg-dark-surfaceContainer p-2 rounded-full transition-colors"
                disabled={isUploading}
              >
                <Icon name="close" size={20} />
              </button>
            </div>
            
            <div className="mb-4 p-3 bg-light-surfaceContainer dark:bg-dark-surfaceContainer rounded-lg">
              <p className="text-bodyMedium text-light-onSurface dark:text-dark-onSurface">
                <span className="font-medium">{selectedUserForUpload?.first_name} {selectedUserForUpload?.last_name}</span>
              </p>
              <p className="text-bodySmall text-light-onSurface/60 dark:text-dark-onSurface/60">
                {selectedUserForUpload?.email}
              </p>
            </div>

            <DocumentUploadArea 
              onFilesAdded={handleFilesAdded} 
              isUploading={isUploading} 
            />
            
            <div className="flex justify-end gap-3 mt-6">
              <button 
                onClick={closeUploadModal} 
                className="px-4 py-2 text-light-onSurface dark:text-dark-onSurface hover:bg-light-surfaceContainer dark:hover:bg-dark-surfaceContainer rounded-full transition-colors"
                disabled={isUploading}
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modale de Gestion des Documents */}
      <ManageDocsModal
        isOpen={isDocsModalOpen}
        onClose={closeDocsModal}
        user={selectedUserForDocs}
        documents={userDocuments}
        isLoading={isLoadingDocs}
        onDeleteDocument={handleDeleteDocument}
      />

      {/* Modale de Confirmation */}
      <ConfirmationModal
        isOpen={confirmationState.isOpen}
        onClose={closeConfirmationModal}
        onConfirm={confirmationState.onConfirm}
        title={confirmationState.title}
        message={confirmationState.message}
        isLoading={confirmationState.isLoading}
        confirmVariant={confirmationState.confirmVariant}
        confirmText={confirmationState.confirmText}
      />
    </div>
  );
};

export default AdminUserManagement;