import React, { useEffect, useState } from 'react';
import { getCurrentUser } from '../services/api.ts'; // Assuming api.ts
import { getUserAppointments } from '../services/api.ts';
import { Link } from 'react-router-dom';

function Dashboard() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await getUserAppointments();
        setAppointments(response.data);
      } catch (err) {
        console.error("Failed to fetch appointments:", err);
        setError("Could not load your appointments.");
        // If the error is 404 from our custom endpoint message, we can handle it gracefully
        if (err.detail === "No appointments found") {
          setError(null); // It's not an error, just an empty state
          setAppointments([]);
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchAppointments();
  }, []);

  if (loading) return <p>Loading your appointments...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Your Dashboard</h2>
      <Link to="/book">Book a New Appointment</Link>
      <hr />
      <h3>Your Upcoming Appointments</h3>
      {appointments.length > 0 ? (
        <ul>
          {appointments.map(app => (
            <li key={app.id}>
              <strong>{app.service_name}</strong> on {new Date(app.start_time).toLocaleDateString()}
              {' at '}
              {new Date(app.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              {' - '}
              <em>Status: {app.status}</em>
            </li>
          ))}
        </ul>
      ) : (
        <p>You have no upcoming appointments.</p>
      )}
    </div>
  );
}

export default Dashboard;