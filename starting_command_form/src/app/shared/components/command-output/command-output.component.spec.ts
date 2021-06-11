import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommandOutputComponent } from './command-output.component';
import { SharedModule } from '../../shared.module';

describe('CommandOutputComponent', () => {
  let component: CommandOutputComponent;
  let fixture: ComponentFixture<CommandOutputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommandOutputComponent ],
      imports: [ SharedModule ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CommandOutputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
