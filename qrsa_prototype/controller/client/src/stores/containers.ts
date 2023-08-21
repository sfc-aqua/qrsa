import { readable, writable } from 'svelte/store';
import type { ContainerInfo } from '../client';
import API from '$lib/api';

export const containers = readable<ContainerInfo[]>([], (set) => {
    const sortAndSet = (cs: ContainerInfo[]) => set(cs.sort((c1, c2) => (c1.name > c2.name ? 1 : -1)));
    API.fetchContainerList().then(sortAndSet);
    const id = setInterval(
        () =>
            API.fetchContainerList().then(sortAndSet),
        3000
    );
    return () => clearInterval(id);
});

type LinkInfo = {
    id: string;
    qnodeIds: Set<string>;
}

export const links = writable<LinkInfo[]>([], )