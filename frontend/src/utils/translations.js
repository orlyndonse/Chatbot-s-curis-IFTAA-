export const translations = {
  fr: {
    toggleTheme: (theme) => `Thème ${theme === 'light' ? 'sombre' : 'clair'}`,
    documentation: 'Documentation',
    logout: 'Se déconnecter',
    language: 'Changer de langue',
    profile: 'Mon Profil',
    userManagement: 'Gestion Utilisateurs',
  },
  ar: {
    toggleTheme: (theme) => `المظهر ${theme === 'light' ? 'الداكن' : 'الفاتح'}`,
    documentation: 'التوثيق',
    logout: 'تسجيل الخروج',
    language: 'تغيير اللغة',
    profile: 'ملفي الشخصي',
    userManagement: 'إدارة المستخدمين',
  },
  en: {
    toggleTheme: (theme) => `${theme === 'light' ? 'Dark' : 'Light'} Theme`,
    documentation: 'Documentation',
    logout: 'Log out',
    language: 'Change Language',
    profile: 'My Profile',
    userManagement: 'User Management',
  }
};