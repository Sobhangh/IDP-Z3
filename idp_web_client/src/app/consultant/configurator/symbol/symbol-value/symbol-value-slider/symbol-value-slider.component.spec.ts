import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SymbolValueSliderComponent } from './symbol-value-slider.component';

describe('SymbolValueSliderComponent', () => {
  let component: SymbolValueSliderComponent;
  let fixture: ComponentFixture<SymbolValueSliderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SymbolValueSliderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SymbolValueSliderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
