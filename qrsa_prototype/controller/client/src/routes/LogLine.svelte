<script lang="ts">
    export let log: string;
    let json: {[key: string]: any} | undefined = undefined;

    $: try {
        json = JSON.parse(log)
    } catch (e) {}
</script>
{#if json != null}
    <span class="json-log">{json.message}</span>
{:else}
    <span class="default">{log}</span>
{/if}
<br/>

<style>
    .json-log {
        font-weight: 800;
    }
    
</style>