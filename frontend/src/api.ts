import axios from 'axios';

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();

if (import.meta.env.PROD && !configuredBaseUrl) {
  throw new Error(
    'VITE_API_BASE_URL must be configured for production builds. See frontend/.env.example.',
  );
}

const baseURL = (configuredBaseUrl || 'http://127.0.0.1:8000').replace(/\/+$/, '');

export const api = axios.create({ baseURL });
