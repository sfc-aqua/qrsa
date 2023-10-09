import { readable, writable } from 'svelte/store';
import type { NetworkData } from '../client';
import API from '$lib/api';

export const networks = readable<NetworkData>({ qnodes: [], links: [] }, (set) => {
	API.fetchNetworkStatus().then(set);
	const id = setInterval(() => API.fetchNetworkStatus().then(set), 3000);
	return () => clearInterval(id);
});

const logRetrievalTimers: number[] = [];
const createLogRetrievalTimer = (id: string, update) => {
	return setInterval(
		() =>
			API.getLogs(id).then(({ logs }) => {
				if (!logs) return;
				update((values) => {
					return { ...values, [id]: [...values[id], logs] };
				});
			}),
		700
	);
};

export const logs = writable<{ [key: string]: string[] }>({}, (set, update) => {
	networks.subscribe(({ qnodes }) => {
		const ids = qnodes.map(({ id }) => id);
		update((values) => {
			for (const id of ids) {
				if (id in values) continue;
				values[id] = [];
				logRetrievalTimers.push(createLogRetrievalTimer(id, update));
			}
			return values;
		});
	});
	return () => {
		logRetrievalTimers.forEach((id) => clearInterval(id));
	};
});

export const clearLog = (id: string) => {
	logs.update((values) => {
		values[id] = [];
		return values;
	});
};
