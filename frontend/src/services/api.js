import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

let accessToken = null;
let refreshToken = null;

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
    if (error.response.status === 401 && refreshToken) {
      try {
        const res = await axios.post(`${API_URL}/token/refresh/`, { refresh: refreshToken });
        accessToken = res.data.access;
        originalRequest.headers['Authorization'] = `Bearer ${accessToken}`;
        return axios(originalRequest);
      } catch (err) {
        console.error('Refresh token fallito', err);
      }
    }
    return Promise.reject(error);
  }
);

export const setTokens = (access, refresh) => {
  accessToken = access;
  refreshToken = refresh;
};

export default api;
