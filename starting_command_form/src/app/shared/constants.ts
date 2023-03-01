import {
  Devices,
  FieldTypes,
  FormControlNames,
  ICommandConstructorField,
  IFieldOption,
  OperatingSystems, StartTypes
} from './models/command-constructor-form';
import { BehaviorSubject } from 'rxjs';
import { MessagesService } from './services/messages.service';

const { optionLabels, fieldLabels } = MessagesService.messages;

export const booleanOptions: IFieldOption[] = [
  { label: optionLabels.boolean.yes, value: true },
  { label: optionLabels.boolean.no, value: false },
];

const osOptions: IFieldOption[] = [
  { label: optionLabels.os.linux, value: OperatingSystems.LINUX },
  { label: optionLabels.os.windows, value: OperatingSystems.WINDOWS },
  { label: optionLabels.os.macOS, value: OperatingSystems.MAC_OS },
];

const devicesOptions: IFieldOption[] = [
  { label: optionLabels.devices.CPU, value: Devices.CPU },
  { label: optionLabels.devices.GPU, value: Devices.GPU },
  { label: optionLabels.devices.NCS2, value: Devices.NCS2 },
  { label: optionLabels.devices.HDDL, value: Devices.HDDL, tooltip: optionLabels.devices.HDDLTooltip },
];

const startOptions: IFieldOption[] = [
  { label: optionLabels.startWith.python, value: StartTypes.PYTHON },
  { label: optionLabels.startWith.docker, value: StartTypes.DOCKER },
];

export const commandConstructorFormFieldsMap: { [key: string]: ICommandConstructorField } = {
  [FormControlNames.DOCKER_INSTALLED]: {
    name: FormControlNames.DOCKER_INSTALLED,
    type: FieldTypes.RADIO,
    label: fieldLabels.dockerInstalled,
    value: true,
    options: booleanOptions,
  },
  [FormControlNames.OS]: {
    name: FormControlNames.OS,
    type: FieldTypes.RADIO,
    label: fieldLabels.os,
    value: OperatingSystems.LINUX,
    options: osOptions,
  },
  [FormControlNames.DEVICES]: {
    name: FormControlNames.DEVICES,
    type: FieldTypes.CHECKBOX,
    label: fieldLabels.devices,
    value: [Devices.CPU],
    options: devicesOptions,
    disabledOptions: new BehaviorSubject([Devices.CPU]),
  },
  [FormControlNames.START_WITH]: {
    name: FormControlNames.START_WITH,
    type: FieldTypes.RADIO,
    label: fieldLabels.startWith,
    value: StartTypes.PYTHON,
    options: startOptions,
  },
  [FormControlNames.HTTP_PROXY]: {
    name: FormControlNames.HTTP_PROXY,
    type: FieldTypes.OPTIONAL_TEXT,
    label: fieldLabels.httpProxy,
    value: '',
    placeholder: optionLabels.proxy.inputPlaceholder,
  },
  [FormControlNames.HTTPS_PROXY]: {
    name: FormControlNames.HTTPS_PROXY,
    type: FieldTypes.OPTIONAL_TEXT,
    label: fieldLabels.httpsProxy,
    value: '',
    placeholder: optionLabels.proxy.inputPlaceholder,
  },
  [FormControlNames.NO_PROXY]: {
    name: FormControlNames.NO_PROXY,
    type: FieldTypes.OPTIONAL_TEXT,
    label: fieldLabels.noProxy,
    value: '',
    placeholder: optionLabels.proxy.inputPlaceholder,
  },
};

export const commandDefaults = {
  pythonWrapperName: 'openvino-workbench',
  dockerRunCommand: 'docker run',
  dockerImageWithTag: 'openvino/workbench:2022.3.0',
  bindIP: '0.0.0.0',
  hostPort: '5665',
  containerPort: '5665',
  containerName: 'workbench',
};
