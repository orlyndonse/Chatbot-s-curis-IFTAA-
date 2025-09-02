import React, { useState, useEffect, useCallback, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion } from 'framer-motion';
import { useLoaderData, useNavigate } from 'react-router-dom';
import { useToggle } from './hooks/useToggle';
import { useSnackbar } from './hooks/useSnackbar';
import { fetchWithAuth } from './utils/fetchWithAuth';
import { useLanguage } from './contexts/LanguageContext';



import PageTitle from './components/PageTitle';
import TopAppBar from './components/TopAppBar';
import Sidebar from './components/Sidebar';
import ContextHubPanel from './components/contextHub/ContextHubPanel';
import PromptField from './components/PromptField';
import Greetings from './pages/Greetings';
import { CircularProgress } from './components/Progress';
import { IconBtn } from './components/Button';
import DocumentPreview from './components/DocumentPreview';
import StreamingMarkdown from './components/StreamingMarkdown';
import LogsPanel from './components/LogsPanel';

const App = () => {
  const { user, conversations: loadedConversations, initialMessages: loadedMessages } = useLoaderData();
  const navigate = useNavigate();
  const [isSidebarOpen, toggleSidebar] = useToggle(window.innerWidth >= 1024);
  const [isContextHubOpen, toggleContextHub] = useToggle(false);
  const [isLogsPanelOpen, toggleLogsPanel] = useToggle(false);
  const { showSnackbar } = useSnackbar();
  const { language } = useLanguage();

  const [allConversations, setAllConversations] = useState(() => loadedConversations || []);
  const [activeConversation, setActiveConversation] = useState(() =>
    (loadedConversations && loadedConversations.length > 0 && loadedMessages && loadedMessages.length > 0)
      ? loadedConversations[0]
      : null
  );
  const [currentMessages, setCurrentMessages] = useState(() => loadedMessages || []);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [isSendingMessage, setIsSendingMessage] = useState(false);
  const [isCreatingConversation, setIsCreatingConversation] = useState(false);
  const [isDeletingConversation, setIsDeletingConversation] = useState(null);
  const [editingMessageId, setEditingMessageId] = useState(null);
  const [editText, setEditText] = useState('');
  const [isEditingMessage, setIsEditingMessage] = useState(false);
  const [renamingConvId, setRenamingConvId] = useState(null);
  const [renameInputText, setRenameInputText] = useState('');
  const [isSavingRename, setIsSavingRename] = useState(false);
  
  const [isUploading, setIsUploading] = useState(false);
  const [documentsInContext, setDocumentsInContext] = useState([]);
  const [currentContextSize, setCurrentContextSize] = useState(0);
  const [maxContextSize, setMaxContextSize] = useState(1024 * 1024 * 5); // Example: 5MB
  const [deletingDocumentId, setDeletingDocumentId] = useState(null);

  const [isPreviewModalOpen, setIsPreviewModalOpen] = useState(false);
  const [documentToPreview, setDocumentToPreview] = useState(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [logs, setLogs] = useState([]);

  const messagesEndRef = useRef(null);
  const editInputRef = useRef(null);

  useEffect(() => { if (!user) { navigate('/login'); } }, [user, navigate]);
  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [currentMessages]);
  
  useEffect(() => { if (editingMessageId && editInputRef.current) { const textarea = editInputRef.current; textarea.style.height = 'auto'; textarea.style.height = `${textarea.scrollHeight}px`; textarea.focus(); textarea.select(); } }, [editingMessageId]);

  const handleCancelEdit = useCallback(() => { setEditingMessageId(null); setEditText(''); setIsEditingMessage(false); }, []);
  const handleCancelRename = useCallback(() => { setRenamingConvId(null); setRenameInputText(''); setIsSavingRename(false);}, []);

  const fetchConversationData = useCallback(async (conversationUid) => {
    if (!conversationUid) {
      setCurrentMessages([]); setDocumentsInContext([]); setCurrentContextSize(0); setIsLoadingData(false); return;
    }
    handleCancelEdit(); handleCancelRename(); setIsLoadingData(true);
    if (activeConversation?.uid !== conversationUid || currentMessages.length === 0) {
        setCurrentMessages([]);
    }
    setDocumentsInContext([]); setCurrentContextSize(0);
    try {
      const [messages, docsResponse] = await Promise.all([
        fetchWithAuth(`/api/v1/conversations/${conversationUid}/messages`),
        fetchWithAuth(`/api/v1/conversations/${conversationUid}/documents`)
      ]);
      if (!(activeConversation?.uid === conversationUid && currentMessages.length > 0 && messages.length === 0)){
         setCurrentMessages(Array.isArray(messages) ? messages : []);
      }
      const fetchedDocs = Array.isArray(docsResponse) ? docsResponse : [];
      const processedDocs = fetchedDocs.map(doc => ({
        ...doc,
        isActiveInContext: doc.is_active !== undefined ? doc.is_active : true
      }));
      setDocumentsInContext(processedDocs);
      setCurrentContextSize(processedDocs.reduce((sum, doc) => sum + (doc.size || 0), 0));
    } catch (error) {
      console.error(`Error fetching data for ${conversationUid}:`, error);
      showSnackbar({ message: "Erreur chargement données.", type: 'error' });
    } finally {
      setIsLoadingData(false);
    }
  }, [showSnackbar, handleCancelEdit, handleCancelRename, activeConversation?.uid]);

  useEffect(() => { if (activeConversation?.uid) { fetchConversationData(activeConversation.uid); } else { setCurrentMessages([]); setDocumentsInContext([]); setCurrentContextSize(0); setIsLoadingData(false);}}, [activeConversation, fetchConversationData]);
    
  const handleSelectConversation = useCallback((conversation) => { if (activeConversation?.uid === conversation?.uid || renamingConvId) { if (window.innerWidth < 1024 && !renamingConvId && isSidebarOpen) toggleSidebar(); return; } setActiveConversation(conversation); if (window.innerWidth < 1024 && isSidebarOpen) toggleSidebar(); }, [activeConversation?.uid, renamingConvId, isSidebarOpen, toggleSidebar]);
  
  const handleNewConversationRequest = useCallback(() => { handleCancelEdit(); handleCancelRename(); setActiveConversation(null); if (window.innerWidth < 1024 && isSidebarOpen) toggleSidebar();}, [isSidebarOpen, toggleSidebar, handleCancelEdit, handleCancelRename]);

  const handleSendMessage = useCallback(async (promptText) => {
    if (isSendingMessage || isCreatingConversation || renamingConvId) {
      showSnackbar({ message: "Veuillez attendre la fin de l'opération en cours.", type: 'info' });
      return;
    }
    handleCancelEdit();
    setIsSendingMessage(true);
    setLogs([]); // Réinitialise les logs à chaque nouvelle requête
  
    let targetConversation = activeConversation;
    const tempPromptId = `temp-prompt-${Date.now()}`;
    let createdConversationLocally = false;
  
    // --- 1. Gestion optimiste du prompt et de la conversation ---
    try {
      const optimisticPromptMessage = {
        uid: tempPromptId,
        user_uid: user.uid,
        prompt: promptText,
        response: null,
        created_at: new Date().toISOString(),
      };
  
      if (!targetConversation) {
        setIsCreatingConversation(true);
        const newTitle = promptText.substring(0, 30) + (promptText.length > 30 ? '...' : '');
        const newConversation = await fetchWithAuth('/api/v1/conversations/', {
          method: 'POST',
          body: JSON.stringify({ title: newTitle }),
        });
        setIsCreatingConversation(false);
        if (!newConversation?.uid) throw new Error("La création de la conversation a échoué.");
        
        setAllConversations(prev => [newConversation, ...prev]);
        setActiveConversation(newConversation);
        targetConversation = newConversation;
        createdConversationLocally = true;
        setCurrentMessages([optimisticPromptMessage]);
        
        // Ajouter un log pour la création de conversation
        setLogs(prev => [...prev, `INFO: Nouvelle conversation créée - ID: ${newConversation.uid}`]);
      } else {
        setCurrentMessages(prev => [...prev, optimisticPromptMessage]);
      }
  
      // --- 2. Préparation pour la réponse en streaming ---
      const tempResponseId = `temp-response-${Date.now()}`;
      const optimisticResponseMessage = {
        uid: tempResponseId,
        prompt: null, // C'est une réponse, pas un prompt
        response: '', // Commence avec une réponse vide
        isLoading: true, // Pour afficher un indicateur de chargement
        created_at: new Date().toISOString(),
      };
      // Ajoute immédiatement le conteneur de réponse vide à l'UI
      setCurrentMessages(prev => [...prev, optimisticResponseMessage]);
      
      // Log du début du streaming
      setLogs(prev => [...prev, `INFO: Début du streaming pour la conversation ${targetConversation.uid}`]);
      
      // --- 3. Appel streaming ---
      const token = localStorage.getItem("awesomeLeadsToken");
      const response = await fetch(
        `http://localhost:8000/api/v1/conversations/${targetConversation.uid}/messages/stream`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ prompt: promptText })
        }
      );
  
      if (!response.ok) {
        const errorText = await response.text();
        setLogs(prev => [...prev, `ERROR: Erreur serveur (${response.status}): ${errorText}`]);
        throw new Error(`Erreur du serveur (${response.status}): ${errorText}`);
      }
  
      setLogs(prev => [...prev, `INFO: Connexion streaming établie avec succès`]);
  
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let chunkCount = 0;
  
      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          setLogs(prev => [...prev, `INFO: Stream terminé - Total chunks reçus: ${chunkCount}`]);
          break;
        }
        
        // Décoder le chunk
        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        
        // Traiter les lignes complètes (SSE)
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Garder la ligne incomplète
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6);
            
            if (data === '[DONE]') {
              setCurrentMessages(prev =>
                prev.map(msg =>
                  msg.uid === tempResponseId
                    ? { ...msg, isLoading: false }
                    : msg
                )
              );
              setLogs(prev => [...prev, `INFO: Signal [DONE] reçu - Streaming terminé`]);
              break;
            }
            
            if (data.trim()) {
              chunkCount++;
              // Ajouter le chunk à la réponse en accumulant le contenu
              setCurrentMessages(prev =>
                prev.map(msg =>
                  msg.uid === tempResponseId
                    ? { 
                        ...msg, 
                        response: (msg.response || '') + data,
                        // Assurez-vous que isLoading reste true pendant le streaming
                        isLoading: true
                      }
                    : msg
                )
              );
              
              setLogs(prev => [...prev, `INFO: Chunk ${chunkCount}: '${data}' (length: ${data.length})`]);
            }
          }
        }
        
        // Vérifier si on a reçu [DONE] pour sortir de la boucle while
        if (lines.some(line => line.startsWith('data: [DONE]'))) {
          break;
        }
      }
  
      // --- 4. Finalisation ---
      setLogs(prev => [...prev, `INFO: Rafraîchissement des données de la conversation`]);
      // Une fois le stream terminé, on rafraîchit les données pour obtenir les vrais UID
      await fetchConversationData(targetConversation.uid);
      
      const nowISO = new Date().toISOString();
      setAllConversations(prev =>
        prev.map(c => c.uid === targetConversation.uid ? { ...c, update_at: nowISO } : c)
          .sort((a, b) => new Date(b.update_at || b.created_at) - new Date(a.update_at || a.created_at))
      );
  
      setLogs(prev => [...prev, `SUCCESS: Message envoyé avec succès`]);
  
    } catch (error) {
      console.error("Erreur lors de l'envoi du message:", error);
      setLogs(prev => [...prev, `ERROR: ${error.message || "Erreur inconnue lors de l'envoi du message"}`]);
      showSnackbar({ message: `Erreur: ${error.message || "Impossible d'envoyer le message."}`, type: 'error' });
      
      // Nettoyage en cas d'erreur
      setCurrentMessages(prev => prev.filter(msg => !msg.uid.startsWith('temp-')));
      if (createdConversationLocally && targetConversation) {
        setAllConversations(prev => prev.filter(c => c.uid !== targetConversation.uid));
        if (activeConversation?.uid === targetConversation.uid) {
          setActiveConversation(null);
        }
      }
    } finally {
      setIsSendingMessage(false);
      setIsCreatingConversation(false);
      setLogs(prev => [...prev, `INFO: Nettoyage terminé - États réinitialisés`]);
    }
  }, [activeConversation, user?.uid, showSnackbar, isSendingMessage, isCreatingConversation, renamingConvId, handleCancelEdit, fetchConversationData]);
  
  const handleDeleteConversation = useCallback(async (conversationUid) => { 
    if (isEditingMessage || renamingConvId) { 
      showSnackbar({ message: "Veuillez terminer.", type: 'info' }); 
      return; 
    } 
    if (isDeletingConversation) return; 
    setIsDeletingConversation(conversationUid); 
    if (activeConversation?.uid === conversationUid) handleCancelEdit(); 
    try { 
      await fetchWithAuth(`/api/v1/conversations/${conversationUid}`, { method: 'DELETE' }); 
      const updated = allConversations.filter(c => c.uid !== conversationUid); 
      setAllConversations(updated); 
      if (activeConversation?.uid === conversationUid) { 
        setActiveConversation(updated[0] || null); 
      } 
      showSnackbar({ message: "Discussion supprimée.", type: 'success' }); 
    } catch (e) { 
      showSnackbar({ message: "Erreur suppression.", type: 'error' }); 
    } finally { 
      setIsDeletingConversation(null); 
    }
  }, [activeConversation?.uid, allConversations, showSnackbar, isDeletingConversation, isEditingMessage, renamingConvId, handleCancelEdit]);

  const handleStartRename = useCallback((id, title) => { 
    if (isEditingMessage || isSavingRename || isSendingMessage || isCreatingConversation) return; 
    handleCancelEdit(); 
    setRenamingConvId(id); 
    setRenameInputText(title);
  }, [isEditingMessage, isSavingRename, isSendingMessage, isCreatingConversation, handleCancelEdit]);

  const handleSaveRename = useCallback(async (id, title) => { 
    const t = title.trim(); 
    if (!t || t.length > 100) { 
      showSnackbar({ message: !t ? "Titre vide." : "Titre trop long.", type: 'error' }); 
      return; 
    } 
    if (isSavingRename) return; 
    setIsSavingRename(true); 
    try { 
      const d = await fetchWithAuth(`/api/v1/conversations/${id}/rename`, { 
        method: 'PUT', 
        body: JSON.stringify({ new_title: t }), 
      }); 
      setAllConversations(p => p.map(c => c.uid === id ? {...c, title: d.title, update_at: d.update_at} : c).sort((a,b) => new Date(b.update_at||b.created_at) - new Date(a.update_at||a.created_at))); 
      if (activeConversation?.uid === id) setActiveConversation(p => p ? {...p, title: d.title, update_at: d.update_at} : null); 
      showSnackbar({ message: "Renommée.", type: 'success' }); 
      handleCancelRename(); 
    } catch (e) { 
      showSnackbar({ message: `Erreur: ${e.data?.detail||e.message}`, type: 'error' }); 
    } finally { 
      setIsSavingRename(false); 
    }
  }, [activeConversation?.uid, showSnackbar, handleCancelRename, isSavingRename]);

  const handleRenameInputChange = useCallback((e) => { setRenameInputText(e.target.value); }, []);

  const handleStartEdit = useCallback((uid, prompt) => { 
    if (isSendingMessage || isEditingMessage || renamingConvId || isCreatingConversation) return; 
    handleCancelRename(); 
    setEditingMessageId(uid); 
    setEditText(prompt);
  }, [isSendingMessage, isEditingMessage, renamingConvId, isCreatingConversation, handleCancelRename]);

  const handleSaveEdit = useCallback(async (uid, prompt) => { 
    const t = prompt.trim(); 
    if (!t || isEditingMessage || !activeConversation?.uid) { 
      if(!t) showSnackbar({ message: "Message vide.", type: 'error' }); 
      return; 
    } 
    if (isSendingMessage || isCreatingConversation) return; 
    
    setIsEditingMessage(true); 
    setLogs([]); // Réinitialise les logs pour l'édition
    
    // Créer un message temporaire avec isLoading pour déclencher StreamingMarkdown
    const tempEditedMessage = {
      uid: uid,
      prompt: t,
      response: '', // Commence avec une réponse vide pour le streaming
      isLoading: true, // Ceci déclenche le mode streaming dans StreamingMarkdown
      created_at: new Date().toISOString(),
    };
    
    // Remplacer le message existant par la version en cours d'édition
    setCurrentMessages(prev => prev.map(msg => 
      msg.uid === uid ? tempEditedMessage : msg
    ));
    
    try { 
      const token = localStorage.getItem("awesomeLeadsToken");
      const response = await fetch(
        `http://localhost:8000/api/v1/conversations/${activeConversation.uid}/messages/${uid}/edit/stream`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ new_prompt: t })
        }
      );
  
      if (!response.ok) {
        const errorText = await response.text();
        setLogs(prev => [...prev, `ERROR: Erreur serveur (${response.status}): ${errorText}`]);
        throw new Error(`Erreur du serveur (${response.status}): ${errorText}`);
      }
  
      setLogs(prev => [...prev, `INFO: Connexion streaming d'édition établie`]);
  
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let chunkCount = 0;
  
      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          setLogs(prev => [...prev, `INFO: Édition stream terminé - Total chunks reçus: ${chunkCount}`]);
          break;
        }
        
        const chunk = decoder.decode(value, { stream: true });
        buffer += chunk;
        
        const lines = buffer.split('\n');
        buffer = lines.pop();
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6);
            
            if (data === '[DONE]') {
              // Marquer comme terminé pour arrêter l'animation de streaming
              setCurrentMessages(prev =>
                prev.map(msg =>
                  msg.uid === uid
                    ? { ...msg, isLoading: false } // Arrêter le mode streaming
                    : msg
                )
              );
              setLogs(prev => [...prev, `INFO: Signal [DONE] reçu - Édition terminée`]);
              break;
            }
            
            if (data.trim() && !data.startsWith('[ERROR]')) {
              chunkCount++;
              //  Accumuler la réponse tout en gardant isLoading=true
              setCurrentMessages(prev =>
                prev.map(msg =>
                  msg.uid === uid
                    ? { 
                        ...msg, 
                        response: (msg.response || '') + data,
                        isLoading: true // Garder le mode streaming actif
                      }
                    : msg
                )
              );
              setLogs(prev => [...prev, `INFO: Edit Chunk ${chunkCount}: '${data}' (length: ${data.length})`]);
            }
            
            if (data.startsWith('[ERROR]')) {
              setLogs(prev => [...prev, `ERROR: ${data}`]);
              throw new Error(data.substring(7)); // Enlève '[ERROR] '
            }
          }
        }
        
        if (lines.some(line => line.startsWith('data: [DONE]'))) {
          break;
        }
      }
      // Une fois le stream terminé, on rafraîchit les données pour obtenir la version finale et stylisée
      await fetchConversationData(activeConversation.uid);

      showSnackbar({ message: "Message modifié avec succès.", type: 'success' }); 
      handleCancelEdit();
      
    } catch (e) { 
      setLogs(prev => [...prev, `ERROR: ${e.message || "Erreur inconnue lors de l'édition"}`]);
      showSnackbar({ message: `Erreur: ${e.message}`, type: 'error' });
      
      // Restaurer l'état original en cas d'erreur
      await fetchConversationData(activeConversation.uid);
    } finally { 
      setIsEditingMessage(false); 
      setLogs(prev => [...prev, `INFO: Nettoyage édition terminé`]);
    }
  }, [activeConversation?.uid, showSnackbar, isEditingMessage, isSendingMessage, isCreatingConversation, handleCancelEdit, fetchConversationData]);

  const handleFileSubmitForContextHub = useCallback(async (files) => {
    if (!activeConversation?.uid) {
      showSnackbar({ message: "Sélectionnez conversation.", type: 'info' });
      return;
    }
    if (isUploading) return;
    setIsUploading(true);
    showSnackbar({ message: `Téléversement ${files.length} fichier(s)...`, type: 'info' });
    const fd = new FormData();
    files.forEach(f => fd.append('files', f));
    try {
      console.log("Sending upload request for files:", files.map(f => f.name));
      const r = await fetchWithAuth(`/api/v1/conversations/${activeConversation.uid}/upload`, {
        method: 'POST',
        body: fd
      });
      console.log("Upload response:", r);
      let sm = r?.message || `${r?.documents?.length || 0} traité(s).`;
      let wm = r?.errors?.length ? `${r.errors.length} erreur(s).` : "";
      showSnackbar({ message: `${sm} ${wm}`.trim(), type: wm ? 'warning' : 'success', duration: 7000 });
      await fetchConversationData(activeConversation.uid);
    } catch (e) {
      console.error("Error in handleFileSubmitForContextHub:", e);
      showSnackbar({ message: `Erreur: ${e.data?.detail || e.message}`, type: 'error' });
    } finally {
      console.log("Upload complete, resetting isUploading");
      setIsUploading(false);
    }
  }, [activeConversation?.uid, isUploading, showSnackbar, fetchConversationData]);

  const handleFileUploadForPromptField = useCallback((files) => {
    try {
      if (!activeConversation?.uid) {
        showSnackbar({ message: "Sélectionnez conversation.", type: 'info' });
        if (!isContextHubOpen) toggleContextHub();
        return;
      }
      const fileArray = Array.from(files); // Convertir FileList en tableau
      console.log("Uploading files from PromptField:", fileArray);
      handleFileSubmitForContextHub(fileArray);
    } catch (e) {
      console.error("Error in handleFileUploadForPromptField:", e);
      showSnackbar({ message: `Erreur d'upload: ${e.message}`, type: 'error' });
      setIsUploading(false); // Réinitialiser l'état en cas d'erreur
    }
  }, [activeConversation?.uid, handleFileSubmitForContextHub, showSnackbar, isContextHubOpen, toggleContextHub]);

  const handleDeleteDocumentFromContext = useCallback(async (docUid) => { 
    if (!activeConversation?.uid || !docUid) return; 
    setDeletingDocumentId(docUid); 
    try { 
      await fetchWithAuth(`/api/v1/conversations/${activeConversation.uid}/documents/${docUid}`, { method: 'DELETE' }); 
      showSnackbar({ message: "Document supprimé.", type: 'success' }); 
      await fetchConversationData(activeConversation.uid); 
    } catch (e) { 
      showSnackbar({ message: `Erreur suppression: ${e.data?.detail||e.message}`, type: 'error' }); 
    } finally { 
      setDeletingDocumentId(null); 
    }
  }, [activeConversation?.uid, showSnackbar, fetchConversationData]);

  const handleToggleDocumentActiveState = useCallback(async (documentUid) => {
    if (!activeConversation?.uid) return;

    const originalDocuments = documentsInContext;
    const newDocuments = documentsInContext.map(doc => {
      if (doc.uid === documentUid) {
        return { ...doc, isActiveInContext: !doc.isActiveInContext };
      }
      return doc;
    });
    setDocumentsInContext(newDocuments);

    const docToUpdate = newDocuments.find(d => d.uid === documentUid);
    const newActiveState = docToUpdate.isActiveInContext;

    try {
      await fetchWithAuth(
        `/api/v1/conversations/${activeConversation.uid}/documents/${documentUid}/toggle-active?is_active=${newActiveState}`,
        { method: 'PATCH' }
      );
      showSnackbar({
        message: `Document "${docToUpdate.filename.substring(0, 20)}..." ${newActiveState ? 'activé' : 'désactivé'}.`,
        type: 'success'
      });
    } catch (error) {
      showSnackbar({
        message: `Erreur lors de la mise à jour du document.`,
        type: 'error'
      });
      setDocumentsInContext(originalDocuments);
      console.error("Failed to toggle document active state:", error);
    }
  }, [activeConversation?.uid, documentsInContext, showSnackbar, fetchWithAuth]);

  const handlePreviewDocument = useCallback(async (doc) => {
    setIsPreviewModalOpen(true);
    const fullDoc = documentsInContext.find(d => d.uid === doc.uid) || doc;
    setDocumentToPreview({ 
      ...fullDoc, 
      name: fullDoc.filename, 
      type: fullDoc.mime_type,
      file: null, 
      previewContent: null,
      error: null 
    });
    setIsPreviewLoading(true);

    if (fullDoc.mime_type?.includes('pdf')) {
      try {
        if (!activeConversation?.uid || !fullDoc.uid) throw new Error("ID de conversation ou de document manquant pour l'aperçu PDF.");
        const rawResp = await fetch(`http://localhost:8000/api/v1/conversations/${activeConversation.uid}/documents/${fullDoc.uid}/download`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem("awesomeLeadsToken")}` }
        });
        if (!rawResp.ok) throw new Error(`Échec du téléchargement PDF: ${rawResp.statusText}`);
        const blob = await rawResp.blob();
        setDocumentToPreview(prev => ({ ...prev, file: blob }));
      } catch (e) {
        showSnackbar({ message: `Erreur de prévisualisation PDF: ${e.message}`, type: 'error' });
        setDocumentToPreview(prev => ({ ...prev, error: "Aperçu PDF impossible." }));
      } finally {
        setIsPreviewLoading(false);
      }
    } else if (fullDoc.mime_type?.startsWith('text/')) {
      try {
        if (!activeConversation?.uid || !fullDoc.uid) throw new Error("ID de conversation ou de document manquant pour l'aperçu texte.");
        const response = await fetch(`http://localhost:8000/api/v1/conversations/${activeConversation.uid}/documents/${fullDoc.uid}/download`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem("awesomeLeadsToken")}` }
        });
        if (!response.ok) throw new Error(`Échec du téléchargement du contenu texte: ${response.statusText}`);
        const textContent = await response.text();
        setDocumentToPreview(prev => ({ ...prev, previewContent: textContent || "Le contenu est vide." }));
      } catch (e) {
        showSnackbar({ message: `Erreur de prévisualisation TXT: ${e.message}`, type: 'error' });
        setDocumentToPreview(prev => ({ ...prev, error: "Aperçu du fichier texte impossible.", previewContent: "Contenu non disponible." }));
      } finally {
        setIsPreviewLoading(false);
      }
    } else if (fullDoc.mime_type?.startsWith('image/')) { 
      try {
        if (!activeConversation?.uid || !fullDoc.uid) throw new Error("ID de conversation ou de document manquant pour l'aperçu image.");
        const rawResp = await fetch(`http://localhost:8000/api/v1/conversations/${activeConversation.uid}/documents/${fullDoc.uid}/download`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem("awesomeLeadsToken")}` }
        });
        if (!rawResp.ok) throw new Error(`Échec du téléchargement de l'image: ${rawResp.statusText}`);
        const blob = await rawResp.blob();
        setDocumentToPreview(prev => ({ ...prev, file: blob }));
      } catch (e) {
        showSnackbar({ message: `Erreur de prévisualisation Image: ${e.message}`, type: 'error' });
        setDocumentToPreview(prev => ({ ...prev, error: "Aperçu de l'image impossible." }));
      } finally {
        setIsPreviewLoading(false);
      }
    } else {
      setDocumentToPreview(prev => ({ ...prev, error: `Aperçu non disponible pour ce type de fichier (${fullDoc.mime_type || 'inconnu'}).` }));
      setIsPreviewLoading(false);
    }
  }, [activeConversation?.uid, showSnackbar, documentsInContext]);
  
  const handleClosePreview = useCallback(() => { 
    setIsPreviewModalOpen(false); 
    if (documentToPreview?.file instanceof Blob && documentToPreview.objectUrl) { 
      URL.revokeObjectURL(documentToPreview.objectUrl); 
    } 
    setDocumentToPreview(null); 
    setIsPreviewLoading(false); 
  }, [documentToPreview]); 

  const handleToggleActiveFromPreview = useCallback(() => { 
    if (!documentToPreview?.uid) return; 
    const docBefore = documentsInContext.find(d=>d.uid === documentToPreview.uid); 
    const futureActive = !(docBefore?.isActiveInContext||false); 
    handleToggleDocumentActiveState(documentToPreview.uid); 
    showSnackbar({ message: `Doc "${documentToPreview.name}" ${futureActive ? 'activé' : 'désactivé'}.`, type: 'success'}); 
    handleClosePreview();
  }, [documentToPreview, documentsInContext, handleToggleDocumentActiveState, showSnackbar, handleClosePreview]);

  const contextHubMarginClass = isContextHubOpen && window.innerWidth >= 1024
    ? language === 'ar' ? 'lg:ml-[360px]' : 'lg:mr-[360px]'
    : '';

  let mainContent;
  if (activeConversation && isLoadingData && currentMessages.length === 0) { 
    mainContent = ( 
      <div className="flex justify-center items-center h-full"> 
        <CircularProgress size="large" /> 
        <p className="ml-4">Chargement...</p> 
      </div> 
    );
  } else if (activeConversation && currentMessages) { 
    mainContent = ( 
      <div className="space-y-5 py-6 flex-grow"> 
        {(currentMessages.length === 0 && !isSendingMessage && !isLoadingData) && ( 
          <p className="text-center italic">Envoyez un message pour commencer.</p> 
        )} 
        {currentMessages.map((msg, index) => (
          <React.Fragment key={msg.uid || `msg-${index}`}>
            {/* PROMPT - reste en texte brut */}
            {msg.prompt && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }} 
                animate={{ opacity: 1, y: 0 }} 
                transition={{ duration: 0.3, delay: 0.05 * index }} 
                className={`flex items-end justify-start group relative ${isEditingMessage && editingMessageId === msg.uid ? 'opacity-70 pointer-events-none' : ''}`} 
              > 
                <div className={`bg-light-surface dark:bg-dark-surfaceContainer p-3 rounded-lg shadow-sm max-w-[85%] ${editingMessageId === msg.uid ? 'w-full border-2 border-light-primary/50 dark:border-dark-primary/50 ring-2 ring-light-primary/30 dark:ring-dark-primary/30' : ''}`}> 
                  {editingMessageId === msg.uid ? ( 
                    // Votre logique d'édition ...
                    <div className="flex flex-col gap-2">
                      <textarea 
                        ref={editInputRef} 
                        value={editText} 
                        onChange={(e) => setEditText(e.target.value)} 
                        onInput={(e) => { e.target.style.height = 'auto'; e.target.style.height = `${e.target.scrollHeight}px`; }} 
                        onKeyDown={(e) => { 
                          if (e.key === 'Enter' && !e.shiftKey) { 
                            e.preventDefault(); 
                            handleSaveEdit(msg.uid, editText); 
                          } else if (e.key === 'Escape') { 
                            handleCancelEdit(); 
                          }
                        }} 
                        className="w-full p-2 border rounded bg-light-surfaceContainerHigh dark:bg-dark-surfaceContainerHigh border-light-outline dark:border-dark-outline text-light-onSurface dark:text-dark-onSurface text-bodyLarge focus:ring-2 focus:ring-light-primary dark:focus:ring-dark-primary outline-none resize-none overflow-hidden min-h-[60px]" 
                        disabled={isEditingMessage} 
                        rows={1} 
                      /> 
                      <div className="flex justify-end items-center gap-2 mt-1 h-8"> 
                        {isEditingMessage ? <CircularProgress size="small" /> : ( 
                          <> 
                            <button 
                              onClick={() => handleSaveEdit(msg.uid, editText)} 
                              className="px-3 py-1 text-sm rounded bg-light-primary text-light-onPrimary dark:bg-dark-primary dark:text-dark-onPrimary hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed font-medium" 
                              disabled={!editText.trim()}
                            >Sauvegarder</button> 
                            <button 
                              onClick={handleCancelEdit} 
                              className="px-3 py-1 text-sm rounded bg-light-secondaryContainer text-light-onSecondaryContainer dark:bg-dark-secondaryContainer dark:text-dark-onSecondaryContainer hover:opacity-90 font-medium"
                            >Annuler</button> 
                          </> 
                        )} 
                      </div> 
                    </div> 
                  ) : (
                    <p className="text-bodyLarge whitespace-pre-wrap text-light-onSurface dark:text-dark-onSurface">
                      {msg.prompt}
                    </p>
                  )} 
                </div> 
                {/* Bouton d'édition ... */}
                {editingMessageId !== msg.uid && index === currentMessages.length - 1 && msg.prompt && !msg.isLoading && ( 
                  <div className="ml-2 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0"> 
                    <IconBtn 
                      icon="edit" 
                      size="small" 
                      title="Modifier" 
                      onClick={() => handleStartEdit(msg.uid, msg.prompt)} 
                      disabled={!!editingMessageId || !!renamingConvId || isSendingMessage || isCreatingConversation} 
                    /> 
                  </div> 
                )} 
              </motion.div>
            )}

            {/* RÉPONSE - utilisez StreamingMarkdown pour TOUS les cas */}
            {msg.response !== null && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }} 
                animate={{ opacity: 1, y: 0 }} 
                transition={{ duration: 0.3, delay: 0.1 }} 
                className="flex items-start justify-end"
              > 
                <div className='bg-light-secondaryContainer dark:bg-dark-secondaryContainer p-3 rounded-lg shadow-sm max-w-[85%]'> 
                  {/*  StreamingMarkdown gère automatiquement le formatage pendant l'édition aussi */}
                  <StreamingMarkdown 
                    content={msg.response || ''} 
                    isStreaming={msg.isLoading || false}
                    streamingText={editingMessageId === msg.uid ? 'Modification en cours...' : 'Génération en cours...'}
                  />
                </div> 
              </motion.div>
            )}

            
          </React.Fragment>
        ))} 
        <div ref={messagesEndRef} style={{ height: '1px' }} /> 
      </div> 
    );
  } else { 
    mainContent = <Greetings user={user} />; 
  }

  return (
    <>
      <PageTitle title={activeConversation ? activeConversation.title : 'ChatBot Fiqh Maliki'} />
      <div className='lg:grid lg:grid-cols-[320px,1fr] h-dvh overflow-hidden relative'>
        <Sidebar
          isSidebarOpen={isSidebarOpen}
          toggleSidebar={toggleSidebar}
          conversations={allConversations}
          onSelectConversation={handleSelectConversation}
          activeConversationUid={activeConversation?.uid}
          onDeleteConversation={handleDeleteConversation}
          onNewConversation={handleNewConversationRequest}
          isDeleting={isDeletingConversation}
          renamingConvId={renamingConvId}
          renameInputText={renameInputText}
          onStartRename={handleStartRename}
          onCancelRename={handleCancelRename}
          onSaveRename={handleSaveRename}
          onRenameInputChange={handleRenameInputChange}
          isSavingRename={isSavingRename}
        />
        <div
          className={`h-dvh grid grid-rows-[max-content,minmax(0,1fr),max-content] overflow-hidden bg-light-background dark:bg-dark-background transition-all duration-medium4 ease-standard ${contextHubMarginClass}`}
        >
          <TopAppBar toggleSidebar={toggleSidebar} user={user} toggleContextHub={toggleContextHub} />
          <div className='px-5 pb-5 flex flex-col overflow-y-auto'>
            <div className='max-w-[840px] w-full mx-auto flex-grow flex flex-col'>
              {mainContent}
            </div>
          </div>
          <div className='bg-light-background dark:bg-dark-background pt-2 pb-1 border-t border-light-outline/20 dark:border-dark-outline/20'>
            <div className='max-w-[870px] px-5 w-full mx-auto'>
              <PromptField
                onSubmit={handleSendMessage}
                isLoading={isSendingMessage || isCreatingConversation}
                isDisabled={isLoadingData || !!editingMessageId || !!renamingConvId}
                onUpload={handleFileUploadForPromptField}
                isUploading={isUploading}
              />
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5, delay: 0.8 }}
                className='text-bodySmall text-center text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant p-3'
              >
                Ce système RAG peut afficher des informations inexactes.
                <a href='#' className='inline underline ms-1'>vie privée & IA</a>
              </motion.p>
            </div>
          </div>
        </div>

        <ContextHubPanel
          isOpen={isContextHubOpen}
          onClose={toggleContextHub}
          title={activeConversation ? `Docs: ${activeConversation.title.substring(0,20)}${activeConversation.title.length > 20 ? '...' : ''}` : "Context Hub"}
          currentContextSize={currentContextSize}
          maxContextSize={maxContextSize}
          onFilesAdded={handleFileSubmitForContextHub}
          isUploading={isUploading}
          activeConversationId={activeConversation?.uid}
          documents={documentsInContext}
          onDeleteDocument={handleDeleteDocumentFromContext}
          onPreviewDocument={handlePreviewDocument}
          deletingDocumentId={deletingDocumentId}
          isLoading={isLoadingData}
          onToggleDocumentActive={handleToggleDocumentActiveState}
        />

        {isPreviewModalOpen && documentToPreview && (
          <DocumentPreview
            document={documentToPreview}
            isLoading={isPreviewLoading}
            onClose={handleClosePreview}
            onAdd={handleToggleActiveFromPreview}
          />
        )}

        {isContextHubOpen && window.innerWidth < 1024 && (
          <div className="fixed inset-0 bg-black/40 z-30" onClick={toggleContextHub}></div>
        )}
      </div>
    </>
  );
};

export default App;