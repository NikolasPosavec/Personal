import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      setCurrentUser(user);
    }
    setLoading(false);
  }, []);

  const login = (userData) => {
    localStorage.setItem('user', JSON.stringify(userData));
    setCurrentUser(userData);
  };

  const register = (userData) => {
    localStorage.setItem('user', JSON.stringify(userData));
    setCurrentUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('user');
    setCurrentUser(null);
  };

  const saveColleges = (colleges) => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      user.colleges = colleges;
      localStorage.setItem('user', JSON.stringify(user));
      setCurrentUser(user);
    }
  };

  return (
    <AuthContext.Provider value={{ currentUser, login, register, logout, saveColleges, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);