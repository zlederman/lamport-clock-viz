<script lang="ts">
	import { ENDPOINT } from '$lib/client';
	import { create, cleanup, type NodeMessage } from '$lib/queries';
	import Graph from './Graph.svelte';

	let nodes: string[] = $state([]);

	let messages: NodeMessage[] = $state([]);

	//let poll = $state(false);

	$inspect(messages);

	function start() {
		const eventSource = new EventSource(ENDPOINT + '/system/start');

		eventSource.onmessage = (event) => {
			messages.push(JSON.parse(event.data));
		};

		eventSource.onerror = () => {
			eventSource.close();
		};

		eventSource.onopen = () => {
			console.log('Connection established');
		};

		console.log('Event Source Created');
	}
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
<div class="container">
	<button
		onclick={async () => {
			const res = await create({ num_nodes: 3, max_messages: 2 });
			nodes = res.node_ids;
		}}>Create</button
	>
	<button
		onclick={() => {
			start();
		}}>Start</button
	>
	<button onclick={() => cleanup()}>Cleanup (does nothing)</button>

	{#if nodes.length !== 0}
		<h2>Nodes:</h2>
		<div class="nodes">
			{#each nodes as node}
				<div class="node">{node}</div>
			{/each}
		</div>
	{/if}

	<div class="graph">
		<h2>Graph</h2>
		<Graph {nodes} {messages} />
	</div>
	<div class="messages">
		<h2>Messages:</h2>
		{#each messages as message}
			<div class="message">{JSON.stringify(message)}</div>
		{/each}
	</div>
</div>

<style lang="scss">
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 4px;
	}
	button {
		background-color: gray;
		color: white;
		border-radius: 4px;
		padding: 4px;
	}
</style>
