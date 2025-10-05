import { motion } from 'framer-motion';
import { useRef, useCallback, useState, useEffect } from "react";
import PropTypes from "prop-types";
import { IconBtn } from "./Button";

const PromptField = ({ onSubmit, isLoading, isDisabled = false }) => {
  const inputField = useRef();
  const inputFieldContainer = useRef();

  const [isMultiline, setMultiline] = useState(false);
  const [inputValue, setInputValue] = useState('');

  // Recalculer l'état multiligne lors du redimensionnement ou du rendu initial
  useEffect(() => {
    const checkMultiline = () => {
        if (inputFieldContainer.current) {
            setMultiline(inputFieldContainer.current.clientHeight > 64);
        }
    };
    checkMultiline();
    window.addEventListener('resize', checkMultiline);
    return () => window.removeEventListener('resize', checkMultiline);
  }, []);

  // Maintenir le focus après un chargement ou un changement d'état
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (inputField.current && !isLoading && !isDisabled) {
        inputField.current.focus();
      }
    }, 50);
    
    return () => clearTimeout(timeoutId);
  }, [isLoading, isDisabled]);

  const handleInputChange = useCallback(() => {
    if (!inputField.current) return;
    
    const currentText = inputField.current.innerText.trim();
    setMultiline(inputFieldContainer.current.clientHeight > 64);
    setInputValue(currentText);
    
    // Forcer la div à être véritablement vide lorsqu'il n'y a pas de texte
    if (!currentText && inputField.current.innerHTML !== '') {
      inputField.current.innerHTML = '';
    }
  }, []);

  const moveCursorToEnd = useCallback(() => {
    if (!inputField.current) return;
    const editableElem = inputField.current;
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(editableElem);
    range.collapse(false);
    if (selection) {
        selection.removeAllRanges();
        selection.addRange(range);
    }
  }, []);

  const handlePaste = useCallback((e) => {
    e.preventDefault();
    if (!inputField.current) return;
    const text = e.clipboardData.getData('text/plain');
    document.execCommand('insertText', false, text);
    handleInputChange();
    moveCursorToEnd();
  }, [handleInputChange, moveCursorToEnd]);

  const handleSubmit = useCallback(() => {
    const trimmedValue = inputField.current?.innerText.trim();
    if (!trimmedValue || isLoading || isDisabled) return;

    onSubmit(trimmedValue);

    if (inputField.current) {
      inputField.current.innerHTML = ''; // On vide le contenu

      // --- CORRECTION : Forcer un "reflow" du navigateur ---
      // Cette astuce (retirer puis redonner le focus en une fraction de seconde) 
      // force le navigateur à recalculer complètement le style et la géométrie du champ.
      // Il "réalise" qu'il est vide, lui redonne sa hauteur d'origine, et le placeholder
      // ainsi que le curseur se repositionnent alors correctement.
      inputField.current.blur();
      inputField.current.focus();
    }
    
    // Le reste de la réinitialisation de l'état
    setInputValue('');
    setMultiline(false);
  }, [inputValue, isLoading, isDisabled, onSubmit]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }, [handleSubmit]);

  const promptFieldVariant = {
    hidden: { scaleY: 0, opacity: 0 },
    visible: {
      scaleY: 1,
      opacity: 1,
      transition: {
        when: 'beforeChildren',
        staggerChildren: 0.1,
        duration: 0.4,
        delay: 0.2,
        ease: [0.2, 0.65, 0.3, 0.9],
      },
    },
  };

  const promptFieldChildrenVariant = {
    hidden: { opacity: 0, y: 5 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.3, ease: 'easeOut' }},
  };

  const containerClasses = `prompt-field-container flex items-end p-2 bg-light-surfaceContainer dark:bg-dark-surfaceContainer ${isMultiline ? 'rounded-2xl' : 'rounded-full'} transition-all duration-200 ease-out ${isDisabled ? 'opacity-70 cursor-not-allowed' : ''}`;
  const inputClasses = `prompt-field grow relative mx-4 py-3 text-light-onSurface dark:text-dark-onSurface text-bodyLarge outline-none whitespace-pre-wrap max-h-[230px] overflow-y-auto`;

  // Déterminer si le bouton doit être actif
  const isButtonActive = !isLoading && !isDisabled && inputValue.trim();

  return (
    <motion.div 
      className={containerClasses}
      variants={promptFieldVariant}
      initial='hidden'
      animate='visible'
      ref={inputFieldContainer}
    > 
      <motion.div
        className={inputClasses} 
        contentEditable={!isLoading && !isDisabled}
        role='textbox' 
        aria-multiline={true}
        aria-label='Entrer un prompt ici' 
        data-placeholder='Entrer un prompt ici'
        variants={promptFieldChildrenVariant}
        ref={inputField}
        onInput={handleInputChange}
        onPaste={handlePaste}
        onKeyDown={handleKeyDown}
      />
      <div className="flex items-center gap-2 ms-auto">
        <motion.div variants={promptFieldChildrenVariant}>
          <IconBtn
            icon={isLoading ? "sync" : "send"}
            size="large"
            classes={`${isLoading ? 'animate-spin' : ''} ${isButtonActive ? 'text-light-primary dark:text-dark-primary' : 'opacity-50'}`}
            onClick={handleSubmit}
            disabled={!isButtonActive}
          />
        </motion.div>
      </div>
    </motion.div>
  );
};

PromptField.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  isLoading: PropTypes.bool,
  isDisabled: PropTypes.bool,
};

export default PromptField;