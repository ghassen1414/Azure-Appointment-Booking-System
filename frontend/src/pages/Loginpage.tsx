import React, { useState, FormEvent } from "react"; // Added FormEvent
import { useNavigate } from "react-router-dom";
import { loginUser, setAuthToken } from "../services/api"; // Assuming api.ts is in ../services/

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      const loginData = await loginUser({ email, password }); // loginUser from api.ts
      if (loginData.access_token) {
        localStorage.setItem("accessToken", loginData.access_token);
        setAuthToken(loginData.access_token); // Configure Axios instance
        // Optionally: Fetch user details here and store in context/global state
        navigate("/"); // Navigate to dashboard (which is '/' in your App.tsx PrivateRoute)
      } else {
        setError("Login failed: No access token received.");
      }
    } catch (err: any) {
      console.error("Login page error:", err);
      // err might be the error object thrown from api.ts (e.g., err.detail)
      // or a generic Error object
      const errorMessage =
        err?.detail ||
        err?.message ||
        "Login failed. Please check your credentials.";
      setError(errorMessage);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="login-email">Email:</label>{" "}
          {/* Best practice to associate label with input */}
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
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit">Login</button>
      </form>
      {/* TODO: Add Link to Register Page: <Link to="/register">Don't have an account? Register</Link> */}
    </div>
  );
};

export default LoginPage;
