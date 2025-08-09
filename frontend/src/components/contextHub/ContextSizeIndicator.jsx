// source code/frontend/src/components/contextHub/ContextSizeIndicator.jsx
import React from 'react';
import PropTypes from 'prop-types';
import Icon from '../Icon';

const ContextSizeIndicator = ({ currentSize, maxSize }) => {
  const percentage = maxSize > 0 ? (currentSize / maxSize) * 100 : 0;
  const displayCurrentSize = (currentSize / 1024).toFixed(1); // KB
  const displayMaxSize = (maxSize / 1024).toFixed(1); // KB

  let progressBarColor = 'bg-green-500 dark:bg-green-400'; // Default
  if (percentage > 85) {
    progressBarColor = 'bg-red-500 dark:bg-red-400'; // Critical
  } else if (percentage > 60) {
    progressBarColor = 'bg-yellow-500 dark:bg-yellow-400'; // Warning
  }

  return (
    <div className="context-size-indicator my-3">
      <div className="flex justify-between text-bodySmall text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant mb-1 px-1">
        <span>Taille du contexte</span>
        <span>{displayCurrentSize}Ko / {displayMaxSize}Ko</span>
      </div>
      <div className="h-2 w-full bg-light-surfaceContainerHighest dark:bg-dark-surfaceContainerHighest rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-300 ease-out ${progressBarColor}`}
          style={{ width: `${Math.min(percentage, 100)}%` }} // Cap at 100%
          role="progressbar"
          aria-valuenow={percentage}
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
    </div>
  );
};

ContextSizeIndicator.propTypes = {
  currentSize: PropTypes.number.isRequired,
  maxSize: PropTypes.number.isRequired,
};

export default ContextSizeIndicator;