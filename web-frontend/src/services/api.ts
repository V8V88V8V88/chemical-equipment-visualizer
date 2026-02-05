import axios from 'axios';
import type { AuthResponse, DatasetListItem, Dataset, Summary } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://chemical-equipment-visualizer-tiu4.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  register: async (username: string, email: string, password: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/register/', {
      username,
      email,
      password,
      password_confirm: password,
    });
    return response.data;
  },

  login: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await api.post('/auth/login/', { username, password });
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout/');
  },
};

export const datasetApi = {
  upload: async (file: File): Promise<Dataset> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  list: async (): Promise<DatasetListItem[]> => {
    const response = await api.get('/datasets/');
    return response.data;
  },

  get: async (id: number): Promise<Dataset> => {
    const response = await api.get(`/datasets/${id}/`);
    return response.data;
  },

  getSummary: async (id: number): Promise<Summary> => {
    const response = await api.get(`/datasets/${id}/summary/`);
    return response.data;
  },

  downloadReport: async (id: number, filename: string): Promise<void> => {
    const response = await api.get(`/datasets/${id}/report/`, {
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${filename}_report.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/datasets/${id}/`);
  },
};

export default api;
