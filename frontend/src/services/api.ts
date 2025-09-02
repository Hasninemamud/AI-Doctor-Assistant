import axios, { AxiosResponse } from 'axios';
import { 
  LoginCredentials, 
  RegisterData, 
  AuthTokens, 
  User, 
  Consultation,
  MedicalHistory,
  AnalysisResponse 
} from '../types';

// Create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const tokens = JSON.parse(localStorage.getItem('tokens') || 'null');
    if (tokens?.access_token) {
      config.headers.Authorization = `Bearer ${tokens.access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens') || 'null');
        if (tokens?.refresh_token) {
          const response = await axios.post(
            `${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/auth/refresh`,
            { refresh_token: tokens.refresh_token }
          );
          
          const newTokens = response.data;
          localStorage.setItem('tokens', JSON.stringify(newTokens));
          
          // Retry the original request with new token
          original.headers.Authorization = `Bearer ${newTokens.access_token}`;
          return api(original);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('tokens');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials: LoginCredentials): Promise<AxiosResponse<AuthTokens>> =>
    api.post('/auth/login', credentials),
    
  register: (userData: RegisterData): Promise<AxiosResponse<User>> =>
    api.post('/auth/register', userData),
    
  refreshToken: (refreshToken: string): Promise<AxiosResponse<AuthTokens>> =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
    
  logout: (): Promise<AxiosResponse<any>> =>
    api.post('/auth/logout'),
    
  getCurrentUser: (): Promise<AxiosResponse<User>> =>
    api.get('/users/me'),
};

// User API
export const userAPI = {
  getProfile: (): Promise<AxiosResponse<User>> =>
    api.get('/users/me'),
    
  updateProfile: (profileData: Partial<User>): Promise<AxiosResponse<User>> =>
    api.put('/users/me', profileData),
    
  getMedicalHistory: (): Promise<AxiosResponse<MedicalHistory>> =>
    api.get('/users/me/medical-history'),
    
  updateMedicalHistory: (historyData: Partial<MedicalHistory>): Promise<AxiosResponse<MedicalHistory>> =>
    api.put('/users/me/medical-history', historyData),
    
  createMedicalHistory: (historyData: Partial<MedicalHistory>): Promise<AxiosResponse<MedicalHistory>> =>
    api.post('/users/me/medical-history', historyData),
};

// Consultation API
export const consultationAPI = {
  create: (consultationData: any): Promise<AxiosResponse<Consultation>> =>
    api.post('/consultations/', consultationData),
    
  getAll: (): Promise<AxiosResponse<Consultation[]>> =>
    api.get('/consultations/'),
    
  getById: (id: string): Promise<AxiosResponse<Consultation>> =>
    api.get(`/consultations/${id}`),
    
  update: (id: string, updateData: any): Promise<AxiosResponse<Consultation>> =>
    api.put(`/consultations/${id}`, updateData),
    
  submitSymptoms: (id: string, symptomsData: any): Promise<AxiosResponse<Consultation>> =>
    api.post(`/consultations/${id}/symptoms`, symptomsData),
    
  analyze: (id: string): Promise<AxiosResponse<AnalysisResponse>> =>
    api.post(`/consultations/${id}/analyze`, {
      consultation_id: id,
      include_test_reports: true,
      include_symptoms: true,
      include_medical_history: true,
    }),
    
  getAnalyses: (id: string): Promise<AxiosResponse<any[]>> =>
    api.get(`/consultations/${id}/analyses`),
    
  uploadFile: (consultationId: string, file: File): Promise<AxiosResponse<any>> => {
    const formData = new FormData();
    formData.append('file', file);
    
    return api.post(`/files/upload/${consultationId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

// File API
export const fileAPI = {
  getFile: (fileId: string): Promise<AxiosResponse<any>> =>
    api.get(`/files/${fileId}`),
    
  deleteFile: (fileId: string): Promise<AxiosResponse<any>> =>
    api.delete(`/files/${fileId}`),
};

export default api;