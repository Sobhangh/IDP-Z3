import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {ShowexplainComponent} from './showexplain.component';

describe('ShowexplainComponent', () => {
  let component: ShowexplainComponent;
  let fixture: ComponentFixture<ShowexplainComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ShowexplainComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowexplainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
