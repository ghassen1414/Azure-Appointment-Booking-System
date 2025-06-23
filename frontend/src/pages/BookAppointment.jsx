import { useState } from "react";

function BookAppointment() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    type: "Initial Consultation",
    date: "",
    time: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Appointment booked:\n${JSON.stringify(form, null, 2)}`);
    // Later: send to backend
  };

  return (
    <div>
      <h2>Book a Consultancy Appointment</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="name"
          type="text"
          placeholder="Your Name"
          value={form.name}
          onChange={handleChange}
          required
        />
        <br /><br />
        <input
          name="email"
          type="email"
          placeholder="Your Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <br /><br />
        <select name="type" value={form.type} onChange={handleChange}>
          <option>Initial Consultation</option>
          <option>Standard Session</option>
          <option>Online Meeting</option>
        </select>
        <br /><br />
        <input
          name="date"
          type="date"
          value={form.date}
          onChange={handleChange}
          required
        />
        <br /><br />
        <input
          name="time"
          type="time"
          value={form.time}
          onChange={handleChange}
          required
        />
        <br /><br />
        <button type="submit">Book</button>
      </form>
    </div>
  );
}

export default BookAppointment;
