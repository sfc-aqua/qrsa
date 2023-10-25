<script lang="ts">
	import { networks, qnodeStatuses } from '../stores/network';
	export let qnodeId: string | undefined;
	let currentQNodeId: string | undefined;
	$: qnode = $networks.qnodes.find((q) => q.id === qnodeId);
	$: if (currentQNodeId != qnodeId) {
		currentQNodeId = qnodeId;
	}
</script>

{#if qnode}
	<div>
		<h1>{qnode?.name}@{qnode?.id}</h1>
		<table>
			<thead>
				<tr>
					<th>id</th>
					<th />
				</tr>
			</thead>
			<tbody>
				{#if qnode.id in $qnodeStatuses}
					{@const status = $qnodeStatuses[qnode.id]}
					<tr>
						<th colspan="2">LA Switch Timings</th>
					</tr>
					{#each Object.entries(status.linkAllocationSwitchTimings) as value}
						{@const [key, conn] = value}
						<tr>
							<td colspan="1">
								{key.substring(0, 6)}
							</td>
							<td colspan="7">
								{JSON.stringify(conn)}
							</td>
						</tr>
					{/each}
					<tr>
						<hr />
					</tr>
					<tr>
						<th colspan="2">Current PPTSN </th>
					</tr>
					{#each Object.entries(status.currentPPTSN) as value}
						{@const [key, conn] = value}
						<tr>
							<td colspan="1">
								{key.substring(0, 6)}
							</td>
							<td colspan="7">
								{JSON.stringify(conn)}
							</td>
						</tr>
					{/each}
					<tr>
						<hr />
					</tr>
					<tr>
						<th colspan="2">Running Connections</th>
					</tr>
					{#each Object.entries(status.runningConnections) as value}
						{@const [key, conn] = value}
						<tr>
							<td colspan="1">
								{key.substring(0, 6)}
							</td>
							<td colspan="7">
								{JSON.stringify(conn)}
							</td>
						</tr>
					{/each}
					<tr>
						<hr />
					</tr>
					<tr>
						<th colspan="2">Pending Connections</th>
					</tr>
					{#each Object.entries(status.pendingConnections) as value}
						{@const [key, conn] = value}
						<tr>
							<td colspan="1">
								{key.substring(0, 6)}
							</td>
							<td colspan="7">
								{JSON.stringify(conn)}
							</td>
						</tr>
					{/each}
					<tr>
						<hr />
					</tr>
					<tr>
						<th colspan="2">Running Runtime</th>
					</tr>
					{#each Object.entries(status.runningRuntime) as value}
						{@const [key, conn] = value}
						<tr>
							<td colspan="1">
								{key.substring(0, 6)}
							</td>
							<td colspan="7">
								{JSON.stringify(conn)}
							</td>
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</div>
{/if}
