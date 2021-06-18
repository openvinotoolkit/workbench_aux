import { commandDefaults } from '../constants';
import { Devices } from './command-constructor-form';

interface ICommandParameter {
  name: string;
  value?: string;
}

export class CommandParameter implements ICommandParameter {
  name: string;
  value?: string;

  constructor(name: string, value?: string) {
    this.name = name;
    this.value = value;
  }

  toString(): string {
    if (!this.value) {
      return this.name;
    }
    return `${this.name} ${this.value}`;
  }
}

export class EnvVarCommandParameter extends CommandParameter {
  envVarName: string;

  constructor(name: string, envVarName: string, value: string) {
    super(name, value);
    this.envVarName = envVarName;
  }

  toString(): string {
    return `${this.name} ${this.envVarName}=${this.value}`;
  }
}

interface ICommandParametersBuilder {
  parameters: CommandParameter[];
  addDevicesParameters(devices: Devices[]): void;
  addProxyParameters(httpProxy: string, httpsProxy: string, noProxy: string): void;
}

export class PythonCommandParametersBuilder implements ICommandParametersBuilder {
  private readonly _parameters: CommandParameter[];

  get parameters(): CommandParameter[] {
    return this._parameters;
  }

  constructor() {
    this._parameters = [
      new CommandParameter('--image', commandDefaults.dockerImageWithTag),
    ];
  }

  addDevicesParameters(devices: Devices[]): void {
    if (devices.includes(Devices.GPU)) {
      this._parameters.push(new CommandParameter('--gpu'));
    }
    if (devices.includes(Devices.NCS2)) {
      this._parameters.push(new CommandParameter('--myriad'));
    }
    if (devices.includes(Devices.HDDL)) {
      this._parameters.push(new CommandParameter('--hddl'));
    }
  }

  addProxyParameters(httpProxy: string, httpsProxy: string, noProxy: string): void {
    if (httpProxy) {
      this._parameters.push(new CommandParameter('--http-proxy', httpProxy));
    }
    if (httpsProxy) {
      this._parameters.push(new CommandParameter('--https-proxy', httpsProxy));
    }
    if (noProxy) {
      this._parameters.push(new CommandParameter('--no-proxy', noProxy));
    }
  }
}

export class DockerCommandParametersBuilder implements ICommandParametersBuilder {
  private readonly _parameters: CommandParameter[];
  private readonly _itParameter: CommandParameter;

  get parameters(): CommandParameter[] {
    return [...this._parameters, this._itParameter];
  }

  constructor() {
    const { dockerImageWithTag, bindIP, hostPort, containerPort, containerName } = commandDefaults;
    this._parameters = [
      new CommandParameter('-p', `${bindIP}:${hostPort}:${containerPort}`),
      new CommandParameter('--name', containerName),
    ];
    this._itParameter = new CommandParameter('-it', dockerImageWithTag);
  }

  addDevicesParameters(devices: Devices[]): void {
    if (devices.includes(Devices.GPU)) {
      // Example:
      // --device /dev/dri
      // --group-add=$(stat -c '%g' /dev/dri/render* | head -1)
      this._parameters.push(new CommandParameter('--device', '/dev/dri'));
      this._parameters.push(new CommandParameter('--group-add', '$(stat -c \'%g\' /dev/dri/render* | head -1)'));
    }
    if (devices.includes(Devices.NCS2)) {
      // Example:
      // --device-cgroup-rule='c 189:* rmw'
      // -v /dev/bus/usb:/dev/bus/usb
      this._parameters.push(new CommandParameter('--device-cgroup-rule', '\'c 189:* rmw\''));
      this._parameters.push(new CommandParameter('-v', '/dev/bus/usb:/dev/bus/usb'));
    }
    if (devices.includes(Devices.HDDL)) {
      // Example:
      // --device=/dev/ion:/dev/ion
      // -v /var/tmp:/var/tmp
      this._parameters.push(new CommandParameter('--device', '/dev/ion:/dev/ion'));
      this._parameters.push(new CommandParameter('-v', '/var/tmp:/var/tmp'));
    }
  }

  addProxyParameters(httpProxy: string, httpsProxy: string, noProxy: string): void {
    if (httpProxy) {
      this._parameters.push(new EnvVarCommandParameter('-e', 'HTTP_PROXY', httpProxy));
    }
    if (httpsProxy) {
      this._parameters.push(new EnvVarCommandParameter('-e', 'HTTPS_PROXY', httpsProxy));
    }
    if (noProxy) {
      this._parameters.push(new EnvVarCommandParameter('-e', 'NO_PROXY', noProxy));
    }
  }
}
