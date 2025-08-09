// Icon.jsx
import PropTypes from 'prop-types';
import { useIcon } from '../hooks/useIcon';

const Icon = ({ name, size = 20, className = '', ...rest }) => {
  const iconPath = useIcon(name);
  
  if (!iconPath) {
    // Fallback pour les icônes non trouvées
    return (
      <span 
        className={`material-symbols-rounded ${className}`} 
        style={{ fontSize: size }}
        {...rest}
      >
        {name}
      </span>
    );
  }
  
  return (
    <img
      src={iconPath}
      alt={name}
      width={size}
      height={size}
      className={`icon ${className}`}
      style={{ width: size, height: size }}
      {...rest}
    />
  );
};

Icon.propTypes = {
  name: PropTypes.string.isRequired,
  size: PropTypes.number,
  className: PropTypes.string,
};

export default Icon;