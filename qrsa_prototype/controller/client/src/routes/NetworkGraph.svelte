<script lang="ts">
	import cytoscape from 'cytoscape';
	import { onMount } from 'svelte';
	import type { ContainerInfo } from '../client';
	import QNodeInfo from './QNodeInfo.svelte';
	import { links } from '../stores/containers';
	import LinkInfo from './LinkInfo.svelte';
	export let containers: ContainerInfo[] = [];
	let cy: cytoscape.Core | undefined;
	let selectedQNodeId: string | undefined;
	let selectedLinkId: string | undefined;
	const CYTOSCAPE_DEFAULT_OPTIONS = {
		style: [
			{
				selector: 'node',
				style: {
					'background-color': '#666',
					label: 'data(name)'
				}
			},
			{
				selector: 'edge',
				style: {
					width: 3,
					'line-color': '#ccc',
					'target-arrow-color': '#ccc',
					'target-arrow-shape': 'none',
					'curve-style': 'bezier'
				}
			},
			{
				selector: ':selected',
				style: {
					'background-color': 'red',
					'line-color': 'orange'
				}
			},
			{
				selector: '.exit',
				style: {}
			}
		]
	};

	const LAYOUT_OPTION = {
		name: 'circle',
		animate: true,
		padding: 30,
		avoidOverlap: true,
		avoidOverlapPadding: 10
	};

	onMount(() => {
		cy = cytoscape({
			container: document.getElementById('network-graph'),
			elements: [],
			...CYTOSCAPE_DEFAULT_OPTIONS
		});
		cy.on('unselect', ({ target }) => {
			const id = target.data().id;
			if (id === selectedLinkId) selectedLinkId = undefined;
			if (id === selectedQNodeId) selectedQNodeId = undefined;
		});
	});

	$: if (cy !== undefined) {
		const layout = cy.layout(LAYOUT_OPTION);
		cy.startBatch();
		for (let i = 0; i < containers.length; i++) {
			const c = containers[i];
			if (c.name.includes('controller')) continue;
			const e = cy.getElementById(c.id);
			if (e.length > 0) continue;
			const elem = cy?.add({ data: { id: c.id, name: c.name } });
			elem.on('select', ({ target }) => {
				selectedLinkId = undefined;
				selectedQNodeId = target.data().id;
			});
		}
		for (let i = 0; i < $links.length; i++) {
			const l = $links[i];
			const id = l.id;
			const [qnodeId1, qnodeId2] = l.qnodeIds.values();
			const edge = cy.getElementById(id);
			if (edge.length > 0) continue;
			if (cy.getElementById(qnodeId1).length === 0 || cy.getElementById(qnodeId2).length === 0)
				continue;
			const elem = cy.add({ data: { id, source: qnodeId1, target: qnodeId2 } });
			elem.on('select', ({ target }) => {
				selectedQNodeId = undefined;
				selectedLinkId = target.data().id;
			});
		}
		cy.endBatch();
		layout.run();
	}
</script>

<div class="container">
	<div id="network-graph" />
	<QNodeInfo qnodeId={selectedQNodeId} />
	<LinkInfo linkId={selectedLinkId} />
</div>

<style>
	#network-graph {
		height: 500px;
		border: solid 1px red;
		min-width: 30vw;
	}
	.container {
		display: flex;
	}
</style>