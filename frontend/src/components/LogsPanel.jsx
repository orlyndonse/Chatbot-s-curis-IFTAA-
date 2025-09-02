import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const LogsPanel = ({ isOpen, onClose, logs }) => {
  const logsEndRef = useRef(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ x: '100%' }}
      animate={{ x: 0 }}
      exit={{ x: '100%' }}
      transition={{ duration: 0.3 }}
      className="fixed top-0 right-0 h-dvh w-[300px] bg-light-surfaceContainer dark:bg-dark-surfaceContainer z-40 shadow-lg overflow-y-auto"
    >
      <div className="p-4 border-b border-light-outline dark:border-dark-outline">
        <h2 className="text-lg font-semibold text-light-onSurface dark:text-dark-onSurface">Logs en Temps Réel</h2>
        <button
          onClick={onClose}
          className="ml-2 text-light-onSurfaceVariant dark:text-dark-onSurfaceVariant hover:text-light-primary dark:hover:text-dark-primary"
        >
          ×
        </button>
      </div>
      <div className="p-4 text-sm text-light-onSurface dark:text-dark-onSurface">
        {logs.map((log, index) => (
          <div key={index} className="mb-2 animate-pulse-once">
            {log}
          </div>
        ))}
        <div ref={logsEndRef} />
      </div>
    </motion.div>
  );
};

export default LogsPanel;