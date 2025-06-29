import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser } from '../services/api.ts'; // Import from your api.ts (adjust path if needed)
// import { Link } from 'react-router-dom'; // For a "Already have an account? Login" link

function Register() { // Or RegisterPage, be consistent
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState(''); // Good practice for registration
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      // Ensure the field name matches your backend (e.g., full_name or fullName)
      const userData = { email, password, full_name: fullName }; 
      const responseData = await registerUser(userData);
      
      console.log("Registration successful:", responseData);
      setSuccessMessage("Registration successful! Please log in.");
      // Optionally, redirect to login after a short delay or directly
      setTimeout(() => {
        navigate('/login');
      }, 2000); // Redirect after 2 seconds

    } catch (err) {
      console.error("Registration page error:", err);
      const errorMessage = err?.detail || err?.message || 'Registration failed. Please try again.';
      setError(errorMessage);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="register-fullname">Full Name:</label>
          <input
            type="text"
            id="register-fullname"
            placeholder="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />
        </div>
        <br />
        <div>
          <label htmlFor="register-email">Email:</label>
          <input
            type="email"
            id="register-email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <br />
        <div>
          <label htmlFor="register-password">Password:</label>
          <input
            type="password"
            id="register-password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <br />
        <div>
          <label htmlFor="register-confirm-password">Confirm Password:</label>
          <input
            type="password"
            id="register-confirm-password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <br />
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
        <button type="submit">Register</button>
      </form>
      {/* <p>Already have an account? <Link to="/login">Login here</Link></p> */}
    </div>
  );
}

export default Register;