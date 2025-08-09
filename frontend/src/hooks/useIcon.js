// hooks/useIcon.js
import { useMemo } from 'react';

// Configuration centralisée des icônes
const ICON_CONFIG = {
  // Icônes d'interface
  'send': '/src/assets/icons/paper-airplane.svg',
  'upload': '/src/assets/icons/cloud-arrow-up.svg',
  'sync': '/src/assets/icons/arrow-right.svg',
  'add': '/src/assets/icons/plus_icon.svg',
  'menu': '/src/assets/icons/menu_icon.svg',
  'close': '/src/assets/icons/x-mark.svg',
  'check': '/src/assets/icons/check-badge.svg',
  'info': '/src/assets/icons/information-circle.svg',
  'warning': '/src/assets/icons/exclamation-triangle.svg',
  'error': '/src/assets/icons/exclamation-circle.svg',
  'lock': '/src/assets/icons/lock-closed.svg',
  'document': '/src/assets/icons/document.svg',
  'document-text': '/src/assets/icons/document-text.svg',
  'document-word': '/src/assets/icons/document-word.svg',
  'photo': '/src/assets/icons/photo.svg',
  'eye': '/src/assets/icons/eye.svg',
  'trash': '/src/assets/icons/trash.svg',
  'pencil': '/src/assets/icons/pencil.svg',
  'archive': '/src/assets/icons/archive-box.svg',
  'envelope': '/src/assets/icons/envelope.svg',
  'user': '/src/assets/icons/UserPlus.svg',
  'shield': '/src/assets/icons/shield-check.svg',
  'presentation': '/src/assets/icons/presentation-chart-line.svg',
  'table': '/src/assets/icons/table-cells.svg',
  'arrows-right-left': '/src/assets/icons/arrows-right-left.svg',
  
  // Icônes pour TopAppBar
  'topic': '/src/assets/icons/squares-2x2.svg',
  'language': '/src/assets/icons/language.svg',
  'dark_mode': '/src/assets/icons/moon.svg',
  'light_mode': '/src/assets/icons/sun.svg',
  'help_outline': '/src/assets/icons/question-mark-circle.svg',
  'logout': '/src/assets/icons/arrow-right-on-rectangle.svg',
  
  // Icônes pour Sidebar
  'chat_bubble': '/src/assets/icons/chat-bubble-left.svg',
  'drive_file_rename_outline': '/src/assets/icons/pencil.svg',
  'delete': '/src/assets/icons/trash.svg',

  'toggle_on': '/src/assets/icons/toggle-on.svg',
  'toggle_off': '/src/assets/icons/toggle-off.svg',
  'visibility': '/src/assets/icons/eye.svg',
  'progress_activity': '@/assets/icons/arrow-path.svg',
  'picture_as_pdf': '@/assets/icons/document-text.svg',
  'slideshow': '@/assets/icons/presentation-chart-line.svg',
  'archive': '@/assets/icons/archive-box.svg'
};

export const useIcon = (iconName) => {
  const iconPath = useMemo(() => {
    const path = ICON_CONFIG[iconName];
    if (!path) {
      console.warn(`Icon "${iconName}" not found in ICON_CONFIG`);
      return null;
    }
    return path;
  }, [iconName]);

  return iconPath;
};

export const getIconPath = (iconName) => {
  return ICON_CONFIG[iconName] || null;
};

export const getAllIcons = () => {
  return Object.keys(ICON_CONFIG);
};
