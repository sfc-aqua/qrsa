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

type IpAddressStr = string;
type RuleSetId = string;
type QNodeStatusData = {
	qnode_id: string;
	pending_connections: { [key: string]: Connection };
	application_id_to_connection_id: { [key: string]: any };
	running_connections: { [key: string]: Connection };
	running_runtime: { [key: string]: Runtime };
	sent_la: { [key: string]: any };
	current_pptsn: { [key: string]: any };
	la_switch_timings: { [key: string]: { [key: IpAddressStr]: number } };
	available_link_resource: { [key: string]: any };
	type: 'qnode_status';
};

type Connection = {
	prev_hop: IpAddressStr | null;
	next_hop: IpAddressStr | null;
	source: IpAddressStr;
	destination: IpAddressStr;
};
type Runtime = {
	ruleset: {
		ruleset_id: RuleSetId;
		stages: any[];
	};
	status: number;
};
type QNodeStatus = {
	pendingConnections: { [key: string]: Connection };
	runningConnections: { [key: string]: Connection };
	runningRuntime: { [key: string]: Runtime };
	sentLinkAllocation: { [key: string]: any };
	currentPPTSN: { [key: string]: any };
	linkAllocationSwitchTimings: { [key: string]: any };
	availableLinkResource: { [key: string]: any };
};

export const qnodeStatuses = readable<{ [key: string]: QNodeStatus }>({}, (set, update) => {
	const f = (event: QNodeStatusData) => {
		const {
			qnode_id: qnodeId,
			pending_connections: pendingConnections,
			running_connections: runningConnections,
			running_runtime: runningRuntime,
			sent_la: sentLinkAllocation,
			current_pptsn: currentPPTSN,
			la_switch_timings: linkAllocationSwitchTimings,
			available_link_resource: availableLinkResource
		} = event;
		update((values) => {
			values[qnodeId] = {
				pendingConnections,
				runningConnections,
				runningRuntime,
				sentLinkAllocation,
				currentPPTSN,
				linkAllocationSwitchTimings,
				availableLinkResource
			};
			return values;
		});
	};
	API.ws.subscribe('qnode_status', f);
	return () => API.ws.unsubscribe('qnode_status', f);
});
