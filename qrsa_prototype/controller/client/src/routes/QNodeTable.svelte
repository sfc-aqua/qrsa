<script lang="ts">
	import type { PortInfo } from '../client';
	import API from '$lib/api';
	import { clearLog, networks } from '../stores/network';

	const convertPortInfo = (ports: Record<string, PortInfo[]> | undefined): string => {
		if (!ports) return '';
		return Object.entries(ports).reduce(
			(acc, [port, info]) =>
				acc + (acc.length > 0 ? ', ' : '') + `${port} -> [${info[0].HostIp}:${info[0].HostPort}]`,
			''
		);
	};

	const startConnectionSetup = (initiatorQNodeId: string, responderQNodeId: string) => {
		$networks.qnodes.forEach(({ id }) => clearLog(id));
		API.startConnectionSetup(initiatorQNodeId, responderQNodeId, 0, 1).catch((e) =>
			console.error(e)
		);
	};
</script>

<table>
	<thead>
		<tr>
			<th>ID</th>
			<th>Name</th>
			<th>IP</th>
			<th>Status</th>
			<th>Port</th>
			<th>Action</th>
			<th />
			<th>Start Conn to</th>
		</tr>
	</thead>
	<tbody>
		{#each $networks.qnodes as qnode}
			{@const c = qnode.container}
			<tr>
				<td>{qnode.id}</td>
				<td class="name">{c?.name}</td>
				<td>{c?.attrs['NetworkSettings']['Networks']['qrsa_qrsa_net']['IPAddress']}</td>
				<td>{c?.status}</td>
				<td>{convertPortInfo(c?.ports)}</td>
				{#if c?.status == 'exited'}
					<td><button on:click={() => API.startContaienr(c.id)}>start</button></td>
				{:else}
					<td><button on:click={() => API.stopContainer(c?.id)}>stop</button></td>
				{/if}
				<td>
					<a href={`/qnode/${qnode.id}`}>show</a>
				</td>
				<td>
					{#each $networks.qnodes as targetNode}
						{#if targetNode.id != qnode.id}
							<button on:click={() => startConnectionSetup(qnode.id, targetNode.id)}
								>{targetNode.name}</button
							>
						{/if}
					{/each}
				</td>
			</tr>
		{/each}
	</tbody>
</table>

<style>
	.name {
		font-weight: 900;
	}
</style>
