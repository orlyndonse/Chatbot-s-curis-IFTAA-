// Sidebar.jsx - Mis à jour avec icônes locales
import React, { useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import { motion } from 'framer-motion';
import Logo from './Logo';
import { ExtendedFab, IconBtn } from './Button';
import { CircularProgress } from './Progress';
import Icon from './Icon'; // Import du composant Icon

const Sidebar = ({
  isSidebarOpen,
  toggleSidebar,
  conversations,
  onSelectConversation,
  activeConversationUid,
  onDeleteConversation,
  onNewConversation,
  isDeleting,
  renamingConvId,
  renameInputText,
  onStartRename,
  onCancelRename,
  onSaveRename,
  onRenameInputChange,
  isSavingRename,
}) => {

  const renameInputRef = useRef(null);

  useEffect(() => {
    if (renamingConvId && renameInputRef.current) {
      renameInputRef.current.focus();
      renameInputRef.current.select();
    }
  }, [renamingConvId]);

  const handleNewChatClick = () => {
    if (renamingConvId) {
      onCancelRename();
    }
    onNewConversation();
    if (window.innerWidth < 1024) {
        toggleSidebar();
    }
  };

  const handleSelect = (conv, event) => {
    if (event && event.target.closest('.action-buttons')) {
      return;
    }

    if (renamingConvId === conv.uid) return;

    if (renamingConvId) {
        onCancelRename();
    }

    if (conv.uid !== activeConversationUid) {
        onSelectConversation(conv);
    }

    if (window.innerWidth < 1024) {
        toggleSidebar();
    }
  };

  const handleKeyDownRename = (event, convId) => {
      if (event.key === 'Enter') {
          event.preventDefault();
          if (renameInputText.trim()) {
             onSaveRename(convId, renameInputText);
          }
      } else if (event.key === 'Escape') {
          onCancelRename();
      }
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        className={`sidebar ${isSidebarOpen ? 'active' : ''}`}>
        <div className="sidebar-inner">
          
          {/* Logo et Bouton Menu */}
          <div className='h-16 grid items-center px-4 mb-4'>
             <div className='flex items-center gap-1'>
                  <IconBtn 
                    icon='menu'
                    title='Menu'
                    size='small'
                    classes='lg:hidden'
                    onClick={toggleSidebar}
                  />
                  <Logo classes=''/>
              </div>
          </div>

          {/* Bouton Nouvelle Discussion */}
          <ExtendedFab
            text='Nouvelle Discussion'
            classes='mb-4'
            onClick={handleNewChatClick}
            disabled={!!renamingConvId || isSavingRename}
          />

          {/* Section Historique */}
          <div className='overflow-y-auto -me-2 pe-1 flex-grow'>
            <p className='text-titleSmall h-9 grid items-center px-4 sticky top-0 bg-light-surfaceContainerLow dark:bg-dark-surfaceContainerLow z-10'>
              Historique
            </p>

            {/* Liste des Conversations */}
            <nav className="flex flex-col gap-1 px-0 py-2">
            {conversations && conversations.length > 0 ? (
              conversations.map((conv) => (
                <div
                   key={conv.uid}
                   className={`nav-item group relative rounded-full transition-colors duration-200 ease-out ${
                     renamingConvId === conv.uid
                       ? 'bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh ring-1 ring-light-primary/50 dark:ring-dark-primary/50'
                       : activeConversationUid === conv.uid
                       ? 'bg-light-secondaryContainer dark:bg-dark-secondaryContainer'
                       : 'hover:bg-light-onSurface/5 dark:hover:bg-dark-onSurface/5'
                   }`}
                   title={renamingConvId === conv.uid ? "Renommer la discussion..." : conv.title}
                   onClick={(e) => handleSelect(conv, e)}
                 >
                   {renamingConvId === conv.uid ? (
                     // UI DE RENOMMAGE
                     <div className="flex items-center gap-1 px-3 py-1 h-[36px]">
                       <input
                         ref={renameInputRef}
                         type="text"
                         value={renameInputText}
                         onChange={onRenameInputChange}
                         onKeyDown={(e) => handleKeyDownRename(e, conv.uid)}
                         disabled={isSavingRename}
                         className="flex-grow bg-transparent border-b border-light-primary dark:border-dark-primary focus:outline-none text-sm px-1 py-0 text-light-onSurface dark:text-dark-onSurface placeholder-light-onSurfaceVariant/70"
                         placeholder="Nouveau titre..."
                         maxLength={100}
                         onClick={(e) => e.stopPropagation()}
                       />
                       
                       {isSavingRename ? (
                           <div className="w-10 h-6 flex justify-center items-center">
                              <CircularProgress size="small" />
                           </div>
                       ) : (
                         <div className="flex items-center" onClick={(e) => e.stopPropagation()}>
                           <IconBtn
                             icon='check'
                             size='small'
                             title='Sauvegarder'
                             onClick={(e) => { 
                               e.stopPropagation(); 
                               if (renameInputText.trim()) onSaveRename(conv.uid, renameInputText);
                             }}
                             disabled={!renameInputText.trim()}
                             classes="text-green-600 dark:text-green-400 hover:bg-green-500/10 disabled:text-gray-400 dark:disabled:text-gray-600 disabled:hover:bg-transparent"
                           />
                           <IconBtn
                             icon='close'
                             size='small'
                             title='Annuler'
                             onClick={(e) => {
                               e.stopPropagation();
                               onCancelRename();
                             }}
                             classes="text-red-600 dark:text-red-400 hover:bg-red-500/10"
                           />
                         </div>
                       )}
                     </div>
                   ) : (
                     // AFFICHAGE NORMAL
                     <div
                       className={`nav-link w-full text-left h-[36px] px-4 flex items-center gap-3 relative overflow-hidden ${
                         activeConversationUid === conv.uid
                           ? 'text-light-onSecondaryContainer dark:text-dark-onSecondaryContainer font-medium'
                           : 'text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant'
                       }`}
                     >
                       {/* Icône de chat */}
                       <Icon 
                         name="chat_bubble" 
                         size={16} 
                         className="flex-shrink-0"
                       />
                       
                       <span className='truncate flex-grow cursor-pointer hover:text-light-primary dark:hover:text-dark-primary transition-colors duration-200'>
                         {conv.title.slice(0, 30)}{conv.title.length > 30 ? '...' : ''}
                       </span>

                       {/* Boutons d'actions */}
                       {!renamingConvId && (
                         <div 
                           className={`action-buttons flex items-center ml-auto transition-opacity duration-150 ease-in-out absolute right-1 top-1/2 -translate-y-1/2 bg-light-surfaceContainerLow dark:bg-dark-surfaceContainerLow rounded-full p-0.5 shadow-sm ${'opacity-0 group-hover:opacity-100 group-focus-within:opacity-100'}`}
                           onClick={(e) => e.stopPropagation()}
                         >
                           {isDeleting === conv.uid ? (
                             <div className="w-12 h-6 flex justify-center items-center">
                               <CircularProgress size="small" />
                             </div>
                           ) : (
                             <>
                               {/* Bouton Renommer */}
                               <IconBtn
                                 icon='drive_file_rename_outline'
                                 size='small'
                                 onClick={(e) => {
                                   e.stopPropagation();
                                   onStartRename(conv.uid, conv.title);
                                 }}
                                 classes='text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant hover:text-light-primary dark:hover:text-dark-primary'
                                 title='Renommer'
                                 disabled={!!isDeleting}
                               />
                               
                               {/* Bouton Supprimer */}
                               <IconBtn
                                 icon='delete'
                                 size='small'
                                 onClick={(e) => {
                                   e.stopPropagation();
                                   onDeleteConversation(conv.uid);
                                 }}
                                 classes='text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant hover:text-red-600 dark:hover:text-red-400'
                                 title='Supprimer'
                                 disabled={!!isDeleting}
                               />
                             </>
                           )}
                         </div>
                       )}
                       
                       <div className='state-layer'></div>
                     </div>
                   )}
                 </div>
              ))
              ) : (
                <p className='px-4 py-2 text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant text-sm italic'>
                  Aucune conversation pour le moment.
                </p>
              )}
            </nav>
          </div>

          {/* Footer */}
          <div className='mt-auto h-14 px-4 grid items-center text-labelLarge text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant border-t border-light-surfaceContainerHigh dark:border-dark-surfaceContainerHigh truncate'>
            &copy; 2025 isetsfax. Tous droits réservés.
          </div>
        </div>
      </motion.div>

      {/* Overlay pour fermer la sidebar sur mobile */}
      <div
           className={`overlay ${isSidebarOpen ? 'active' : ''} lg:hidden`}
           onClick={() => {
             if (renamingConvId) onCancelRename();
             toggleSidebar();
           }}
           style={{
            zIndex: 'var(--overlay-z-index, 30)'
          }}
         ></div>
    </>
  );
};

Sidebar.propTypes = {
  isSidebarOpen: PropTypes.bool,
  toggleSidebar: PropTypes.func,
  conversations: PropTypes.array,
  onSelectConversation: PropTypes.func,
  activeConversationUid: PropTypes.string,
  onDeleteConversation: PropTypes.func,
  onNewConversation: PropTypes.func,
  isDeleting: PropTypes.string,
  renamingConvId: PropTypes.string,
  renameInputText: PropTypes.string,
  onStartRename: PropTypes.func,
  onCancelRename: PropTypes.func,
  onSaveRename: PropTypes.func,
  onRenameInputChange: PropTypes.func,
  isSavingRename: PropTypes.bool,
};

export default Sidebar;