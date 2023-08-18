<script lang="ts">
	import { containers } from '../../stores/containers';
	import ContainerTable from '../ContainerTable.svelte';
</script>

<section>
	<h1>Docker Containers</h1>
    <ContainerTable containers={$containers}/>
</section>
