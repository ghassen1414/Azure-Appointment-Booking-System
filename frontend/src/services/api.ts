import axios from 'axios';

// Use environment variable for API base URL
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// TODO: Add interceptor for adding JWT token to requests
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken'); // Or get from state management
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});


// Example service functions (you'll add many more)
export const registerUser = (userData: any) => { // TODO: Define proper type for userData
  return apiClient.post('/users/register', userData);
};

export const loginUser = (credentials: any) => { // TODO: Define proper type for credentials
  return apiClient.post('/token', new URLSearchParams(credentials)); // FastAPI token endpoint expects form data
};

export const fetchDashboardData = () => {
  return apiClient.get('/users/me/appointments'); // Example protected route
};

// TODO: Add more service functions for appointments, etc.

export default apiClient;