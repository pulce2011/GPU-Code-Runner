import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

// Recupera token dal localStorage
let accessToken = localStorage.getItem('accessToken') || null;
let refreshToken = localStorage.getItem('refreshToken') || null;

// Crea istanza Axios
const api = axios.create({ baseURL: API_URL });

// Pulisce token
const clearTokens = () => {
  accessToken = null;
  refreshToken = null;
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};

// Aggiunge Authorization header
api.interceptors.request.use(
  (config) => {
    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor per refresh token automatico
api.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && refreshToken) {
      try {
        const response = await axios.post(`${API_URL}/token/refresh/`, {
          refresh: refreshToken
        });

        accessToken = response.data.access;
        localStorage.setItem('accessToken', accessToken);

        originalRequest.headers['Authorization'] = `Bearer ${accessToken}`;
        return axios(originalRequest);
      } catch (error) {
        console.error('Refresh token fallito:', error);
        clearTokens();
      }
    }

    return Promise.reject(error);
  }
);

// Funzione per impostare i token
export const setTokens = (access, refresh) => {
  accessToken = access;
  refreshToken = refresh;
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
};

export default api;
