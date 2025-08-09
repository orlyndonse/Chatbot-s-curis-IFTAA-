// src/components/ToggleIcons.jsx
import React from 'react';
import PropTypes from 'prop-types';

// Composant Toggle On
export const ToggleOnIcon = ({ size = 24, className = '', style = {}, ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={`toggle-on-icon ${className}`}
    style={style}
    {...props}
  >
    <rect
      x="2"
      y="6"
      width="20"
      height="12"
      rx="6"
      fill="currentColor"
      opacity="0.9"
    />
    <circle
      cx="16"
      cy="12"
      r="4"
      fill="white"
    />
  </svg>
);

// Composant Toggle Off
export const ToggleOffIcon = ({ size = 24, className = '', style = {}, ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={`toggle-off-icon ${className}`}
    style={style}
    {...props}
  >
    <rect
      x="2"
      y="6"
      width="20"
      height="12"
      rx="6"
      stroke="currentColor"
      strokeWidth="2"
      fill="none"
      opacity="0.6"
    />
    <circle
      cx="8"
      cy="12"
      r="4"
      fill="currentColor"
      opacity="0.6"
    />
  </svg>
);

// Composant Progress Activity (spinner)
export const ProgressActivityIcon = ({ size = 24, className = '', style = {}, ...props }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={`progress-activity-icon animate-spin ${className}`}
    style={style}
    {...props}
  >
    <path
      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
      fill="currentColor"
      opacity="0.3"
    />
    <path
      d="M12 2C17.52 2 22 6.48 22 12h-2c0-4.41-3.59-8-8-8V2z"
      fill="currentColor"
    />
  </svg>
);

ToggleOnIcon.propTypes = {
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  className: PropTypes.string,
  style: PropTypes.object,
};

ToggleOffIcon.propTypes = {
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  className: PropTypes.string,
  style: PropTypes.object,
};

ProgressActivityIcon.propTypes = {
  size: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
  className: PropTypes.string,
  style: PropTypes.object,
};