import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommandConstructorComponent } from './command-constructor.component';
import { SharedModule } from '../shared/shared.module';

describe('CommandConstructorComponent', () => {
  let component: CommandConstructorComponent;
  let fixture: ComponentFixture<CommandConstructorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CommandConstructorComponent ],
      imports: [ SharedModule ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CommandConstructorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
