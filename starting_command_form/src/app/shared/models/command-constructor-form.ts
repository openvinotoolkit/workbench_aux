import { BehaviorSubject } from 'rxjs';

export interface IFieldOption {
  label: string;
  value: boolean | string;
  tooltip?: string;
}

export enum FieldTypes {
  RADIO = 'radio',
  CHECKBOX = 'checkbox',
  OPTIONAL_TEXT = 'optionalText',
}

export type FieldValueType = boolean | string | string[] | null;

export interface ICommandConstructorField {
  name: string;
  type: FieldTypes;
  label: string;
  value: FieldValueType;
  helpMessage?: string;
  placeholder?: string;
  options?: IFieldOption[];
  disabledOptions?: BehaviorSubject<string[]>;
}

export enum FormControlNames {
  DOCKER_INSTALLED = 'dockerInstalled',
  OS = 'os',
  DEVICES = 'devices',
  START_WITH = 'startWith',
  HTTP_PROXY = 'httpProxy',
  HTTPS_PROXY = 'httpsProxy',
  NO_PROXY = 'noProxy',
}

export enum OperatingSystems {
  LINUX = 'linux',
  WINDOWS = 'windows',
  MAC_OS = 'macos',
}

export enum Devices {
  CPU = 'CPU',
  GPU = 'GPU',
  NCS2 = 'NCS2',
  HDDL = 'HDDL',
}

export enum StartTypes {
  PYTHON = 'python',
  DOCKER = 'docker',
}

export interface ICommandConfig {
  dockerInstalled: boolean;
  os: OperatingSystems;
  devices: Devices[];
  startWith: StartTypes;
  httpProxy: string;
  httpsProxy: string;
  noProxy: string;
}
