<script lang="ts">
	import QNodeTable from './QNodeTable.svelte';
	import NetworkGraph from './NetworkGraph.svelte';
	import LogMonitor from './LogMonitor.svelte';
</script>

<section>
	<div class="top-container">
		<NetworkGraph />
		<QNodeTable />
	</div>
	<LogMonitor />
</section>

<style>
	.top-container {
		display: flex;
	}
</style>
