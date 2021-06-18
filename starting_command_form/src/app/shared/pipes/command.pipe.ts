import { Pipe, PipeTransform } from '@angular/core';
import { ICommandConfig, StartTypes } from '../models/command-constructor-form';
import { commandDefaults } from '../constants';
import { DockerCommandParametersBuilder, PythonCommandParametersBuilder } from '../models/command-parameter';

@Pipe({
  name: 'command'
})
export class CommandPipe implements PipeTransform {
  private readonly commandExecutableMap = {
    [StartTypes.PYTHON]: commandDefaults.pythonWrapperName,
    [StartTypes.DOCKER]: commandDefaults.dockerRunCommand,
  };

  transform(commandConfig: ICommandConfig): string {
    const { startWith, devices, httpProxy, httpsProxy, noProxy } = commandConfig;
    const commandBuilder = startWith === StartTypes.DOCKER ? new DockerCommandParametersBuilder() : new PythonCommandParametersBuilder();
    commandBuilder.addDevicesParameters(devices);
    commandBuilder.addProxyParameters(httpProxy, httpsProxy, noProxy);
    const commandExecutable = this.commandExecutableMap[startWith];
    const parametersString = commandBuilder.parameters.map((parameter) => parameter.toString()).join(' ');
    return `${commandExecutable} ${parametersString}`;
  }

}
