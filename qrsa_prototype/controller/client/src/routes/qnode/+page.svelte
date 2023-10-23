<script lang="ts">
	import type { PageData } from './$types';
	import { networks, clearLog } from '../../stores/network';
	import type { ContainerInfo } from '../../client';
	import API from '$lib/api';
	import Log from '../Log.svelte';

	export let data: PageData;
	let container: ContainerInfo | undefined;
	$: container = $networks.qnodes.find((c) => c.id === data.qnodeId)?.container || undefined;
</script>

<section>
	{#if data.qnodeId == null}
		<h1>specify qnode</h1>
	{:else}
		<h1>Container: {container?.name} : {container?.id}</h1>
		<button on:click={() => API.clearLogRetrievedAt(data.qnodeId ?? '')}>get all log</button>
		<button on:click={() => clearLog(data.qnodeId ?? '')}>clear</button>
		<Log qnodeId={data.qnodeId} />
	{/if}
</section>
