<script lang="ts">
	import { networks } from '../stores/network';
	import Log from './Log.svelte';
</script>

<div class="container">
	{#each $networks.qnodes as qnode}
		<div class="log-content">
			<h3>{qnode.name}</h3>
			<Log qnodeId={qnode.id} />
		</div>
	{/each}
</div>

<style>
	.container {
		display: flex;
		height: 30vh;
		width: 100%;
	}
	.log-content {
		flex-grow: 1;
	}
</style>
