<script lang="ts">
    import {networks} from "../stores/network"
	import Log from "./Log.svelte";

</script>

<div class="container">
{#each $networks.qnodes as qnode}
    <Log qnodeId={qnode.id} />
{/each}
</div>

<style>
.container {
    display:flex;
    height:30vh;
}
</style>