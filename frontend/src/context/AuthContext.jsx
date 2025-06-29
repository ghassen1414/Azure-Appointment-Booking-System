import React, { createContext, useState, useContext, useEffect } from 'react';
import { setAuthToken } from '../services/api.ts'; 

// Create the context
const AuthContext = createContext(null);

// Create the provider component
export const AuthProvider = ({ children }) => {
  // We initialize the state by checking localStorage for an existing token
  const [authToken, setAuthTokenState] = useState(localStorage.getItem('accessToken'));
  // You could also store a user object here: const [user, setUser] = useState(null);

  useEffect(() => {
    // When the component mounts, ensure the Axios helper has the token if it exists
    if (authToken) {
      setAuthToken(authToken);
    }
  }, [authToken]); // This effect runs when authToken state changes

  const login = (token) => {
    localStorage.setItem('accessToken', token);
    setAuthToken(token); // Configure Axios
    setAuthTokenState(token); // Update React state
    // You could fetch and set user data here as well
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    setAuthToken(null); // Clear Axios headers
    setAuthTokenState(null); // Update React state
    // Clear any user data you have stored
  };

  const value = {
    authToken,
    isAuthenticated: !!authToken, // A handy boolean flag
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Create a custom hook for easy access to the context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};