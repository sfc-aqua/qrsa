<script lang="ts">
	import { logs } from '../stores/network';
	import LogLine from './LogLine.svelte';
	export let qnodeId: string;
	let prettyLog = true;
	const parseLog = (log: string): Array<string | string[]> => {
		const logs = log.split('\n');
		if (!prettyLog) return logs;
		let readingTraceback = false;
		let buf = [];
		const results = [];
		for (let i = 0; i < logs.length; i++) {
			const line = logs[i];
			const firstCol = line.split(':')[0];
			if (['INFO', 'WARN', 'ERROR', 'Exception'].indexOf(firstCol) != -1) {
				results.push(line);
				continue;
			}
			if (line.length > 0 && line[0] == '{') {
				results.push(line);
				continue;
			}
			if (line.startsWith('Traceback')) {
				if (buf.length > 0) {
					results.push(buf);
					buf = [];
				}
				readingTraceback = true;
			}
			if (readingTraceback) {
				buf.push(line);
				if (line.length == 0) {
					results.push(buf);
					buf = [];
					readingTraceback = false;
				}
			} else {
				results.push(line);
			}
		}
		return results;
	};
</script>

<section class="log-container">
	{#if prettyLog}
		<button on:click={() => (prettyLog = false)}>switch to raw log</button>
	{:else}
		<button on:click={() => (prettyLog = true)}>switch to pretty log (experimental)</button>
	{/if}
	{#if qnodeId in $logs}
		{@const logText = $logs[qnodeId]}
		{#each logText as log}
			{#each parseLog(log) as line}
				<LogLine log={line} pretty={prettyLog} />
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
