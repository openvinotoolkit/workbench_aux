import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CommandConstructorComponent } from './command-constructor.component';
import { SharedModule } from '../shared/shared.module';



@NgModule({
  declarations: [CommandConstructorComponent],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports: [CommandConstructorComponent]
})
export class CommandConstructorModule { }
