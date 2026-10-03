import apiClient from './client';

export const signup = async (userData) => {
  const response = await apiClient.post('/auth/signup', userData);
  return response.data;
};

export const login = async (email, password) => {
  const response = await apiClient.post('/auth/login', { email, password });
  if (response.data && response.data.access_token) {
    localStorage.setItem('token', response.data.access_token);
  }
  return response.data;
};
