// TopAppBar.jsx - Mis à jour avec icônes locales
import PropTypes from "prop-types";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { IconBtn } from "./Button";
import Avatar from "./Avatar";
import Menu from "./Menu";
import MenuItem from "./MenuItem";
import Logo from "./Logo";
import Icon from "./Icon"; // Import du composant Icon
import { useLanguage } from '../contexts/LanguageContext';
import { translations } from '../utils/translations';

const TopAppBar = ({ toggleSidebar, user, toggleContextHub }) => {
  const navigate = useNavigate();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const userMenuRef = useRef(null);
  const avatarButtonRef = useRef(null);

  const { language, toggleLanguage } = useLanguage();
  const t = translations[language];

  // Theme Toggle State and Logic
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || 'dark';
  });

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const handleThemeToggle = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    setShowUserMenu(false);
  };

  const userDisplayName = user?.username || user?.first_name || "";

  const handleLogout = async () => {
    const token = localStorage.getItem("awesomeLeadsToken");
    try {
      await fetch("http://localhost:8000/api/v1/auth/logout", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
      });
    } catch (error) {
      console.error("Erreur lors de la déconnexion:", error);
    } finally {
      localStorage.removeItem("awesomeLeadsToken");
      localStorage.removeItem("awesomeLeadsRefreshToken");
      navigate("/login");
    }
  };

  const handleOpenDocs = () => {
    window.open('http://localhost:3001/my-docs/', '_blank', 'noopener,noreferrer');
    setShowUserMenu(false);
  };

  const handleLanguageChange = () => {
    toggleLanguage();
    setShowUserMenu(false);
  };

  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        showUserMenu &&
        userMenuRef.current &&
        !userMenuRef.current.contains(event.target) &&
        avatarButtonRef.current &&
        !avatarButtonRef.current.contains(event.target)
      ) {
        setShowUserMenu(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showUserMenu]);

  return (
    <header className='relative flex justify-between items-center h-16 px-4'>
      {/* Left section: Sidebar toggle and Logo for mobile */}
      <div className='flex items-center gap-1'>
        <IconBtn
          icon='menu'
          title='Menu'
          size='small'
          classes='lg:hidden'
          onClick={toggleSidebar}
        />
        <Logo classes='lg:hidden'/>
      </div>

      {/* Right section: Context Hub Toggle and User Menu */}
      <div className="flex items-center gap-2">
        {/* Button to toggle Context Hub Panel */}
        <IconBtn
          icon="topic"
          title="Toggle Context Hub"
          size="small"
          onClick={toggleContextHub}
        />

        {/* User Avatar and Dropdown Menu */}
        <div className="relative">
          <div ref={avatarButtonRef}>
            <IconBtn onClick={toggleUserMenu}>
              <Avatar name={userDisplayName} />
            </IconBtn>
          </div>
          
          <div ref={userMenuRef}>
            <Menu classes={`${showUserMenu ? 'active' : ''} z-30`}>
              
              {/* Menu Item: Language */}
              <MenuItem
                icon='language'
                labelText={t.language}
                onClick={handleLanguageChange}
              />
            
              {/* Menu Item: Theme */}
              <MenuItem
                icon={theme === 'light' ? 'dark_mode' : 'light_mode'}
                labelText={t.toggleTheme(theme)}
                onClick={handleThemeToggle}
              />

              {/* Menu Item: Documentation */}
              <MenuItem
                icon='help_outline'
                labelText={t.documentation}
                onClick={handleOpenDocs}
              />

              {/* Menu Item: Logout */}
              <MenuItem
                icon='logout'
                labelText={t.logout}
                onClick={handleLogout}
              />

            </Menu>
          </div>
        </div>
      </div>
    </header>
  );
};

TopAppBar.propTypes = {
  toggleSidebar: PropTypes.func,
  user: PropTypes.object,
  toggleContextHub: PropTypes.func.isRequired,
};

export default TopAppBar;