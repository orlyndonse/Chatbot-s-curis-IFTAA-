import React from 'react';
import { Outlet, useLoaderData } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopAppBar from './TopAppBar';
import { useToggle } from '../hooks/useToggle';

const AdminLayout = () => {
  // On récupère les données de l'appLoader pour le layout
  const { user, conversations } = useLoaderData(); 
  const [isSidebarOpen, toggleSidebar] = useToggle(window.innerWidth >= 1024);
  
  const toggleContextHub = () => {};

  return (
    <div className='lg:grid lg:grid-cols-[320px,1fr] h-dvh overflow-hidden relative'>
      <Sidebar
        user={user}
        isSidebarOpen={isSidebarOpen}
        toggleSidebar={toggleSidebar}
        conversations={conversations || []} // Assurer que c'est un tableau
        // Pas de conversation active dans ce contexte
        activeConversationUid={null} 
        // Fonctions non pertinentes pour la page admin, on passe des fonctions vides
        onSelectConversation={() => {}}
        onDeleteConversation={() => {}}
        onNewConversation={() => {}}
        isAdminPage={true} // Active le mode admin
      />
      <div className="h-dvh grid grid-rows-[max-content,1fr] overflow-hidden bg-light-background dark:bg-dark-background">
        <TopAppBar 
          toggleSidebar={toggleSidebar} 
          user={user} 
          toggleContextHub={toggleContextHub} 
        />
        <main className="overflow-y-auto">
          
          <Outlet /> 
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;