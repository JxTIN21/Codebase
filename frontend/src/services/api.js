import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadCodebase = async (FormData) => {
    const response = await api.post('/upload-codebase', FormData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const searchCodebase = async (codebaseId, query) => {
    const response = await api.post('/search', {
        codebase_id: codebaseId,
        query: query,
    });
    return response.data;
};

export const getCodebaseStatus = async (codebaseId) => {
    const response = await api.get(`/codebase/${codebaseId}/status`);
    return response.data;
};

export default api;