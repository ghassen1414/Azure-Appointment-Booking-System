import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; 
import { createAppointment, updateAppointment } from '../services/api.ts'; 

function BookAppointment() {
  const navigate = useNavigate();
  const location = useLocation(); // Hook to access route state from navigate()

  // --- NEW: Check if we are in "edit mode" ---
  const appointmentToEdit = location.state?.appointmentToEdit;
  const isEditMode = !!appointmentToEdit; // Will be true if appointmentToEdit exists, otherwise false

  // --- NEW: Helper function to format datetime strings for the input field ---
  const formatDateTimeForInput = (isoString) => {
    if (!isoString) return '';
    return isoString.slice(0, 16);
  };

  // --- UPDATED: State initialization is now aware of edit mode ---
  const [serviceName, setServiceName] = useState(appointmentToEdit?.service_name || 'Initial Consultation');
  const [startTime, setStartTime] = useState(formatDateTimeForInput(appointmentToEdit?.start_time));
  const [notes, setNotes] = useState(appointmentToEdit?.notes || '');

  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // --- UPDATED: handleSubmit now handles both create and update ---
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setSuccessMessage(null);

    if (!startTime) {
      setError("Please select a start date and time.");
      return;
    }

    // Determine duration based on selected service
    const durationInMinutes = serviceName === 'Standard Session' ? 60 : serviceName === 'Online Meeting' ? 45 : 30;
    const startDateTime = new Date(startTime);
    const endDateTime = new Date(startDateTime.getTime() + durationInMinutes * 60000);

    const appointmentData = {
      service_name: serviceName,
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString(),
      notes: notes,
    };

    try {
      if (isEditMode) {
        // --- EDIT LOGIC ---
        await updateAppointment(appointmentToEdit.id, appointmentData);
        setSuccessMessage("Appointment updated successfully! Redirecting to dashboard...");
      } else {
        // --- CREATE LOGIC (your original logic) ---
        await createAppointment(appointmentData);
        setSuccessMessage("Appointment booked successfully! Redirecting to dashboard...");
      }

      // Common logic for both cases
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);

    } catch (err) {
      console.error("Booking/Editing page error:", err);
      const errorMessage = err?.detail || err?.message || 'Operation failed. The time slot may be unavailable or in the past.';
      setError(errorMessage);
    }
  };

  // --- UPDATED: The returned JSX is now dynamic based on edit mode ---
  return (
    <div>
      <h2>{isEditMode ? `Edit Appointment (ID: ${appointmentToEdit.id})` : 'Book a New Appointment'}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="service">Service Type:</label>
          <select id="service" value={serviceName} onChange={(e) => setServiceName(e.target.value)}>
            <option value="Initial Consultation">Initial Consultation (30 mins)</option>
            <option value="Standard Session">Standard Session (60 mins)</option>
            <option value="Online Meeting">Online Meeting (45 mins)</option>
          </select>
        </div>
        <br />
        <div>
          <label htmlFor="start-time">Start Date and Time:</label>
          <input
            type="datetime-local"
            id="start-time"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            required
          />
        </div>
        <br />
        <div>
          <label htmlFor="notes">Notes (optional):</label>
          <textarea
            id="notes"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>
        <br />
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
        <button type="submit">
          {isEditMode ? 'Update Appointment' : 'Book Appointment'}
        </button>
      </form>
    </div>
  );
}

export default BookAppointment;