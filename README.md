# SaaS Appointment Booking System

A cloud-hosted, full-stack application designed for consultancies to manage their client appointments. This project was developed as part of a university cloud course, emphasizing modern web technologies and Platform-as-a-Service (PaaS) integrations on Microsoft Azure.

![SaaS Appointment Booking System Demo](link-to-a-demo-gif-or-screenshot.png) 

---

##  Core Features

*   **Secure User Authentication:** Clients can register for an account and log in using a secure, token-based (JWT) system.
*   **Dynamic Appointment Booking:** An intuitive interface for booking appointments from a list of predefined services (Initial Consultation, Standard Session, Online Meeting).
*   **Robust Validation:** The backend enforces business logic, preventing double-bookings and scheduling appointments in the past.
*   **Self-Service Management:** Users can update or cancel their appointments using a unique ID provided via email.
*   **Automated Email Notifications:** Instant email confirmations, updates, and cancellations are sent to users for every booking event.

---

## Tech Stack & Cloud Architecture

This project is built on a modern, decoupled full-stack architecture, leveraging Microsoft Azure for key services.

### Frontend
*   **Framework:** React (using JavaScript/JSX)
*   **Routing:** React Router
*   **HTTP Client:** Axios
*   **Styling:** CSS

### Backend
*   **Framework:** Python with FastAPI
*   **Authentication:** JWT (JSON Web Tokens) with Passlib for password hashing.
*   **Database ORM:** SQLAlchemy
*   **Schema Validation:** Pydantic
*   **Database Migrations:** Alembic

### Cloud Integration (Microsoft Azure)
*   **Database:** **Azure SQL Database** (PaaS) - For scalable, managed, and persistent data storage.
*   **Email Notifications:** **Azure Communication Services (ACS)** (PaaS) - For sending reliable, transactional emails.
*   **Planned Hosting:**
    *   **Frontend:** Azure Static Web Apps
    *   **Backend:** Azure App Service (using Docker containers)


---

## Getting Started (Local Development)

Follow these instructions to get the project running on your local machine for development and testing purposes.

### Prerequisites

*   Node.js (v16+) and npm
*   Python (v3.9+)
*   An active Microsoft Azure subscription
*   Azure SQL Database and Azure Communication Services resources provisioned
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Optional, but recommended for future deployment)

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    # Create the venv (only once)
    python -m venv .venv

    # Activate the venv (every time you work on the project)
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    # source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    *   Copy the example environment file: `cp .env.example .env` (or just copy/paste and rename it).
    *   Edit the `.env` file and fill in your actual credentials for:
        *   `DATABASE_URL` (your Azure SQL DB connection string)
        *   `SECRET_KEY` (generate a strong random string)
        *   `ACS_CONNECTION_STRING`
        *   `ACS_SENDER_ADDRESS`
        *   Ensure `BACKEND_CORS_ORIGINS` is set to `'["http://localhost:3000"]'` for local development.
5.  **Run Database Migrations:**
    *   Make sure your database is accessible.
    *   Apply all migrations:
        ```bash
        # Ensure your venv is active
        python -m alembic upgrade head
        ```
6.  **Run the Backend Server:**
    ```bash
    # Ensure your venv is active
    python -m uvicorn app.main:app --reload
    ```
    The backend API will be running at `http://localhost:8000`. You can access the interactive documentation at `http://localhost:8000/api/v1/docs`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Configure Environment Variables:**
    *   Copy the example file: `cp .env.example .env` (or copy/paste and rename).
    *   Ensure your `.env` file contains:
        ```
        REACT_APP_API_BASE_URL=http://localhost:8000/api/v1
        ```
4.  **Run the Frontend Development Server:**
    ```bash
    npm start
    ```
    The frontend application will open in your browser at `http://localhost:3000`.

---
