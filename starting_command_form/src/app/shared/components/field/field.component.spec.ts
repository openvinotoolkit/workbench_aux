import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FieldComponent } from './field.component';
import { ICommandConstructorField } from '../../models/command-constructor-form';
import { SharedModule } from '../../shared.module';

describe('FieldComponent', () => {
  let component: FieldComponent;
  let fixture: ComponentFixture<FieldComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedModule],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FieldComponent);
    component = fixture.componentInstance;
    component.field = {} as ICommandConstructorField;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
