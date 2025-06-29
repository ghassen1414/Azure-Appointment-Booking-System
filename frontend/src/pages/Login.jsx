import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser, setAuthToken } from '../services/api.ts'; 
import { useAuth } from '../context/AuthContext'; 

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { login } = useAuth(); 

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    try {
      const data = await loginUser({ email, password });
      if (data.access_token) {
        login(data.access_token); 
        navigate('/dashboard'); 
      }
    } catch (err) {
      console.error("Login page error:", err);
      const errorMessage = err?.detail || err?.message || 'Login failed. Please check your credentials.';
      setError(errorMessage);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="login-email">Email:</label>
          <input
            type="email"
            id="login-email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <br />
        <div>
          <label htmlFor="login-password">Password:</label>
          <input
            type="password"
            id="login-password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <br />
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit">Login</button>
      </form>
      {/* TODO: Add Link to Register Page: import { Link } from 'react-router-dom'; <Link to="/register">Register</Link> */}
    </div>
  );
}

export default Login;