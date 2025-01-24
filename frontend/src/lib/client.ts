import axios from 'axios';

export const ENDPOINT = 'http://localhost:8000';

export const client = axios.create({
	baseURL: ENDPOINT
});
