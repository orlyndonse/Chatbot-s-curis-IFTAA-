import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import router from './routers/routes'
import './index.css'
import { UserProvider } from './contexts/UserContext' 
import SnackbarProvider from './contexts/SnackbarContext'
import { LanguageProvider } from './contexts/LanguageContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <UserProvider>
      <LanguageProvider> {/* <- Envelopper l'application */}
        <SnackbarProvider>
          <RouterProvider router={router} />
        </SnackbarProvider>
      </LanguageProvider>
    </UserProvider>
  </StrictMode>
)