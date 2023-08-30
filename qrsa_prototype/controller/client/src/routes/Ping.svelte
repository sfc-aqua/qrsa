<script lang="ts">
	import API from '$lib/api';
	import { onDestroy } from 'svelte';
	import type { CancelablePromise } from '../client';
	import { containers } from '../stores/containers';

	export let containerId: string | undefined = undefined;
	let pingStates: {
		[key: string]: { cancellable: CancelablePromise<any> | null; result: string };
	} = {};
	const ping = (target: string) => {
		if (!containerId) return;
        const key = containerId + target;
		pingStates[key] = { cancellable: null, result: '' };
		const cancellable = API.ping(containerId, target, (result: string) => {
			const lines = result.split('\n').filter(Boolean);
			const line: string = lines[lines.length - 1];
			if (line.includes(':')) {
				pingStates[key]['result'] = line.split(':')[1];
			}
		});
        pingStates[key].cancellable = cancellable;
	};
	const cancel = (key: string) => {
        console.log(containerId, key, "destroy")
		pingStates[key].cancellable?.cancel();
		pingStates[key].cancellable = null;
	};
	onDestroy(() => {
		Object.keys(pingStates).forEach((key) => {
			pingStates[key].cancellable?.cancel();
		});
	});
</script>

<h1>ping</h1>
{containerId}
<h2>target</h2>
{#each $containers as container}
	{#if container.id !== containerId}
		{@const key = containerId + container.name}
		<div>
			{container.name}
			{#if key in pingStates && pingStates[key].cancellable}
				<button on:click={() => cancel(key)}>stop</button>
				{pingStates[key].result}
			{:else}
				<button on:click={() => ping(container.name)}>ping</button>
			{/if}
		</div>
	{/if}
{/each}

<style>
	span {
		white-space: pre-wrap;
	}
</style>
