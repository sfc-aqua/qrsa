import { readable } from 'svelte/store';
import type { NetworkData } from '../client';
import API from '$lib/api';

export const networks = readable<NetworkData>({ qnodes: [], links: [] }, (set) => {
	API.fetchNetworkStatus().then(set);
	const id = setInterval(() => API.fetchNetworkStatus().then(set), 3000);
	return () => clearInterval(id);
});
