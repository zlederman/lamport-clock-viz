<script lang="ts">
	import type { EventType, NodeMessage } from '$lib/queries';

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
		nodeId: string;
		msgTo?: string;
		idForSwimlane: number;
		x: number;
		y: number;
		eventType: EventType;
	};
	const messageSpacing = 20;
	const nodeRadius = 5;

	function getNodeColor(eventType: EventType): string {
		if (eventType === 'INTERNAL') {
			return 'blue';
		} else if (eventType === 'RECV') {
			return 'red';
		} else {
			return 'black';
		}
	}

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

			messageNodes.push({
				nodeId: message.node_id,
				msgTo: message.msg_to,
				idForSwimlane: counts[message.node_id],
				x,
				y,
				eventType: message.event_type
			});
		}

		return messageNodes;
	});

	type ArrowProps = {
		length: number;
		angle: number;
		from: {
			x: number;
			y: number;
		};
		dbg: {
			from: string;
			frid: number;
			to: string;
			toid: number;
		};
	};

	const arrows = $derived.by((): ArrowProps[] => {
		let arrows: ArrowProps[] = [];

		let sp: Record<string, number> = {};

		for (let i = 0; i < messageNodes.length; i++) {
			const node = messageNodes[i]!;
			if (node.msgTo === undefined || i === messageNodes.length - 1) {
				continue;
			}

			// find the receiver
			// assumes events from messages are received in order.
			// Otherwise, you can refactor messageNodes so we don't double loop
			// AND solve this problem.
			let to;
			for (let j = i + 1; j < messageNodes.length; j++) {
				const receiver = messageNodes[j]!;
				if (receiver.nodeId !== node.msgTo || receiver.eventType !== 'RECV') {
					continue;
				}
				// check sp to ensure that this node doesn't already have a receiver, and set it to this node
				let lastTaken = sp[receiver.nodeId];
				if (lastTaken === undefined) {
					sp[receiver.nodeId] = j;
				} else if (lastTaken >= j) {
					//means that this node is already taken
					continue;
				}
				to = {
					node: receiver.nodeId,
					sid: receiver.idForSwimlane,
					x: receiver.x,
					y: receiver.y
				};

				break;
			}

			if (!to) {
				console.error("couldn't find receiver for arrow for node", node);
				continue;
			}

			const from = {
				x: node.x,
				y: node.y
			};

			const length = Math.hypot(to.x - from.x, to.y - from.y);
			const angle = Math.atan2(to.y - from.y, to.x - from.x) * (180 / Math.PI);

			arrows.push({
				length,
				angle,
				from,
				dbg: {
					from: node.nodeId,
					frid: node.idForSwimlane,

					to: to.node,
					toid: to.sid
				}
			});
		}

		return arrows;
	});
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
				style:background-color={getNodeColor(messageNode.eventType)}
				style:top={messageNode.y + 'px'}
				style:left={messageNode.x + 'px'}
			>
				{messageNode.idForSwimlane}
			</div>
		{/each}
		{#each arrows as arrow}
			{@const dbg = arrow.dbg}
			<div
				class="arrow"
				style:left={arrow.from.x + 'px'}
				style:top={arrow.from.y + 'px'}
				style:width={arrow.length + 'px'}
				style:transform={`rotate(${arrow.angle}deg)`}
			>
				({dbg.from}:{dbg.frid}) => ({dbg.to}:{dbg.toid})
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

	.arrow {
		position: absolute;
		height: 2px;
		background-color: green;
		transform-origin: 0 0;
	}
</style>
