import axios from 'axios';

export const ENDPOINT = import.meta.env.ENDPOINT

export const client = axios.create({
	baseURL: ENDPOINT
});
