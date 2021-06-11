import { ChangeDetectionStrategy, Component, forwardRef, Input } from '@angular/core';
import { FieldTypes, FieldValueType, ICommandConstructorField } from '../../models/command-constructor-form';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'wb-field',
  templateUrl: './field.component.html',
  styleUrls: [ './field.component.scss' ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => FieldComponent),
      multi: true,
    },
  ]
})
export class FieldComponent implements ControlValueAccessor {
  public FieldTypes = FieldTypes;

  @Input()
  public field: ICommandConstructorField;

  public value: FieldValueType;

  public formControlOnChange: (_: FieldValueType) => void;

  handleInputChange(value): void {
    this.formControlOnChange(value);
  }

  writeValue(value: FieldValueType): void {
    this.value = value;
  }

  registerOnChange(fn: (value: FieldValueType) => void): void {
    this.formControlOnChange = fn;
  }

  registerOnTouched(fn: (value: FieldValueType) => void): void {}
}
