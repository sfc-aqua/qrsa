<script lang="ts">
    import API from "$lib/api"
    import {containers} from "../stores/containers"
    export let containerId: string | undefined = undefined;
    let output;
    const ping = (name: string) => {
        console.log(containerId, name)
        if (!containerId) return;
        console.log(API.execRunStream(containerId, `ping ${name}`))
    } 

</script>

<h1>ping</h1>
{containerId}
<h2>target</h2>
{#each $containers as container}
    <div>{container.id}: {container.name} <button on:click={() => ping(container.name)}>ping</button></div>
{/each}
