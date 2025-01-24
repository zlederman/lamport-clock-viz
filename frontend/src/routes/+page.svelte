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

	let numNodes = $state(3);
	let maxMessages = $state(2);
	let swimlaneSpacing = $state(80);
	let nodeRadius = $state(5);
	let messageSpacing = $state(20);
</script>

<div class="container">
	<div class="contents">
		<div class="actions">
			<div class="buttons">
				<button
					onclick={async () => {
						const res = await create({ num_nodes: numNodes, max_messages: maxMessages });
						nodes = res.node_ids;
					}}>Create</button
				>
				<button
					onclick={() => {
						start();
					}}>Start</button
				>
				<button onclick={() => cleanup()}>Cleanup</button>
			</div>

			<div class="config">
				<div class="opt">
					<label for="nn">Num Nodes: </label><input name="nn" type="number" bind:value={numNodes} />
				</div>
				<div class="opt">
					<label for="mm">Max Messages: </label><input
						name="mm"
						type="number"
						bind:value={maxMessages}
					/>
				</div>
				<div class="opt">
					<label for="sl">Swimlane spacing: </label><input
						name="sl"
						type="number"
						bind:value={swimlaneSpacing}
					/>
				</div>
				<div class="opt">
					<label for="nr">Node Radius: </label><input
						name="nr"
						type="number"
						bind:value={nodeRadius}
					/>
				</div>
				<div class="opt">
					<label for="ms">Message Spacing: </label><input
						name="ms"
						type="number"
						bind:value={messageSpacing}
					/>
				</div>
			</div>
		</div>

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
			<Graph {nodes} {messages} {swimlaneSpacing} {nodeRadius} {messageSpacing} />
		</div>
		<div class="messages">
			<h2>Messages:</h2>
			{#each messages as message}
				<div class="message">{JSON.stringify(message)}</div>
			{/each}
		</div>
	</div>
</div>

<style lang="scss">
	.container {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 20px;
	}
	.contents {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 4px;
	}
	button {
		background-color: gray;
		color: white;
		border-radius: 4px;
		padding: 4px;
	}

	.actions {
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.config {
		display: flex;
		flex-direction: column;

		.opt {
			display: flex;
			justify-content: space-between;
			gap: 8px;
			input {
				width: 50px;
			}
		}
	}
</style>
