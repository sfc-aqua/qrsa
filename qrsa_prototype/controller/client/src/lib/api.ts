import type { AxiosProgressEvent } from 'axios';
import { CancelablePromise, DefaultService, OpenAPI } from '../client';
import { request } from '../client/core/request';
OpenAPI.BASE = 'http://localhost:9000/api';
const startContaienr = DefaultService.startContainerContainersIdStartPost;
const stopContainer = DefaultService.stopContainerContainersIdStopPost;
const getDiskDiff = DefaultService.diffContainerContainersIdDiffGet;
const getLogs = DefaultService.logContainerContainersIdLogsGet;
const clearLogRetrievedAt = DefaultService.clearLogRetrievalAtContainersIdClearLogRetrievalAtGet;
const execRun = DefaultService.execRunContainerContainersIdExecRunPost;
const fetchNetworkStatus = () => DefaultService.getNetworkNetworkGet();
const startConnectionSetup = DefaultService.startConnectionSetupContainerIdStartConnectionSetupPost;

/**
 * Exec Run Container Stream
 * @param id
 * @param cmd
 * @returns any Successful Response
 * @throws ApiError
 */
function execRunStream(
	id: string,
	cmd: string,
	onProgress?: (e: AxiosProgressEvent) => void
): CancelablePromise<any> {
	return request(OpenAPI, {
		method: 'POST',
		url: '/containers/{id}/exec_run_stream',
		path: {
			id: id
		},
		query: {
			cmd: cmd
		},
		errors: {
			422: `Validation Error`
		},
		onDownloadProgress: onProgress,
		responseType: 'stream'
	});
}

const ping = (containerId: string, target: string, onProgress: any) => {
	const handleProgressEvent = (e: AxiosProgressEvent) => {
		onProgress(e.event.target.response.slice(e.loaded - e.bytes));
	};
	return execRunStream(containerId, `ping ${target}`, handleProgressEvent);
};

type WSEventListeners = {
	log: Array<(event: { qnodeId: string; type: 'log'; data: string }) => void>;
	network: Array<(event: any) => void>;
	qnode_status: Array<(event: any) => void>;
};
type WSEventType = keyof WSEventListeners;

class WSConn {
	ws: WebSocket | undefined;
	url: string;
	eventListeners: WSEventListeners;
	constructor(url = 'ws://localhost:9000/api/ws') {
		this.url = url;
		this.eventListeners = {
			log: [],
			network: [],
			qnode_status: []
		};
		this.connect();
	}
	connect() {
		this.ws = new WebSocket(this.url);
		console.log('connecting...');
		this.ws.onmessage = this.handleMessage.bind(this);
		this.ws.onerror = console.warn;
		this.ws.onopen = () => console.log('connected');
		this.ws.onclose = this.handleClose.bind(this);
	}
	handleClose(event: CloseEvent) {
		console.warn('closed: ', event.reason);
		console.log('reconnect...');
		setTimeout(() => {
			this.connect();
		}, 1000);
	}
	handleMessage(e: MessageEvent) {
		try {
			const value = JSON.parse(e.data);
			const type = value.type;
			if (type in this.eventListeners) {
				const listeners = this.eventListeners[type as WSEventType];
				for (const f of listeners) {
					f(value);
				}
			}
		} catch (e) {}
	}
	subscribe(type: WSEventType, fn: (event: any) => void) {
		this.eventListeners[type].push(fn);
	}
	unsubscribe(type: WSEventType, fn: (event: any) => void) {
		this.eventListeners[type] = this.eventListeners[type].filter((f) => f != fn);
	}
}

const ws = new WSConn();

const API = {
	startContaienr,
	stopContainer,
	getDiskDiff,
	getLogs,
	execRun,
	execRunStream,
	ping,
	fetchNetworkStatus,
	clearLogRetrievedAt,
	startConnectionSetup,
	ws
};
export default API;
