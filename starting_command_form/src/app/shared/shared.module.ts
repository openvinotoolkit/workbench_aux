import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { MaterialModule } from './material.module';
import { SharedComponentsModule } from './components/shared-components.module';

@NgModule({
  imports: [
    /* Shared Angular modules */
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    /* Shared project modules */
    MaterialModule,
    SharedComponentsModule,
  ],
  exports: [
    /* Shared Angular modules */
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    /* Shared project modules */
    MaterialModule,
    SharedComponentsModule,
  ],
})
export class SharedModule {}
