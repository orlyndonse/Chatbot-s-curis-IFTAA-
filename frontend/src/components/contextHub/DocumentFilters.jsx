import React from 'react';
import PropTypes from 'prop-types';
import TextField from '../TextField';
import Icon from '../Icon';

const DocumentFilters = ({
  searchTerm,
  onSearchTermChange,
  sortOption,
  onSortOptionChange,

}) => {
  return (
    <div className="document-filters mb-3 p-1 bg-light-surfaceContainer dark:bg-dark-surfaceContainer rounded-lg">
      <TextField
        name="documentSearch"
        type="search"
        placeholder="Rechercher des documents par nom..."
        value={searchTerm}
        onChange={(e) => onSearchTermChange(e.target.value)}
        fieldClasses="text-sm h-11 !ring-1 focus:!ring-2" 
        label="Rechercher des documents" 
        classes="mb-2" 
      />
      <div className="mt-2 flex items-center justify-between"> {/*Mise en page flexible */}
        <label 
            htmlFor="sortOption" 
            className="text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mr-2 shrink-0" // Prevent label from shrinking
        >
            Trier par :
        </label>
        <select
          id="sortOption"
          name="sortOption"
          value={sortOption}
          onChange={(e) => onSortOptionChange(e.target.value)}
          className="p-2 h-10 w-full rounded-md border border-light-outline dark:border-dark-outline bg-light-surface dark:bg-dark-surface text-bodySmall focus:ring-1 focus:ring-light-primary focus:border-light-primary dark:focus:ring-dark-primary dark:focus:border-dark-primary appearance-none"
          // Ajout de appearance-none pour permettre un style personnalisé de la flèche de sélection si souhaité (via des plugins Tailwind ou du CSS personnalisé).
        >
          <option value="upload_date_desc">Date d'ajout (Plus récent d'abord)</option>
          <option value="upload_date_asc">Date d'ajout (Plus ancien d'abord)</option>
          <option value="filename_asc">Nom (A-Z)</option>
          <option value="filename_desc">Nom (Z-A)</option>
          <option value="size_desc">Taille (Plus volumineux d'abord)</option>
          <option value="size_asc">Taille (Plus petit d'abord)</option>
        </select>
      </div>
    </div>
  );
};

DocumentFilters.propTypes = {
  searchTerm: PropTypes.string.isRequired,
  onSearchTermChange: PropTypes.func.isRequired,
  sortOption: PropTypes.string.isRequired,
  onSortOptionChange: PropTypes.func.isRequired,
};

export default DocumentFilters;