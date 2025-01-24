import axios from 'axios';

export const ENDPOINT = import.meta.env.VITE_ENDPOINT

export const client = axios.create({
	baseURL: ENDPOINT
});
