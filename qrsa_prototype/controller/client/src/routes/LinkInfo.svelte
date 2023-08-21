<script lang="ts">
	import { containers, links } from '../stores/containers';
	export let linkId: string | undefined;
	let currentLinkId: string | undefined;
	$: link = $links.find((l) => l.id === linkId);
	$: if (currentLinkId != linkId) {
		currentLinkId = linkId;
	}
</script>

{#if link}
	<div>
		{linkId}
		<h1>{link?.id}</h1>
	</div>
{/if}
