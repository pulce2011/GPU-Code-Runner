import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

// Recupera token dal localStorage se presente
let accessToken = localStorage.getItem('accessToken') || null;
let refreshToken = localStorage.getItem('refreshToken') || null;

// Crea istanza Axios
const api = axios.create({ baseURL: API_URL });

// Aggiunge Authorization header prima di ogni richiesta
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
        // Richiesta refresh token
        const res = await axios.post(`${API_URL}/token/refresh/`, {
          refresh: refreshToken
        });

        // Aggiorna token
        accessToken = res.data.access;
        localStorage.setItem('accessToken', accessToken);

        // Ripeti richiesta originale con nuovo token
        originalRequest.headers['Authorization'] = `Bearer ${accessToken}`;
        return axios(originalRequest);
      } catch (err) {
        console.error('Refresh token fallito', err);
        // Pulizia token se refresh fallisce
        accessToken = null;
        refreshToken = null;
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }
    }

    return Promise.reject(error);
  }
);

// Funzione per impostare i token dopo login
export const setTokens = (access, refresh) => {
  accessToken = access;
  refreshToken = refresh;

  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
};

export default api;
