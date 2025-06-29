import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Function to set JWT for authenticated requests
// This will be important AFTER successful login
export const setAuthToken = (token: string | null) => {
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common['Authorization'];
  }
};

interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  // Add other fields your backend might return on login, e.g., user details
}

export const loginUser = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const formData = new URLSearchParams();
  formData.append('username', credentials.email); // FastAPI OAuth2PasswordRequestForm expects 'username'
  formData.append('password', credentials.password);

  try {
    const response = await apiClient.post<LoginResponse>('/users/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  } catch (error) {
    // Handle or re-throw error for the component to manage
    console.error("Login API error:", error);
    if (axios.isAxiosError(error) && error.response) {
        throw error.response.data; // Throw backend error message if available
    }
    throw new Error('Login failed. Please try again.');
  }
};

// --- Registration Interfaces and Function (NEW or VERIFY) ---
interface RegisterCredentials {
  email: string;
  password: string;
  full_name: string; // Or fullName, match your backend UserCreate Pydantic schema
}

interface RegisterResponse { // Assuming backend returns the created user
  id: number;
  email: string;
  full_name: string; // Or fullName
  is_active: boolean;
  is_superuser: boolean;
}

export const registerUser = async (userData: RegisterCredentials): Promise<RegisterResponse> => {
  try {
    // For registration, we send JSON data
    const response = await apiClient.post<RegisterResponse>('/users/register', userData, {
        headers: { 'Content-Type': 'application/json' } // Explicitly set, though often default for Axios POST
    });
    return response.data;
  } catch (error) {
    console.error("Registration API error:", error);
    if (axios.isAxiosError(error) && error.response) {
        throw error.response.data; // Throw backend error message if available
    }
    throw new Error('Registration failed. Please try again.');
  }
};

export const getAppointmentById = (id: number) => {
  // The ID is passed in the URL path
  return apiClient.get(`/appointments/${id}`);
};

export const updateAppointment = (id: number, appointmentData: any) => {
  // The ID is in the URL path, and the update data is in the request body
  return apiClient.put(`/appointments/${id}`, appointmentData);
};

export const deleteAppointment = (id: number) => {
  // The ID is passed in the URL path
  return apiClient.delete(`/appointments/${id}`);
};


export const getCurrentUser = () => apiClient.get('/users/me');
export const getUserAppointments = () => apiClient.get('/appointments/');
export const createAppointment = (appointmentData: any) => apiClient.post('/appointments/', appointmentData);
export default apiClient;