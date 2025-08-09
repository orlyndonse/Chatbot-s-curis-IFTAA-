// source code/frontend/src/components/contextHub/DocumentFilters.jsx
import React from 'react';
import PropTypes from 'prop-types';
import TextField from '../TextField'; // Assuming TextField.jsx is in src/components/
import Icon from '../Icon';

const DocumentFilters = ({
  searchTerm,
  onSearchTermChange,
  sortOption,
  onSortOptionChange,
  // Future props for filtering by type or status can be added here
  // filterType,
  // onFilterTypeChange,
  // filterStatus,
  // onFilterStatusChange,
}) => {
  return (
    <div className="document-filters mb-3 p-1 bg-light-surfaceContainer dark:bg-dark-surfaceContainer rounded-lg">
      <TextField
        name="documentSearch"
        type="search" // Using type="search" can give a clear 'x' button in some browsers
        placeholder="Rechercher des documents par nom..."
        value={searchTerm}
        onChange={(e) => onSearchTermChange(e.target.value)}
        fieldClasses="text-sm h-11 !ring-1 focus:!ring-2" // Adjusted for a more compact look
        // Using ! to ensure these override default TextField styles if specificity is an issue
        label="Rechercher des documents" // Label will animate based on TextField's internal logic
        classes="mb-2" // Add some margin below the search field
      />
      <div className="mt-2 flex items-center justify-between"> {/* Flex layout for sort */}
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
          // Added appearance-none for custom styling of select arrow if desired (via Tailwind plugins or custom CSS)
        >
          <option value="upload_date_desc">Date d'ajout (Plus récent d'abord)</option>
          <option value="upload_date_asc">Date d'ajout (Plus ancien d'abord)</option>
          <option value="filename_asc">Nom (A-Z)</option>
          <option value="filename_desc">Nom (Z-A)</option>
          <option value="size_desc">Taille (Plus volumineux d'abord)</option>
          <option value="size_asc">Taille (Plus petit d'abord)</option>
          {/* Example for future status filter (would require isActiveInContext to be filterable):
            <option value="status_active">Statut (Actif)</option>
            <option value="status_inactive">Statut (Inactif)</option> 
          */}
        </select>
      </div>
      {/* Placeholder for future filter dropdowns (e.g., by type, by status) */}
      {/* <div className="mt-2">
        <label htmlFor="filterType" className="text-bodySmall ...">Filtrer par type :</label>
        <select id="filterType" value={filterType} onChange={onFilterTypeChange} className="...">
          <option value="">Tous les types</option>
          <option value="application/pdf">PDF</option>
          <option value="text/plain">Texte</option>
          // Add more types
        </select>
      </div> 
      */}
    </div>
  );
};

DocumentFilters.propTypes = {
  searchTerm: PropTypes.string.isRequired,
  onSearchTermChange: PropTypes.func.isRequired,
  sortOption: PropTypes.string.isRequired,
  onSortOptionChange: PropTypes.func.isRequired,
  // filterType: PropTypes.string,
  // onFilterTypeChange: PropTypes.func,
  // filterStatus: PropTypes.string,
  // onFilterStatusChange: PropTypes.func,
};

export default DocumentFilters;