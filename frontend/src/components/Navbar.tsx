import React from "react";
import { Link } from "react-router-dom";

const Navbar: React.FC = () => {
  // TODO: Add logic for conditional rendering based on auth status
  return (
    <nav
      style={{
        marginBottom: "20px",
        paddingBottom: "10px",
        borderBottom: "1px solid #ccc",
      }}
    >
      <Link to="/" style={{ marginRight: "10px" }}>
        Dashboard
      </Link>
      <Link to="/book" style={{ marginRight: "10px" }}>
        Book Appointment
      </Link>
      <Link to="/login" style={{ marginRight: "10px" }}>
        Login
      </Link>
      <Link to="/register">Register</Link>
      {/* TODO: Add Logout button */}
    </nav>
  );
};

export default Navbar;
