<script lang="ts">
	import type { ContainerInfo, PortInfo } from '../client';
	import API from '$lib/api';

	export let containers: ContainerInfo[];
	const convertPortInfo = (ports: Record<string, PortInfo[]>): string => {
		return Object.entries(ports).reduce(
			(acc, [port, info]) => acc + `${port} -> [${info[0].HostIp}:${info[0].HostPort}]`,
			''
		);
	};
</script>

<table>
	<thead>
		<tr>
			<th>ID</th>
			<th>Name</th>
			<th>Status</th>
			<th>Port</th>
			<th>Action</th>
		</tr>
	</thead>
	<tbody>
		{#each containers as c}
			<tr>
				<td>{c.id}</td>
				<td>{c.name}</td>
				<td>{c.status}</td>
				<td>{convertPortInfo(c.ports)}</td>
				{#if c.status == 'exited'}
					<td><button on:click={() => API.startContaienr(c.id)}>start</button></td>
				{:else}
					<td><button on:click={() => API.stopContainer(c.id)}>stop</button></td>
				{/if}
				<td>
					<a href={`/containers/${c.id}`}>show</a>
				</td>
			</tr>
		{/each}
	</tbody>
</table>
