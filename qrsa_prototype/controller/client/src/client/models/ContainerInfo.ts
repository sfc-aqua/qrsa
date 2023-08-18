/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ContainerStatus } from './ContainerStatus';
import type { PortInfo } from './PortInfo';
import type { ProcessesInfo } from './ProcessesInfo';

export type ContainerInfo = {
    id: string;
    name: string;
    status: ContainerStatus;
    attrs: any;
    ports: Record<string, Array<PortInfo>>;
    top: ProcessesInfo;
};

