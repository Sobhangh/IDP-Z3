import {Injectable} from '@angular/core';
import {BehaviorSubject, Subject} from 'rxjs';
import {AppSettings} from './AppSettings';
import {Visibility} from '../model/Visibility';
import {Relevance} from '../model/Relevance';
import {Collapse} from '../model/Collapse';
import {Formula} from '../model/Formula';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {

  visibility: Subject<Visibility>;
  collapse:   Subject<Collapse>;
  formula:    BehaviorSubject<Formula>;

  constructor() {
    this.visibility = new BehaviorSubject(AppSettings.DEFAULT_VISIBILITY);
    this.collapse   = new BehaviorSubject(AppSettings.DEFAULT_COLLAPSE);
    this.formula    = new BehaviorSubject(AppSettings.DEFAULT_FORMULA);
  }

  setVisibility(visibility: Visibility): void {
    this.visibility.next(visibility);
  }

  setCollapse(collapse: Collapse): void {
    this.collapse.next(collapse);
  }

  setFormula(formula: Formula): void {
    this.formula.next(formula);
  }

  useReading(): boolean {
    return this.formula.getValue() === Formula.READING;
  }
}
