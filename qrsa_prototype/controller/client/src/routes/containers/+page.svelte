<script lang="ts">
	import { containers } from '../../stores/containers';
	import ContainerTable from '../ContainerTable.svelte';
	import NetworkGraph from '../NetworkGraph.svelte';
</script>

<section>
	<h1>Docker Containers</h1>
	<NetworkGraph containers={$containers} />
	<ContainerTable containers={$containers} />
</section>
