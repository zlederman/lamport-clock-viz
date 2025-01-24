<script lang="ts">
	import type { EventType, NodeMessage } from '$lib/queries';

	interface Props {
		nodes: string[];
		messages: NodeMessage[];
		swimlaneSpacing: number;
		nodeRadius: number;
		messageSpacing: number;
	}

	let { nodes, messages, swimlaneSpacing: spacing, messageSpacing, nodeRadius }: Props = $props();

	type SwimlaneProps = {
		y: number;
	};

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

	//const messageNode

	type MessageNode = {
		nodeId: string;
		msgTo?: string;
		msgFrom?: string;
		idForSwimlane: number;
		x: number;
		y: number;
		eventType: EventType;
	};

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
				msgFrom: message.msg_from,
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

		let takenNodes: Record<string, number[]> = {};

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
				if (
					receiver.nodeId !== node.msgTo ||
					receiver.eventType !== 'RECV' ||
					receiver.msgFrom !== node.nodeId
				) {
					continue;
				}
				// check sp to ensure that this node doesn't already have a receiver, and set it to this node
				let taken = takenNodes[receiver.nodeId];

				if (taken === undefined) {
					takenNodes[receiver.nodeId] = [receiver.idForSwimlane];
				} else if (taken.findIndex((p) => p === receiver.idForSwimlane) !== -1) {
					//this node is already taken
					continue;
				} else {
					// add to taken
					taken.push(receiver.idForSwimlane);
				}

				to = {
					node: receiver.nodeId,
					sid: receiver.idForSwimlane,
					x: receiver.x + nodeRadius,

					y: receiver.y + nodeRadius
				};

				break;
			}

			if (!to) {
				console.error("couldn't find receiver for arrow for node", node);
				continue;
			}

			const from = {
				x: node.x + nodeRadius,
				y: node.y + nodeRadius
			};

			const length = Math.hypot(to.x - from.x, to.y - from.y);
			const angle = Math.atan2(to.y - from.y, to.x - from.x) * (180 / Math.PI);

			const dbg = {
				from: node.nodeId,
				frid: node.idForSwimlane,

				to: to.node,
				toid: to.sid
			};

			arrows.push({
				length,
				angle,
				from,
				dbg
			});
		}

		return arrows;
	});

	const graphHeight = $derived(spacing * Math.max(nodes.length - 1, 0) + 'px');

	//todo: derive
	const graphWidth = $derived.by(() => {
		const defWidth = 600;
		if (messageNodes.length === 0) {
			return defWidth + 'px';
		}

		let lastNode = messageNodes[messageNodes.length - 1];

		return Math.max(lastNode.x, defWidth) + 'px';
	});
</script>

<div class="container">
	<div class="graph" style:height={graphHeight} style:width={graphWidth}>
		<!-- Swimlanes -->
		{#each Object.entries(swimlanes) as [node, props]}
			<div class="lane" style:top={props.y + 'px'}>{node}</div>
		{/each}

		<!-- Arrows -->
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
	</div>
</div>

<style lang="scss">
	.container {
		border: 1px solid black;
		padding: 40px 20px;
		overflow: auto;
		max-width: 80vw;
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
		font-size: 10px;
	}
</style>
