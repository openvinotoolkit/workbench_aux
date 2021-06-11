import { Pipe, PipeTransform } from '@angular/core';
import { ICommandConfig, OperatingSystems, StartTypes } from '../models/command-constructor-form';
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

  private readonly lineContinueSymbolMap = {
    [OperatingSystems.LINUX]: commandDefaults.unixLineContinuationSymbol,
    [OperatingSystems.MAC_OS]: commandDefaults.unixLineContinuationSymbol,
    [OperatingSystems.WINDOWS]: commandDefaults.windowsLineContinuationSymbol,
  };

  transform(commandConfig: ICommandConfig): string {
    const { startWith, os, devices, httpProxy, httpsProxy, noProxy } = commandConfig;
    const commandBuilder = startWith === StartTypes.DOCKER ? new DockerCommandParametersBuilder() : new PythonCommandParametersBuilder();
    commandBuilder.addDevicesParameters(devices);
    commandBuilder.addProxyParameters(httpProxy, httpsProxy, noProxy);
    const commandExecutable = this.commandExecutableMap[startWith];
    const lineContinueSymbol = this.lineContinueSymbolMap[os];
    const parametersString = commandBuilder.parameters.map((parameter) => parameter.toString()).join(` ${lineContinueSymbol}\n\t`);
    return `${commandExecutable} ${lineContinueSymbol}\n\t${parametersString}`;
  }

}
