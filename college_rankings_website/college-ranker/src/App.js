import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Container } from '@mui/material';
import Navbar from './components/Navbar';
import CollegeRanker from './components/CollegeRanker';
import UserColleges from './components/UserColleges';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Navbar />
        <Container maxWidth="md" sx={{ mt: 4 }}>
          <Routes>
            <Route path="/" element={<CollegeRanker />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/my-colleges" element={
              <PrivateRoute>
                <UserColleges />
              </PrivateRoute>
            } />
          </Routes>
        </Container>
      </AuthProvider>
    </Router>
  );
}

const PrivateRoute = ({ children }) => {
  const { currentUser } = useAuth();
  return currentUser ? children : <Navigate to="/login" />;
};

export default App;