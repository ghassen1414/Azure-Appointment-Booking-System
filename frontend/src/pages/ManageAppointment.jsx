import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// Import all necessary API functions
import { getAppointmentById, updateAppointment, deleteAppointment } from '../services/api.ts';

function ManageAppointment() {
  const [searchId, setSearchId] = useState('');
  const [appointment, setAppointment] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const navigate = useNavigate();

  const handleFindAppointment = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setAppointment(null);
    setIsEditing(false);
    try {
      const response = await getAppointmentById(parseInt(searchId, 10));
      setAppointment(response.data);
    } catch (err) {
      setError('Appointment not found or you do not have access.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to cancel this appointment?")) return;
    
    setError(null);
    try {
      await deleteAppointment(appointment.id);
      alert("Appointment successfully cancelled!");
      navigate('/dashboard'); // Go back to dashboard after deletion
    } catch (err) {
      setError('Failed to cancel appointment. Please try again.');
    }
  };
  
  // TODO: A more robust update form could be here.
  // For a quick demo, we can just allow changing the notes or status.
  const handleUpdateNotes = async (newNotes) => {
     try {
        await updateAppointment(appointment.id, { notes: newNotes });
        alert("Appointment notes updated!");
        // Refetch the appointment to show updated data
        handleFindAppointment({ preventDefault: () => {} }); // "Re-find" to refresh
     } catch (err) {
        setError('Failed to update notes.');
     }
  };

  return (
    <div>
      <h2>Manage Your Appointment</h2>
      
      <form onSubmit={handleFindAppointment}>
        <label htmlFor="appointment-id">Enter Appointment ID:</label>
        <input
          type="text"
          id="appointment-id"
          value={searchId}
          onChange={(e) => setSearchId(e.target.value)}
          placeholder="e.g., 1"
          required
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Finding...' : 'Find Appointment'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {appointment && (
        <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '15px' }}>
          <h3>Appointment Details (ID: {appointment.id})</h3>
          <p><strong>Service:</strong> {appointment.service_name}</p>
          <p><strong>Time:</strong> {new Date(appointment.start_time).toLocaleString()}</p>
          <p><strong>Status:</strong> {appointment.status}</p>
          <p><strong>Notes:</strong> {appointment.notes || 'N/A'}</p>
          
          <hr/>
          
          <button onClick={() => navigate('/book', { state: { appointmentToEdit: appointment } })}>
            Edit Appointment Time
          </button>

          <button onClick={handleDelete} style={{ marginLeft: '10px', backgroundColor: 'red', color: 'white' }}>
            Cancel Appointment
          </button>
        </div>
      )}
    </div>
  );
}

export default ManageAppointment;