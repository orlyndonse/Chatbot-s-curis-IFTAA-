// MenuItem.jsx - Mis à jour avec icônes locales
import PropTypes from 'prop-types';
import Icon from './Icon';

const MenuItem = ({ 
  classes = '', 
  icon, 
  labelText, 
  onClick, 
  destructive = false,
  ...rest
}) => {
  return (
    <button
      className={`menu-item ${destructive ? 'destructive' : ''} ${classes}`}
      onClick={onClick}
      type="button"
      {...rest}
    >
      {icon && (
        <Icon 
          name={icon} 
          size={18} 
          className="mr-3"
        />
      )}
      <span>{labelText}</span>
      <div className="state-layer"></div>
    </button>
  );
};

MenuItem.propTypes = {
  classes: PropTypes.string,
  icon: PropTypes.string,
  labelText: PropTypes.string.isRequired,
  onClick: PropTypes.func,
  destructive: PropTypes.bool,
};

export default MenuItem;