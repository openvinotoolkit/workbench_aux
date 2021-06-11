import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RadioButtonInputComponent } from './radio-button-input.component';

describe('RadioButtonInputComponent', () => {
  let component: RadioButtonInputComponent;
  let fixture: ComponentFixture<RadioButtonInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RadioButtonInputComponent ]
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
