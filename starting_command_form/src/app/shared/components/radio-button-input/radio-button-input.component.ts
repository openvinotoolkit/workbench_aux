import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';
import { IFieldOption } from '../../models/command-constructor-form';

@Component({
  selector: 'wb-radio-button-input',
  templateUrl: './radio-button-input.component.html',
  styleUrls: ['./radio-button-input.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RadioButtonInputComponent {
  @Input()
  public options: IFieldOption[];

  @Input()
  public value: boolean | string;

  @Output()
  public changeValue = new EventEmitter<boolean | string>();
}
