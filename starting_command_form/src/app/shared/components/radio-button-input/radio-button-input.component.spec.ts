import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RadioButtonInputComponent } from './radio-button-input.component';
import {SharedModule} from '../../shared.module';

describe('RadioButtonInputComponent', () => {
  let component: RadioButtonInputComponent;
  let fixture: ComponentFixture<RadioButtonInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedModule],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RadioButtonInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
