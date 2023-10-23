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
	startConnectionSetup
};
export default API;
