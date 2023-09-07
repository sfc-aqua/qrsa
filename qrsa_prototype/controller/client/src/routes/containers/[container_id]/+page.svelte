<script lang="ts">
	import type { PageData } from './$types';
	import { networks } from '../../../stores/network';
	import type { ContainerInfo } from '../../../client';

	export let data: PageData;
	let container: ContainerInfo | undefined;
	$: container = $networks.qnodes.find((c) => c.id === data.container_id)?.container || undefined;
</script>

<section>
	<h1>Container: {container?.name} : {container?.id}</h1>
	<div>{JSON.stringify(container?.top)}</div>
	<div class="code">{JSON.stringify(container?.attrs, undefined, 2)}</div>
</section>

<style>
	.code {
		white-space: pre-wrap;
		font-family: 'Courier New', Courier, monospace;
	}
</style>
