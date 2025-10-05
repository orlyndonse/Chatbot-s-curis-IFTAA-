import { useState } from 'react';
import { useNavigate, useLoaderData } from 'react-router-dom';
import { motion } from 'framer-motion';
import PageTitle from '../components/PageTitle';
import { IconBtn } from '../components/Button';
import { useSnackbar } from '../hooks/useSnackbar';
import { fetchWithAuth } from '../utils/fetchWithAuth';
import { CircularProgress } from '../components/Progress';

const Profile = () => {
  const { user } = useLoaderData();
  const navigate = useNavigate();
  const { showSnackbar } = useSnackbar();

  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isSavingProfile, setIsSavingProfile] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [isSavingPassword, setIsSavingPassword] = useState(false);
  const [isDeletingAccount, setIsDeletingAccount] = useState(false);
  const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);

  const [profileData, setProfileData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    username: user?.username || '',
  });

  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_new_password: '',
  });

  const handleProfileChange = (field, value) => {
    setProfileData(prev => ({ ...prev, [field]: value }));
  };

  const handlePasswordChange = (field, value) => {
    setPasswordData(prev => ({ ...prev, [field]: value }));
  };

  const handleSaveProfile = async () => {
    setIsSavingProfile(true);
    try {
      await fetchWithAuth('/api/v1/auth/me/profile', {
        method: 'PUT',
        body: JSON.stringify(profileData),
      });
      
      showSnackbar({ message: 'Profil mis à jour avec succès', type: 'success' });
      setIsEditingProfile(false);
      window.location.reload();
    } catch (error) {
      showSnackbar({ 
        message: error.data?.detail || 'Erreur lors de la mise à jour du profil', 
        type: 'error' 
      });
    } finally {
      setIsSavingProfile(false);
    }
  };

  const handleSavePassword = async () => {
    if (passwordData.new_password !== passwordData.confirm_new_password) {
      showSnackbar({ message: 'Les mots de passe ne correspondent pas', type: 'error' });
      return;
    }

    setIsSavingPassword(true);
    try {
      await fetchWithAuth('/api/v1/auth/me/change-password', {
        method: 'PUT',
        body: JSON.stringify(passwordData),
      });
      
      showSnackbar({ message: 'Mot de passe modifié avec succès', type: 'success' });
      setIsChangingPassword(false);
      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_new_password: '',
      });
    } catch (error) {
      showSnackbar({ 
        message: error.data?.detail || 'Erreur lors du changement de mot de passe', 
        type: 'error' 
      });
    } finally {
      setIsSavingPassword(false);
    }
  };

  const handleDeleteAccount = async () => {
    setIsDeletingAccount(true);
    try {
      await fetchWithAuth('/api/v1/auth/me/account', {
        method: 'DELETE',
      });
      
      showSnackbar({ message: 'Compte supprimé avec succès', type: 'success' });
      
      // Nettoyer les tokens et rediriger
      localStorage.removeItem('awesomeLeadsToken');
      localStorage.removeItem('awesomeLeadsRefreshToken');
      
      setTimeout(() => {
        navigate('/login');
      }, 1000);
      
    } catch (error) {
      showSnackbar({ 
        message: error.data?.detail || 'Erreur lors de la suppression du compte', 
        type: 'error' 
      });
      setIsDeletingAccount(false);
    }
  };

  return (
    <>
      <PageTitle title="Mon Profil" />
      <div className="min-h-screen bg-light-background dark:bg-dark-background">
        <header className="flex items-center h-16 px-4 border-b border-light-outline/20 dark:border-dark-outline/20">
          <IconBtn
            icon="arrow_back"
            title="Retour"
            onClick={() => navigate('/')}
          />
          <h1 className="ml-4 text-headlineSmall text-light-onSurface dark:text-dark-onSurface">
            Mon Profil
          </h1>
        </header>

        <div className="max-w-2xl mx-auto p-6 space-y-6">
          {/* Section Informations Personnelles */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-light-surface dark:bg-dark-surface rounded-lg p-6 shadow-sm"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-titleLarge text-light-onSurface dark:text-dark-onSurface">
                Informations personnelles
              </h2>
              {!isEditingProfile && (
                <IconBtn
                  icon="edit"
                  title="Modifier"
                  onClick={() => setIsEditingProfile(true)}
                />
              )}
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={user?.email || ''}
                  disabled
                  className="w-full p-3 rounded bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest text-light-onSurface dark:text-dark-onSurface opacity-50 cursor-not-allowed"
                />
                <p className="text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mt-1">
                  L'email ne peut pas être modifié
                </p>
              </div>

              <div>
                <label className="block text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                  Prénom
                </label>
                <input
                  type="text"
                  value={profileData.first_name}
                  onChange={(e) => handleProfileChange('first_name', e.target.value)}
                  disabled={!isEditingProfile}
                  className="w-full p-3 rounded bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest text-light-onSurface dark:text-dark-onSurface disabled:opacity-50"
                />
              </div>

              <div>
                <label className="block text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                  Nom
                </label>
                <input
                  type="text"
                  value={profileData.last_name}
                  onChange={(e) => handleProfileChange('last_name', e.target.value)}
                  disabled={!isEditingProfile}
                  className="w-full p-3 rounded bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest text-light-onSurface dark:text-dark-onSurface disabled:opacity-50"
                />
              </div>

              <div>
                <label className="block text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                  Nom d'utilisateur
                </label>
                <input
                  type="text"
                  value={profileData.username}
                  onChange={(e) => handleProfileChange('username', e.target.value)}
                  disabled={!isEditingProfile}
                  maxLength={8}
                  className="w-full p-3 rounded bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest text-light-onSurface dark:text-dark-onSurface disabled:opacity-50"
                />
              </div>

              {isEditingProfile && (
                <div className="flex gap-2 justify-end pt-2">
                  <button
                    onClick={() => {
                      setIsEditingProfile(false);
                      setProfileData({
                        first_name: user?.first_name || '',
                        last_name: user?.last_name || '',
                        username: user?.username || '',
                      });
                    }}
                    className="px-4 py-2 rounded bg-light-secondaryContainer text-light-onSecondaryContainer dark:bg-dark-secondaryContainer dark:text-dark-onSecondaryContainer hover:opacity-90"
                    disabled={isSavingProfile}
                  >
                    Annuler
                  </button>
                  <button
                    onClick={handleSaveProfile}
                    disabled={isSavingProfile}
                    className="px-4 py-2 rounded bg-light-primary text-light-onPrimary dark:bg-dark-primary dark:text-dark-onPrimary hover:opacity-90 disabled:opacity-50 flex items-center gap-2"
                  >
                    {isSavingProfile && <CircularProgress size="small" />}
                    Sauvegarder
                  </button>
                </div>
              )}
            </div>
          </motion.div>

          {/* Section Changement de Mot de Passe */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-light-surface dark:bg-dark-surface rounded-lg p-6 shadow-sm"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-titleLarge text-light-onSurface dark:text-dark-onSurface">
                Sécurité
              </h2>
            </div>

            {!isChangingPassword ? (
              <button
                onClick={() => setIsChangingPassword(true)}
                className="px-4 py-2 rounded bg-light-primary text-light-onPrimary dark:bg-dark-primary dark:text-dark-onPrimary hover:opacity-90"
              >
                Changer le mot de passe
              </button>
            ) : (
              <div className="space-y-4">
                <div>
                  <label className="block text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                    Mot de passe actuel
                  </label>
                  <input
                    type="password"
                    value={passwordData.current_password}
                    onChange={(e) => handlePasswordChange('current_password', e.target.value)}
                    className="w-full p-3 rounded bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest text-light-onSurface dark:text-dark-onSurface"
                  />
                </div>

                <div>
                  <label className="block text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                    Nouveau mot de passe
                  </label>
                  <input
                    type="password"
                    value={passwordData.new_password}
                    onChange={(e) => handlePasswordChange('new_password', e.target.value)}
                    className="w-full p-3 rounded bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest text-light-onSurface dark:text-dark-onSurface"
                  />
                </div>

                <div>
                  <label className="block text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1">
                    Confirmer le nouveau mot de passe
                  </label>
                  <input
                    type="password"
                    value={passwordData.confirm_new_password}
                    onChange={(e) => handlePasswordChange('confirm_new_password', e.target.value)}
                    className="w-full p-3 rounded bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest text-light-onSurface dark:text-dark-onSurface"
                  />
                </div>

                <div className="flex gap-2 justify-end pt-2">
                  <button
                    onClick={() => {
                      setIsChangingPassword(false);
                      setPasswordData({
                        current_password: '',
                        new_password: '',
                        confirm_new_password: '',
                      });
                    }}
                    className="px-4 py-2 rounded bg-light-secondaryContainer text-light-onSecondaryContainer dark:bg-dark-secondaryContainer dark:text-dark-onSecondaryContainer hover:opacity-90"
                    disabled={isSavingPassword}
                  >
                    Annuler
                  </button>
                  <button
                    onClick={handleSavePassword}
                    disabled={isSavingPassword || !passwordData.current_password || !passwordData.new_password || !passwordData.confirm_new_password}
                    className="px-4 py-2 rounded bg-light-primary text-light-onPrimary dark:bg-dark-primary dark:text-dark-onPrimary hover:opacity-90 disabled:opacity-50 flex items-center gap-2"
                  >
                    {isSavingPassword && <CircularProgress size="small" />}
                    Changer le mot de passe
                  </button>
                </div>
              </div>
            )}
          </motion.div>

          {/* NOUVELLE SECTION : Zone de Danger - Suppression de compte */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 rounded-lg p-6 shadow-sm"
          >
            <div className="mb-4">
              <h2 className="text-titleLarge text-red-700 dark:text-red-400 mb-2">
                Zone de danger
              </h2>
              <p className="text-bodyMedium text-red-600 dark:text-red-300">
                La suppression de votre compte est irréversible. Toutes vos données seront définitivement perdues.
              </p>
            </div>

            {!showDeleteConfirmation ? (
              <button
                onClick={() => setShowDeleteConfirmation(true)}
                className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-800 transition-colors"
              >
                Supprimer mon compte
              </button>
            ) : (
              <div className="space-y-4">
                <div className="bg-white dark:bg-dark-surface p-4 rounded border border-red-300 dark:border-red-800">
                  <p className="text-bodyLarge font-semibold text-red-700 dark:text-red-400 mb-2">
                    Êtes-vous absolument sûr ?
                  </p>
                  <p className="text-bodyMedium text-light-onSurface dark:text-dark-onSurface mb-3">
                    Cette action supprimera définitivement :
                  </p>
                  <ul className="list-disc list-inside text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant space-y-1 mb-4">
                    <li>Votre compte et vos informations personnelles</li>
                    <li>Toutes vos conversations</li>
                    <li>Tous vos messages</li>
                    <li>Tous vos documents uploadés</li>
                  </ul>
                  <p className="text-bodyMedium font-semibold text-red-600 dark:text-red-400">
                    Cette action est IRRÉVERSIBLE et ne peut pas être annulée.
                  </p>
                </div>

                <div className="flex gap-2 justify-end">
                  <button
                    onClick={() => setShowDeleteConfirmation(false)}
                    disabled={isDeletingAccount}
                    className="px-4 py-2 rounded bg-light-secondaryContainer text-light-onSecondaryContainer dark:bg-dark-secondaryContainer dark:text-dark-onSecondaryContainer hover:opacity-90"
                  >
                    Annuler
                  </button>
                  <button
                    onClick={handleDeleteAccount}
                    disabled={isDeletingAccount}
                    className="px-4 py-2 rounded bg-red-600 text-white hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-800 disabled:opacity-50 flex items-center gap-2 font-semibold"
                  >
                    {isDeletingAccount && <CircularProgress size="small" />}
                    Oui, supprimer définitivement
                  </button>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </>
  );
};

export default Profile;