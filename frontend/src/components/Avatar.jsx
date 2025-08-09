import PropTypes from "prop-types";

const Avatar = ({ name }) => {
  // Générer la première lettre du nom (ou "?" si pas de nom)
  const firstLetter = name ? name.charAt(0).toUpperCase() : "?";
  
  // Générer une couleur de fond basée sur le nom (pour avoir une couleur consistante pour chaque utilisateur)
  const getBackgroundColor = (name) => {
    if (!name) return "#FB8C00"; // Couleur par défaut si pas de nom
    
    // Calculer une valeur de hachage simple à partir du nom
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    // Convertir le hachage en une couleur HSL (teinte entre 0 et 360)
    const hue = hash % 360;
    return `hsl(${hue}, 70%, 60%)`;
  };

  const bgColor = getBackgroundColor(name);
  
  return (
    <figure className="avatar inline-flex items-center justify-center rounded-full bg-opacity-80 text-white w-10 h-10 overflow-hidden">
      {/* Si vous implémentez une image d'avatar plus tard, vous pourriez ajouter une condition ici */}
      <div 
        style={{ backgroundColor: bgColor }}
        className="w-full h-full flex items-center justify-center text-lg font-medium"
      >
        {firstLetter}
      </div>
    </figure>
  );
};

Avatar.propTypes = {
  name: PropTypes.string,
};

export default Avatar;