<script lang="ts">
	import type { ContainerInfo } from "../client";
    import {logs} from "../stores/network"
	import LogLine from "./LogLine.svelte";
    export let qnodeId: string;

</script>

<section class="log-container">
    {#if qnodeId in $logs}
    {@const logText = $logs[qnodeId]}
        {#each logText as log}
            {#each log.split("\n") as line}
            <LogLine log={line} />
            {/each}
        {/each}
    {/if}
</section>


<style>
    .log-container {
        flex: 1;
        overflow-y: scroll;
    }
</style>