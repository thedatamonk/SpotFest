// src/services/axios.js
import axios from 'axios';

const baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000'; // Default URL

const axiosInstance = axios.create({
  baseURL: baseURL
});

export default axiosInstance;
