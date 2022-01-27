import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {SymbolValueComponent} from './symbol-value.component';

describe('SymbolValueComponent', () => {
  let component: SymbolValueComponent;
  let fixture: ComponentFixture<SymbolValueComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [SymbolValueComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SymbolValueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
