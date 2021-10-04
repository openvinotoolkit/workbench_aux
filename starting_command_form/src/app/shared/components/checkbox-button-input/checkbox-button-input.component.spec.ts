import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckboxButtonInputComponent } from './checkbox-button-input.component';
import {SharedModule} from '../../shared.module';

describe('CheckboxButtonInputComponent', () => {
  let component: CheckboxButtonInputComponent;
  let fixture: ComponentFixture<CheckboxButtonInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedModule],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CheckboxButtonInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
