import { readable, writable } from 'svelte/store';
import type { ContainerInfo } from '../client';
import API from '$lib/api';

export const containers = readable<ContainerInfo[]>([], (set) => {
	const sortAndSet = (cs: ContainerInfo[]) =>
		set(cs.sort((c1, c2) => (c1.name > c2.name ? 1 : -1)));
	API.fetchContainerList().then(sortAndSet);
	const id = setInterval(() => API.fetchContainerList().then(sortAndSet), 3000);
	return () => clearInterval(id);
});

type LinkInfo = {
	id: string;
	qnodeIds: Set<string>;
	name: string;
};

export const links = writable<LinkInfo[]>([]);
const getLinkId = (id1: string, id2: string): string =>
	id1 > id2 ? `${id1}-${id2}` : `${id2}-${id1}`;
containers.subscribe((cs) => {
	links.update((ls) => {
		const newLinks = [...ls];
		for (let i = 0; i < cs.length; i++) {
			const c1 = cs[i];
			for (let j = i + 1; j < cs.length; j++) {
				const c2 = cs[j];
				const id = getLinkId(c1.id, c2.id);
				const index = ls.findIndex((l) => l.id === id);
				if (index !== -1) {
					newLinks[i] = { ...newLinks[i], }
				} else {
					newLinks.push({ id, qnodeIds: new Set([c1.id, c2.id]), name: `${c1.name}-${c2.name}` });
				}
			}
		}
		return newLinks;
	});
});
