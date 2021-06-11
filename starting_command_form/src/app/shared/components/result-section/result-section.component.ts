import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { ICommandConfig, OperatingSystems, StartTypes } from '../../models/command-constructor-form';
import { commandDefaults } from '../../constants';
import { MessagesService } from '../../services/messages.service';

@Component({
  selector: 'wb-result-section',
  templateUrl: './result-section.component.html',
  styleUrls: [ './result-section.component.scss' ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ResultSectionComponent {
  @Input()
  public commandConfig: ICommandConfig;

  public StartTypes = StartTypes;
  public OperatingSystems = OperatingSystems;

  public readonly commands = {
    installPythonWrapper: `python3 -m pip install -U ${commandDefaults.pythonWrapperName}`,
    pullImage: `docker pull ${commandDefaults.dockerImageWithTag}`,
  };
  public readonly resultStepsMessages = this.messagesService.messages.resultSteps;

  constructor(private messagesService: MessagesService) {}

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
}
