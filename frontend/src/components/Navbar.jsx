import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // <<< IMPORT useAuth HOOK
import './Navbar.css'; 

function Navbar() {
  const { isAuthenticated, logout } = useAuth(); // <<< GET AUTH STATE AND logout FUNCTION
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); // Call the logout function from context
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <nav className="navbar">
      <div className="navbar-links">
        {/* Always show Home/Brand link */}
        <Link to="/">Home</Link> 

        {isAuthenticated && ( // Conditionally render these links
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/book">Book Appointment</Link>
            <Link to="/manage">Manage Appointment</Link>
          </>
        )}
      </div>

      <div className="navbar-auth">
        {isAuthenticated ? (
          // If logged in, show a Logout button
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        ) : (
          // If not logged in, show Login and Register links
          <>
            <Link to="/login">Login</Link>
            {' | '}
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;