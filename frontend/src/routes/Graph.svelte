<script lang="ts">
	import type { NodeMessage } from '$lib/queries';

	interface Props {
		nodes: string[];
		messages: NodeMessage[];
	}

	let { nodes, messages }: Props = $props();

	type SwimlaneProps = {
		y: number;
	};

	const spacing = 80;

	const graphHeight = $derived(spacing * Math.max(nodes.length - 1, 0) + 'px');

	//todo: derive
	const graphWidth = '600px';

	const swimlanes = $derived.by((): Record<string, SwimlaneProps> => {
		const props: Record<string, SwimlaneProps> = {};
		for (let i = 0; i < nodes.length; i++) {
			const node = nodes[i]!;
			props[node] = {
				y: spacing * i
			};
		}

		return props;
	});

	$inspect('swimlanes: ', swimlanes);

	//const messageNode

	type MessageNode = {
		id_for_node: number;
		x: number;
		y: number;
		color: string;
	};
	const messageSpacing = 20;
	const nodeRadius = 5;

	const messageNodes = $derived.by((): MessageNode[] => {
		const messageNodes: MessageNode[] = [];

		//holds a count for the nodes, ignores arrow numbers
		const counts: Record<string, number> = {};

		//ignore timestamp, assumed that messages are received in order
		for (const message of messages) {
			const swimlane = swimlanes[message.node_id];
			const x = messageSpacing * messageNodes.length - nodeRadius;
			const y = swimlane.y - nodeRadius;
			//set new count
			const countForNode = counts[message.node_id];
			if (countForNode === undefined) {
				counts[message.node_id] = 1;
			} else {
				counts[message.node_id] += 1;
			}

			let color = 'black';
			if (message.event_type === 'INTERNAL') {
				color = 'blue';
			} else if (message.event_type === 'RECV') {
				color = 'red';
			}

			messageNodes.push({
				id_for_node: counts[message.node_id],
				x,
				y,
				color
			});
		}

		return messageNodes;
	});

	type ArrowProps = {
		from: {
			x: number;
			y: number;
		};
		to: {
			x: number;
			y: number;
		};
	};
</script>

<div class="container">
	<div class="graph" style:height={graphHeight} style:width={graphWidth}>
		<!-- Swimlanes -->
		{#each Object.entries(swimlanes) as [node, props]}
			<div class="lane" style:top={props.y + 'px'}>{node}</div>
		{/each}

		<!-- Nodes -->
		{#each messageNodes as messageNode}
			<div
				class="message-node"
				style:width={nodeRadius * 2 + 'px'}
				style:height={nodeRadius * 2 + 'px'}
				style:background-color={messageNode.color}
				style:top={messageNode.y + 'px'}
				style:left={messageNode.x + 'px'}
			>
				{messageNode.id_for_node}
			</div>
		{/each}
	</div>
</div>

<style lang="scss">
	.container {
		border: 1px solid black;
		padding: 40px 20px;
	}
	.graph {
		position: relative;
	}

	.message-node {
		border-radius: 100%;
		outline: 1px solid black;
		position: absolute;
		color: white;
		font-size: 10px;
		text-align: center;
		vertical-align: center;
	}

	.lane {
		position: absolute;
		height: 1px;
		background-color: black;
		width: 100%;
	}
</style>
