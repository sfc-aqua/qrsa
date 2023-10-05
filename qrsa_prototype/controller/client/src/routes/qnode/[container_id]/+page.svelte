<script lang="ts">
	import type { PageData } from './$types';
	import { networks, logs, clearLog } from '../../../stores/network';
	import type { ContainerInfo } from '../../../client';
	import API from '$lib/api';
	import Log from '../../Log.svelte';

	export let data: PageData;
	let container: ContainerInfo | undefined;
	$: container = $networks.qnodes.find((c) => c.id === data.container_id)?.container || undefined;
</script>

<section>
	<h1>Container: {container?.name} : {container?.id}</h1>
	<button on:click={() => API.clearLogRetrievedAt(data.container_id)}>get all log</button>
	<button on:click={() => clearLog(data.container_id)}>clear</button>
	<Log qnodeId={data.container_id}/>
</section>

<style>
	.code {
		white-space: pre-wrap;
		font-family: 'Courier New', Courier, monospace;
	}
</style>
