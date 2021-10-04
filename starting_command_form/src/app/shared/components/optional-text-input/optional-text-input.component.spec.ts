import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OptionalTextInputComponent } from './optional-text-input.component';
import {SharedModule} from '../../shared.module';

describe('OptionalTextInputComponent', () => {
  let component: OptionalTextInputComponent;
  let fixture: ComponentFixture<OptionalTextInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SharedModule],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OptionalTextInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
