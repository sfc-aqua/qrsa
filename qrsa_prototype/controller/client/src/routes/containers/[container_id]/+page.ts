import { dev } from '$app/environment';

export function load({ params }) {
    return {
        container_id: params.container_id
    }
}

export const prerender = true;
export const csr = true;
export const ssr = dev;