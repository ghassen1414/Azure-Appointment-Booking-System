import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import BookAppointment from "./pages/BookAppointment";
import "./App.css";
import PrivateRoute from './components/PrivateRoute';
import ManageAppointments from "./pages/ManageAppointment"; // Import the ManageAppointments page

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<PrivateRoute />}> {/* Wrap protected routes */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/book" element={<BookAppointment />} />
          <Route path="/manage" element={<ManageAppointments />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
