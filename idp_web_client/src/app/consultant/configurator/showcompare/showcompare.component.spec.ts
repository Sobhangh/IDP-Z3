import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {ShowcompareComponent} from './showcompare.component';

describe('ShowcompareComponent', () => {
  let component: ShowcompareComponent;
  let fixture: ComponentFixture<ShowcompareComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ShowcompareComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowcompareComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
