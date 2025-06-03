import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export const submitQuery = (query) =>
  axios.post(`${API_BASE}/query`, { query });

export const searchByKeyword = (q) =>
  axios.get(`${API_BASE}/documents/search`, { params: { q } });

export const fetchDocumentById = (id) =>
  axios.get(`${API_BASE}/documents/${id}`);

export const uploadPDF = (formData) =>
  axios.post(`${API_BASE}/upload/pdf`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
