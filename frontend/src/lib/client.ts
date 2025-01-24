import axios from 'axios';

export const ENDPOINT = "https://lamport-clock-viz-production.up.railway.app"

export const client = axios.create({
	baseURL: ENDPOINT
});
