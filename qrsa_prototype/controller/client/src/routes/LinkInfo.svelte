<script lang="ts">
	import { networks } from '../stores/network';
	export let linkId: string | undefined;
	let currentLinkId: string | undefined;
	$: link = $networks.links.find((l) => l.id === linkId);
	$: if (currentLinkId != linkId) {
		currentLinkId = linkId;
	}
</script>

{#if link}
	<div>
		{linkId}
		<h1>{link?.id}</h1>
		<!-- <div><button>disconnect</button></div> -->
	</div>
{/if}
