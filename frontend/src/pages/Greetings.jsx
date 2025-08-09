import { motion } from "motion/react";
import PropTypes from "prop-types";

const Greetings = ({ user }) => { 
  return (
    <div className='grid place-content-center h-full'> 
      <h2 className='text-headlineLarge font-semibold text-center tracking-tight text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant'>
        <motion.span 
          initial={{ backgroundPositionX: '100%' }}
          animate={{ backgroundPositionX: '0%' }} 
          transition={{ duration: 4, ease: [0.05, 0.7, 0.1, 1] }}
          className='bg-gradient-to-r from-amber-600 from-0% via-amber-500 via-56% to-transparent to-75% bg-[length:350%_100%] bg-[100%_0] bg-clip-text text-transparent'>
          مرحبا، {user?.first_name || 'Orly'}
        </motion.span> 
        <br />
        <motion.span     
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.3, ease:'easeOut' }}
          className='dark: font-medium'
        >
          كيف يمكنني مساعدتك؟
        </motion.span>
      </h2>
    </div>
  );
};

Greetings.propTypes = {
  user: PropTypes.object
};

export default Greetings;
