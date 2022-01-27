import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { IDEComponent } from './IDE.component';

describe('IDEComponent', () => {
  let component: IDEComponent;
  let fixture: ComponentFixture<IDEComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ IDEComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IDEComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
