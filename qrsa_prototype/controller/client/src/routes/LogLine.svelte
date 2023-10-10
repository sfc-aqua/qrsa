<script lang="ts">
	import Highlight from 'svelte-highlight';
	import python from 'svelte-highlight/languages/python';
	import 'svelte-highlight/styles/github.css';

	export let log: string | string[];
	export let pretty: boolean;
	let json: { [key: string]: any } | undefined = undefined;
	let color = '';
	let traceback: string[] = [];
	let tracebackVisible = false;
	if (Array.isArray(log)) {
		traceback = log;
	} else {
		const firstCol = log.split(' ')[0];
		const SEVERITY_DICT = {
			'INFO:': 'info',
			'WARN:': 'warn',
			'ERROR:': 'error',
			'Exception:': 'exception'
		} as const;

		if (firstCol in SEVERITY_DICT) {
			color = SEVERITY_DICT[firstCol as keyof typeof SEVERITY_DICT];
		}

		if (pretty) {
			try {
				json = JSON.parse(log);
			} catch {} // eslint-disable-line
		}
	}
</script>

{#if json != null}
	<span class="json-log-header {json.level}">{json.level}</span>|
	<span class="json-log">{json.message}</span>
{:else if traceback.length > 0}
	<span>{traceback[traceback.length - 2]}</span>
	{#if tracebackVisible}
		<div class="traceback-dialog">
			<Highlight language={python} code={traceback.join('\n')} />
			<button
				on:click={() => {
					tracebackVisible = false;
				}}>close</button
			>
		</div>
	{:else}
		<button
			on:click={() => {
				tracebackVisible = true;
			}}>see traceback</button
		>
	{/if}
{:else}
	<span class="default {color}">{log}</span>
{/if}
<br />

<style>
	.json-log-header {
		width: 5rem;
		display: inline-block;
	}
	.json-log {
		font-weight: 800;
	}
	.info {
		font-weight: 400;
		color: darkgreen;
	}
	.warn {
		font-weight: 800;
		color: yellow;
	}
	.error,
	.exception {
		font-weight: 800;
		color: red;
	}
	.traceback-dialog {
		position: fixed;
		background-color: black;
		color: white;
		font-family: 'Courier New', Courier, monospace;
		white-space: pre-wrap;
		left: 10vw;
		width: 80vw;
		top: 5vh;
		height: 90vh;
		overflow-y: scroll;
		padding: 1rem;
	}
</style>
