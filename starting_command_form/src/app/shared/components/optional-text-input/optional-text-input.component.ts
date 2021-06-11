import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';

import { booleanOptions } from '../../constants';

@Component({
  selector: 'wb-optional-text-input',
  templateUrl: './optional-text-input.component.html',
  styleUrls: ['./optional-text-input.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OptionalTextInputComponent {
  @Input()
  public enabled = false;

  @Input()
  public value: string;

  @Input()
  public placeholder?: string;

  @Output()
  public changeValue = new EventEmitter<string | null>();

  private _currentValue: string = null;

  public booleanOptions = booleanOptions;

  handleRadioButtonInputChange(isEnabled: boolean): void {
    this.enabled = isEnabled;
    const textInputValue = isEnabled ? this._currentValue : null;
    this.changeValue.emit(textInputValue);
  }

  handleTextInputChange(value: string): void {
    this.changeValue.emit(value);
    this._currentValue = value;
  }
}
