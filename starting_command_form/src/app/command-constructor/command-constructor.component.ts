import { ChangeDetectionStrategy, Component, OnDestroy } from '@angular/core';

import { commandConstructorFormFieldsMap } from '../shared/constants';
import { Devices, FormControlNames, ICommandConstructorField, OperatingSystems } from '../shared/models/command-constructor-form';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { MessagesService } from '../shared/services/messages.service';
import { OSDetector } from '../shared/models/os-detector';

@Component({
  selector: 'wb-command-constructor',
  templateUrl: './command-constructor.component.html',
  styleUrls: [ './command-constructor.component.scss' ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CommandConstructorComponent implements OnDestroy {
  // TODO Add service and/or json file for messages

  public generalOptionsFields = [
    commandConstructorFormFieldsMap[FormControlNames.DOCKER_INSTALLED],
    commandConstructorFormFieldsMap[FormControlNames.OS],
    commandConstructorFormFieldsMap[FormControlNames.DEVICES],
  ];

  public advancedOptionsFields = [
    commandConstructorFormFieldsMap[FormControlNames.START_WITH],
    commandConstructorFormFieldsMap[FormControlNames.HTTP_PROXY],
    commandConstructorFormFieldsMap[FormControlNames.HTTPS_PROXY],
    commandConstructorFormFieldsMap[FormControlNames.NO_PROXY],
  ];

  public commandFormGroup: FormGroup = null;

  public incompatibleDevicesSelected = false;

  public readonly messages = this.messagesService.messages;

  private unsubscribe$ = new Subject();

  constructor(private fb: FormBuilder, private messagesService: MessagesService) {
    this.commandFormGroup = this._buildFormGroup([
      ...this.generalOptionsFields,
      ...this.advancedOptionsFields,
    ]);
    const devicesField = commandConstructorFormFieldsMap[FormControlNames.DEVICES];
    // Disable devices for selected OS
    this.commandFormGroup.get(FormControlNames.OS).valueChanges.pipe(takeUntil(this.unsubscribe$)).subscribe((os: OperatingSystems) => {
      if (os !== OperatingSystems.LINUX) {
        this.commandFormGroup.get(FormControlNames.DEVICES).setValue([ Devices.CPU ]);
        const allDevices = [ ...devicesField.options ].map(({ value }) => value as string);
        devicesField.disabledOptions.next(allDevices);
      } else {
        devicesField.disabledOptions.next([ Devices.CPU ]);
      }
    });
    // Disable HDDL and NCS2 devices to prevent simultaneous selection
    this.commandFormGroup.get(FormControlNames.DEVICES).valueChanges.pipe(takeUntil(this.unsubscribe$)).subscribe((devices: Devices[]) => {
      this.incompatibleDevicesSelected = devices.includes(Devices.NCS2) || devices.includes(Devices.HDDL);

      const currentDisabledDevices = devicesField.disabledOptions.getValue();
      if (devices.includes(Devices.NCS2)) {
        devicesField.disabledOptions.next([ ...currentDisabledDevices, Devices.HDDL ]);
      } else if (devices.includes(Devices.HDDL)) {
        devicesField.disabledOptions.next([ ...currentDisabledDevices, Devices.NCS2 ]);
      } else {
        devicesField.disabledOptions.next([ Devices.CPU ]);
      }
    });
    // Set OS control value with detected platform
    this.commandFormGroup.get(FormControlNames.OS).setValue(OSDetector.os);
  }

  private _buildFormGroup(fields: ICommandConstructorField[]): FormGroup {
    const controlsConfig = fields.reduce((acc, field) => {
      acc[field.name] = new FormControl(field.value);
      return acc;
    }, {});
    return this.fb.group(controlsConfig);
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
