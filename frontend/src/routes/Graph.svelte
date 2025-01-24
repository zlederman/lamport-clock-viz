<script lang="ts">
	import type { NodeMessage } from '$lib/queries';

	interface Props {
		nodes: string[];
		messages: NodeMessage[];
	}

	let { nodes, messages }: Props = $props();

	type NodeProps = {
		y: number;
	};

	const spacing = 80;

	const graphHeight = $derived(spacing * nodes.length + 'px');

	//todo: derive
	const graphWidth = '600px';

	const nodeProps = $derived.by((): Record<string, NodeProps> => {
		const props: Record<string, NodeProps> = {};
		for (let i = 0; i < nodes.length; i++) {
			const node = nodes[i]!;
			props[node] = {
				y: spacing * i
			};
		}

		return props;
	});
</script>

<div class="container">
	<div class="graph" style:height={graphHeight} style:width={graphWidth}>
		{#each Object.entries(nodeProps) as [node, props]}
			<div class="lane" style:top={props.y + 'px'}>{node}</div>
		{/each}
	</div>
</div>

<style lang="scss">
	.container {
		border: 1px solid black;
		padding: 20px;
	}
	.graph {
		position: relative;
	}

	.lane {
		position: absolute;
		height: 1px;
		background-color: black;
		width: 100%;
	}
</style>
