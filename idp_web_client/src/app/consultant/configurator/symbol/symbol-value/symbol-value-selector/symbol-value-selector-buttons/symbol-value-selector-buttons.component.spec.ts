import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {SymbolValueSelectorButtonsComponent} from './symbol-value-selector-buttons.component';

describe('SymbolValueSelectorButtonsComponent', () => {
  let component: SymbolValueSelectorButtonsComponent;
  let fixture: ComponentFixture<SymbolValueSelectorButtonsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [SymbolValueSelectorButtonsComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SymbolValueSelectorButtonsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
