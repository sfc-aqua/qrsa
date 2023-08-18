/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ContainerInfo } from '../models/ContainerInfo';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Docker Ps
     * @returns ContainerInfo Successful Response
     * @throws ApiError
     */
    public static dockerPsContainersGet(): CancelablePromise<Array<ContainerInfo>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/containers',
        });
    }

    /**
     * Start Container
     * @param id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static startContainerContainersIdStartPost(
        id: any,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/containers/{id}/start',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Stop Container
     * @param id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static stopContainerContainersIdStopPost(
        id: any,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/containers/{id}/stop',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Log Container
     * @param id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static logContainerContainersIdLogsGet(
        id: any,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/containers/{id}/logs',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Diff Container
     * @param id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static diffContainerContainersIdDiffGet(
        id: any,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/containers/{id}/diff',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Exec Run Container
     * @param id
     * @param cmd
     * @returns any Successful Response
     * @throws ApiError
     */
    public static execRunContainerContainersIdExecRunPost(
        id: string,
        cmd: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/containers/{id}/exec_run',
            path: {
                'id': id,
            },
            query: {
                'cmd': cmd,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
