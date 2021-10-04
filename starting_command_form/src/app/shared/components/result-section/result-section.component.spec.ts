import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultSectionComponent } from './result-section.component';
import { SharedModule } from '../../shared.module';
import { ICommandConfig } from '../../models/command-constructor-form';

describe('ResultSectionComponent', () => {
  let component: ResultSectionComponent;
  let fixture: ComponentFixture<ResultSectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ SharedModule ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ResultSectionComponent);
    component = fixture.componentInstance;
    component.commandConfig = { devices: [] } as ICommandConfig;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
