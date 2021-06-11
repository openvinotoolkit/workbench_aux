import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckboxButtonInputComponent } from './checkbox-button-input.component';

describe('CheckboxButtonInputComponent', () => {
  let component: CheckboxButtonInputComponent;
  let fixture: ComponentFixture<CheckboxButtonInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CheckboxButtonInputComponent ]
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
