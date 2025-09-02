/**
* @copyright 2025 isetsfax
*/

import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { motion } from "motion/react";
import Icon from "./Icon";

const Button = ({
    classes = '',
    variant='filled',
    color= 'primary',
    children,
    ... rest
    }) => {
    return (
        <motion.button 
            className={`btn ${variant} ${color} ${classes}`}
            { ...rest}
        > 
        {children}
        <div className='state-layer'></div> 
    </motion.button>
    );
};

Button.propTypes = {
    classes: PropTypes.string,
    variant:PropTypes.string,
    color: PropTypes.string,
    children: PropTypes.any,
};

const IconBtn = ({ 
    classes = '', 
    icon, 
    size = '', 
    children, 
    ...rest 
}) => { 
    const iconSize = size === 'small' ? 16 : size === 'large' ? 24 : 20;
    
    return (
        <button
            className={`icon-btn ${size} ${classes}`}
            {...rest}
        >
            {children}

            {!children && icon && (
                <Icon name={icon} size={iconSize} />
            )}
            
            <div className='state-layer'></div>
        </button>
    );
};

IconBtn.propTypes = { 
    classes: PropTypes.string, 
    icon: PropTypes.string, 
    size: PropTypes.string, 
    children: PropTypes.any,
};

const ExtendedFab = ({ href, text, classes = '', ... rest }) => {
    if (href) {
        return (
            <Link
                to={href}
                className={`extended-fab ${classes}`}
                { ... rest}
            >
                <Icon name="add" size={20} />
                <span className="truncate">{text}</span>
                <div className='state-layer'></div>
            </Link>
        );
    }
    
    // Version bouton pour onClick
    return (
        <button
            className={`extended-fab ${classes}`}
            { ... rest}
        >
            <Icon name="add" size={20} />
            <span className="truncate">{text}</span>
            <div className='state-layer'></div>
        </button>
    );
};

ExtendedFab.propTypes = {
    href: PropTypes.string,
    text: PropTypes.string,
    classes: PropTypes.string,
};

const UploadButton = ({ 
    classes = '', 
    isLoading = false, 
    isDisabled = false, 
    onChange, 
    multiple = false, 
    accept = '*/*',
    ...rest 
}) => {
    return (
        <div className={`relative ${classes}`}>
            <IconBtn
                icon={isLoading ? 'sync' : 'upload'}
                size="large"
                classes={`${isLoading ? 'animate-spin' : ''}`}
                disabled={isDisabled || isLoading}
                {...rest}
            />
            <input
                type="file"
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                onChange={onChange}
                disabled={isDisabled || isLoading}
                multiple={multiple}
                accept={accept}
            />
        </div>
    );
};

UploadButton.propTypes = {
    classes: PropTypes.string,
    isLoading: PropTypes.bool,
    isDisabled: PropTypes.bool,
    onChange: PropTypes.func.isRequired,
    multiple: PropTypes.bool,
    accept: PropTypes.string,
};

export {Button, IconBtn, ExtendedFab, UploadButton };