import { ChangeDetectionStrategy, Component, HostBinding, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'wb-text-input',
  templateUrl: './text-input.component.html',
  styleUrls: ['./text-input.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TextInputComponent {
  @Input()
  public value: string;

  @Input()
  @HostBinding('class.disabled')
  set disabled(value: boolean) {
    this._disabled = value;
    this.active = false;
  }

  get disabled(): boolean {
    return this._disabled;
  }

  private _disabled = false;

  @Input()
  @HostBinding('class.active')
  public active = false;

  @Input()
  public placeholder?: string;

  @Output()
  public changeText = new EventEmitter<string>();

  handleEdit(inputElement: HTMLElement): void {
    if (this.disabled) {
      return;
    }
    this.active = true;
    inputElement.focus();
  }

  handleSave(value: string): void {
    if (this.disabled) {
      return;
    }
    this.active = false;
    this.changeText.emit(value);
  }
}
