<script lang="ts">
	import { containers } from '../stores/containers';
	export let qnodeId: string | undefined;
	let currentQNodeId: string | undefined;
	$: qnode = $containers.find((c) => c.id === qnodeId);
	$: if (currentQNodeId != qnodeId) {
		currentQNodeId = qnodeId;
	}
</script>

{#if qnode}
	<div>
		{qnodeId}
		<h1>{qnode?.name}</h1>
	</div>
{/if}
