import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../material.module';
import { RadioButtonInputComponent } from './radio-button-input/radio-button-input.component';
import { CheckboxButtonInputComponent } from './checkbox-button-input/checkbox-button-input.component';
import { FieldComponent } from './field/field.component';
import { ResultSectionComponent } from './result-section/result-section.component';
import { CommandOutputComponent } from './command-output/command-output.component';
import { TextInputComponent } from './text-input/text-input.component';
import { OptionalTextInputComponent } from './optional-text-input/optional-text-input.component';
import { CommandPipe } from '../pipes/command.pipe';

@NgModule({
  declarations: [
    RadioButtonInputComponent,
    CheckboxButtonInputComponent,
    FieldComponent,
    ResultSectionComponent,
    CommandOutputComponent,
    TextInputComponent,
    OptionalTextInputComponent,
    CommandPipe,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MaterialModule,
  ],
  exports: [
    RadioButtonInputComponent,
    CheckboxButtonInputComponent,
    FieldComponent,
    ResultSectionComponent,
  ],
})
export class SharedComponentsModule {}
