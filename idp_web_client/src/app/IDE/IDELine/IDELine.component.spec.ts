import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {IDELineComponent} from './IDELine.component';

describe('IDELineComponent', () => {
  let component: IDELineComponent;
  let fixture: ComponentFixture<IDELineComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [IDELineComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IDELineComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
