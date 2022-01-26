import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {SymbolValueSelectorComponent} from './symbol-value-selector.component';

describe('SymbolValueSelectorComponent', () => {
  let component: SymbolValueSelectorComponent;
  let fixture: ComponentFixture<SymbolValueSelectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [SymbolValueSelectorComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SymbolValueSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
