import {AppSettings} from '../services/AppSettings';
import {InputMetaInfo, InputSymbolInfo, InputValueInfo} from './inputmeta';
import {Relevance} from '../model/Relevance';
import {Visibility} from '../model/Visibility';
import {SelectItem} from 'primeng/api';

export class CurrentAssignment {
  symbolName: string; // e.g. Sides
  valueName: string; // atom string
  reading: string;
  normal: boolean;

  typ = null;
  value = null;   // internal value; may be a ratio that needs conversion
  value2: String = null;  // displayed string
  values: SelectItem[] = null;

  relevant = true;
  status = null;
  environmental = false;
  is_assignment = false;
  unknown = false;

  get known(): boolean {
    return this.value !== null;
  }

  get true(): boolean {
    return this.value === true;
  }

  get choice(): boolean {
    return this.status === 'GIVEN' || this.status === 'EXPANDED' || this.status === 'DEFAULT';
  }

  get non_user_choice(): boolean {
    return this.status === 'EXPANDED';
  }

  get consequence(): boolean {
    return this.status === 'CONSEQUENCE' || this.status === 'ENV_CONSQ';
  }

  get universal(): boolean {
    return this.status === 'UNIVERSAL';
  }

  static clone(inp: CurrentAssignment): CurrentAssignment {
    const out = new CurrentAssignment();
    out.symbolName = inp.symbolName;
    out.valueName = inp.valueName;
    out.reading = inp.reading;

    out.typ = inp.typ;
    out.value = inp.value;
    out.values = inp.values;

    out.relevant   = inp.relevant;
    out.status     = inp.status;
    out.environmental = inp.environmental;
    out.is_assignment = inp.is_assignment;
    out.unknown    = inp.unknown; // per Z3
    return out;
  }

  idpRepr(all: boolean): Object {
    const included = all || !this.consequence;
    if (this.typ === 'Bool') {
      return {
        'typ': 'Bool',
        'value': included ? this.value : '',
        'status': this.status
      };
    } else if (this.typ === 'Date') {
      return {
        'typ': 'Date',
        'value': included ? this.value2 : '',
        'status': this.status
      };
    }{
      return {
        'value': this.value,
        'typ': this.typ,
        'status': this.status
      };
    }
  }

  reset() {
    this.value = null;
    this.value2 = '';
    this.unknown = false;
  }
}

export class SymbolInfo {
  idpname: string;
  type: string;
  priority: number;
  showOptimize: boolean;
  view: string;
  environmental: string;
  guiname: string;
  shortinfo?: string;
  longinfo?: string;
  unit?: string;
  category?: string;
  slider: SliderInfo;

  values: ValueInfo[];

  get relevant() {
    return this.values.some(x => x.assignment.relevant);
  }

  get known() {
    return this.values.some(x => x.assignment.known);
  }

  static fromInput(inp: InputSymbolInfo): SymbolInfo {
    const out = new SymbolInfo();
    out.idpname = inp.idpname;
    out.type = inp.type;
    out.priority = inp.priority === 'core' ? 0 : 2;
    out.showOptimize = inp.showOptimize || false;
    out.view = inp.view || '';
    out.environmental = inp.environmental;
    out.guiname = inp.guiname || inp.idpname;
    out.shortinfo = inp.shortinfo;
    out.longinfo = inp.longinfo;
    out.unit = inp.unit;
    out.category = inp.category;
    out.slider = inp.slider || null;

    out.values = [];
    return out;
  }

  atomConsistency(a: CurrentAssignment) {
    // makes sure that a user entry is not blocked by the content of another field
    // e.g. Sides = 3 is shown in a list box AND as a sentence
    if (!a.is_assignment) return;
    if (a.typ !== 'Bool' ) { // if assigning a ground value to a number or constructed type
      for (const v of this.values) { // for each line of the symbol
        if ( v.assignment.valueName === a.valueName) {  // exact match
          v.assignment.value = a.value; // to copy from explain panel to base page
        } else if (v.assignment.is_assignment) {
          if ( v.assignment.valueName == a.valueName + ' = ' + a.value) {
                v.assignment.value = true;  // confirm same assignment (but in boolean form)
                v.assignment.status = a.status
          } else if (v.assignment.valueName.startsWith(a.valueName)
                    && v.assignment.value == true){  // invalidate other assignment
              v.assignment.value = null
              v.assignment.status = 'UNKNOWN'
          }
        }
      }
    } else { // a.typ == 'Bool'
      const valueName = a.valueName.split(" = ")[0]
      const value = a.valueName.split(" = ")[1]
      for (const v of this.values) { // for each line of the symbol
        if (v.assignment.valueName == valueName) {  // direct value assignment
          if (a.value == true) {
            v.assignment.value = value;
            v.assignment.status = a.status
          } else if (value == v.assignment.value) {
            v.assignment.value = null;
            v.assignment.status = 'UNKNOWN'
          }
        }  // no need to update the other assignment in boolean form
      }
    }
  }

  getValue(name: string) {
    for (const x of this.values) { // search first on exact match
      if (x.atom === name) { return x; }
    }
    for (const x of this.values) { // use partial match (to find entry field for explainer)
      const l = x.atom.length;
      if (x.atom === name.substr(0, l)) { return x; }
    }
  }

  idpRepr(all: boolean): Object {
    const out = {};
    out[this.idpname] = this.values
      .filter(v => v.assignment.known && (all || v.assignment.choice))
      .map(x => x.idpRepr(all))
      .reduce((a, b) => { return {...a, ...b};}, {});
    return out;
  }
}

export class ValueInfo {
  shortinfo?: string;
  longinfo?: string;
  assignment: CurrentAssignment = new CurrentAssignment();
  comparison = false;

  constructor(public atom: string, symbolName: string) {
    this.assignment.symbolName = symbolName;
    this.assignment.valueName = atom;
  }

  static fromInput(inp: InputValueInfo): ValueInfo {
    const out = new ValueInfo(inp.idpname, 'INPUT VALUE INFO');
    out.shortinfo = inp.shortinfo;
    out.longinfo = inp.longinfo;
    if (inp.guiname) {
      out.atom = inp.guiname;
    }
    return out;
  }

  static clone(inp: ValueInfo): ValueInfo {
    const out = new ValueInfo(inp.atom, inp.assignment.symbolName);
    out.shortinfo = inp.shortinfo;
    out.longinfo = inp.longinfo;
    out.atom = inp.atom;
    out.comparison = inp.comparison;
    out.assignment = CurrentAssignment.clone(inp.assignment);
    return out;
  }

  idpRepr(all: boolean): Object {
    const out = {};
    out[this.atom] = this.assignment.idpRepr(all);
    return out;
  }
}

export class MetaInfo {

  symbols: SymbolInfo[];
  valueinfo: any;

  timeout: number;
  optionalPropagation = false;
  manualPropagation = false;
  optionalRelevance = false;
  manualRelevance = false;
  visibility: Visibility = AppSettings.DEFAULT_VISIBILITY;
  env_dec = false;

  static fromInput(inp: InputMetaInfo): MetaInfo {
    const out = new MetaInfo();
    out.timeout = inp.timeout || AppSettings.DEFAULT_TIMEOUT;
    out.optionalPropagation = inp.optionalPropagation;
    out.manualPropagation = inp.manualPropagation;
    out.optionalRelevance = inp.optionalRelevance;
    out.manualRelevance = inp.manualRelevance;
    out.symbols = inp.symbols.map(SymbolInfo.fromInput);
    out.valueinfo = inp.valueinfo;
    for (const symb of out.symbols) {
      if (!out.valueinfo[symb.idpname]) {
        console.log('Unknown Idpname: ', symb.idpname);
        continue;
      }
      for (const v of Object.keys(out.valueinfo[symb.idpname])) {
        if (v.startsWith('__')) {
        } else {
          const out = new ValueInfo(v, symb.idpname);
          symb.values.push(out);
        }
      }
    }
    return out;
  }

  getSymbol(symbolName: string): SymbolInfo {
    return this.symbols.filter(x => x.idpname === symbolName)[0];
  }

  idpRepr(all: boolean): Object {
    return this.symbols.map(x => x.idpRepr(all))
                       .reduce((a, b) => {return {...a, ...b};}, {});
  }

  expanded(): Object {
    return this.symbols.filter(x => x.view === 'expanded')
                       .map(x => x.idpname);
  }

  atomConsistency(a: CurrentAssignment) {
    this.symbols.forEach(x => x.atomConsistency(a));
  }

  resetBasedOnStatus(statuses: string[]) {
    this.symbols.forEach(x =>
      x.values.forEach(y => {
        if (statuses.includes(y.assignment.status)) {
          y.assignment.reset();
          y.assignment.status = 'UNKNOWN';
          y.assignment.relevant = true;
        }
      })
    );
  }

  resetBasedOnHeading(heading: string) {
    this.symbols.forEach(x => {
      if (x.category === heading) {
        x.values.forEach(y => {
          y.assignment.reset();
          y.assignment.status = 'UNKNOWN';
          y.assignment.relevant = true;
        });
      }
    });
  }
}

export class SliderInfo {
  lower_bound: number;
  upper_bound: number;
  lower_symbol: string;
  upper_symbol: string;
}
