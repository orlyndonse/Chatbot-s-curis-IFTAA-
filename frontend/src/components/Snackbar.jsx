/**
* @copyright 2025 isetsfax
*/

/**
 * Node modules
 */

import PropTypes from "prop-types";
import { motion, AnimatePresence } from "motion/react";

const Snackbar = ({ snackbar }) => {

    const snackbarVariant = {
        hidden: { scaleY: 0 },
        visible: {
            scaleY: 1,
            transition: {
                duration: 0.2,
                ease: [0.05, 0.7, 0.1, 1],
            }
        }
    }

    const snackbarChildVariant = {
        hidden: { opacity: 0 },
        visible: {opacity: 1}
    }
    return (
        <AnimatePresence>
            {snackbar.open && (
                <motion.div 
                variants={snackbarVariant} 
                initial='hidden'
                animate='visible'
                exit={{
                    opacity:0,
                    transition: {
                        duration: 0.15,
                        ease: 'easeOut',
                    },
                }}
                className={`snackbar ${snackbar.type}`}
                >
                    <motion.span 
                        variants={snackbarChildVariant}
                        transition={{ 
                            duration:0.2, 
                            delay:0.1, 
                            ease:'easeOut' }}
                    >
                        {snackbar.message}
                    </motion.span>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

Snackbar.propTypes = {
    snackbar: PropTypes.shape({
      open: PropTypes.bool.isRequired,
      message: PropTypes.string.isRequired,
      type: PropTypes.oneOf(['error', 'success', 'info']), 
      duration: PropTypes.number
    })
  };

export default Snackbar;