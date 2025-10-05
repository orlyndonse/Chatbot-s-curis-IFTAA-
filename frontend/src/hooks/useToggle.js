// src/hooks/useToggle.js

import { useState, useCallback } from "react";

// Accepte une valeur initiale (ex: true ou false)
const useToggle = (initialState = false) => {
    const [isOpen, setToggle] = useState(initialState);
    
    const toggle = useCallback(() => { 
        setToggle((prev) => !prev);
    }, []);

    return [isOpen, toggle];
};

export { useToggle };