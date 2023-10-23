import { readable, writable } from 'svelte/store';
import type { NetworkData } from '../client';
import API from '$lib/api';

export const networks = readable<NetworkData>({ qnodes: [], links: [] }, (set) => {
	API.fetchNetworkStatus().then(set);
	API.ws.subscribe('network', set);
	return () => API.ws.unsubscribe('network', set);
});

export const logs = writable<{ [key: string]: string[] }>({}, (set, update) => {
	const f = (event: { data: string; qnode_id: string }) => {
		const { qnode_id: qnodeId, data } = event;
		update((values) => {
			if (!(qnodeId in values)) {
				values[qnodeId] = [];
			}
			values[qnodeId].push(data);
			return values;
		});
	};

	API.ws.subscribe('log', f);
	return () => API.ws.unsubscribe('log', f);
});

export const clearLog = (id: string) => {
	logs.update((values) => {
		values[id] = [];
		return values;
	});
};
