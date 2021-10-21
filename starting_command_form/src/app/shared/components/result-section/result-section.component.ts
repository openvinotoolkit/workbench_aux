import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { Devices, ICommandConfig, OperatingSystems, StartTypes } from '../../models/command-constructor-form';
import { commandDefaults } from '../../constants';
import { MessagesService } from '../../services/messages.service';

@Component({
  selector: 'wb-result-section',
  templateUrl: './result-section.component.html',
  styleUrls: [ './result-section.component.scss' ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ResultSectionComponent implements OnInit {
  @Input()
  public commandConfig: ICommandConfig;

  public StartTypes = StartTypes;
  public Devices = Devices;
  public OperatingSystems = OperatingSystems;

  public readonly commands = {
    pullImage: `docker pull ${commandDefaults.dockerImageWithTag}`,
  };
  public readonly resultStepsMessages = this.messagesService.messages.resultSteps;

  constructor(private messagesService: MessagesService) {}

  ngOnInit(){
    console.log(this.commandConfig);
  }

  get installDockerInstructionsContent(): string {
    const { os } = this.commandConfig;
    const { installDockerInstructions } = this.resultStepsMessages.descriptions;
    if (os === OperatingSystems.WINDOWS) {
      return installDockerInstructions.windows;
    }
    if (os === OperatingSystems.MAC_OS) {
      return installDockerInstructions.macOS;
    }
    return installDockerInstructions.linux;
  }

  get installPythonCommand() {
    const { os } = this.commandConfig;
    const isWindows = os === OperatingSystems.WINDOWS; 
    const pythonBinaryName = `python${isWindows? '': '3'}`;
    return `${pythonBinaryName} -m pip install -U ${commandDefaults.pythonWrapperName}`
  }

  get allocateMemoryForDockerCommand() {
    const { os } = this.commandConfig;
    const isWindows = os === OperatingSystems.WINDOWS;
    return isWindows?
          this.messagesService.messages.resultSteps.descriptions.allocateMemoryForDocker.windows
          : this.messagesService.messages.resultSteps.descriptions.allocateMemoryForDocker.macOS;
  }

  get installPipCommand() {
    const { os } = this.commandConfig;
    const isWindows = os === OperatingSystems.WINDOWS;
    const pythonBinaryName = `python${isWindows? '': '3'}`;
    const pipCommand =  `${pythonBinaryName} -m pip --version`
    return `${this.messagesService.messages.resultSteps.descriptions.installPip}` +
           ` "${pipCommand}". `+
           `${this.messagesService.messages.resultSteps.descriptions.checkPipVersion}`;
  }
}
