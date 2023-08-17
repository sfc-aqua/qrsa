import { readable } from "svelte/store";
import type { ContainerInfo } from "../client";
import API from "$lib/api";

export const containers = readable<ContainerInfo[]>([], (set) => {
    const id = setInterval(() => API.fetchContainerList().then(set), 3000);
    return () => clearInterval(id);
})