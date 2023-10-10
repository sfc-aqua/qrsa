<script lang="ts">
	import { networks } from '../stores/network';
	import Ping from './Ping.svelte';
	export let qnodeId: string | undefined;
	let currentQNodeId: string | undefined;
	$: qnode = $networks.qnodes.find((q) => q.id === qnodeId);
	$: if (currentQNodeId != qnodeId) {
		currentQNodeId = qnodeId;
	}
</script>

{#if qnode}
	<div>
		{qnodeId}
		<h1>{qnode?.name}</h1>
		<Ping containerId={qnodeId} />
	</div>
{/if}
