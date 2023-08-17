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
     * Read Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static readRootHelloGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/hello',
        });
    }

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
    public static startContainerContainersStartIdPost(
        id: any,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/containers/start/{id}',
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
    public static stopContainerContainersStopIdPost(
        id: any,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/containers/stop/{id}',
            path: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
