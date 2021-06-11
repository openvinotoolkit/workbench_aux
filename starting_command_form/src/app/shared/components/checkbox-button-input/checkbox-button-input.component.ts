import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';
import { IFieldOption } from '../../models/command-constructor-form';
import { MatCheckboxChange } from '@angular/material/checkbox';

@Component({
  selector: 'wb-checkbox-button-input',
  templateUrl: './checkbox-button-input.component.html',
  styleUrls: [ './checkbox-button-input.component.scss' ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CheckboxButtonInputComponent {
  @Input()
  public options: IFieldOption[];

  @Input()
  public set value(value: string[]) {
    this.selectedOptions = new Set<string>(value);
  }

  public get value(): string[] {
    return Array.from(this.selectedOptions?.values());
  }

  @Input()
  public disabledOptions: string[] = [];

  @Output()
  public changeValue = new EventEmitter<string[]>();

  private selectedOptions = new Set<string>();

  updateSelectedOptions(change: MatCheckboxChange): void {
    const { checked, source: { name } } = change;
    if (checked) {
      this.selectedOptions.add(name);
    } else {
      this.selectedOptions.delete(name);
    }
    this.changeValue.emit(Array.from(this.selectedOptions));
  }
}
