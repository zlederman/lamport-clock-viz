import { client } from './client';

export type CreateRequest = {
	num_nodes: number;
	max_messages: number;
};

export type CreateResponse = {
	node_ids: string[];
};

export type EventType = 'SEND' | 'RECV' | 'INTERNAL';

export type NodeMessage = {
	node_id: string;
	timestamp: number;
	event_type: EventType;
	msg_to?: string;
};

export async function create(request: CreateRequest): Promise<CreateResponse> {
	const response = await client.post('/system/create', request);

	console.log('create response: ', response.data);
	return response.data;
}

export async function cleanup() {
	const response = await client.get('/system/cleanup');

	console.log('create response: ', response.data);
}
