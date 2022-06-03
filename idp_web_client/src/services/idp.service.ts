/*

    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

*/

import {ApplicationRef, EventEmitter, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {AppSettings} from './AppSettings';
import {Observable} from 'rxjs';
import {map, share} from 'rxjs/operators';
import {MetaInfo, ValueInfo} from '../domain/metaInfo';
import {ConfigurationService} from './configuration.service';
import {deepCompare} from '../deepCompare';
import {InputMetaInfo} from '../domain/inputmeta';
import {MessageService} from 'primeng/api';
import {SelectItem} from 'primeng/api';
import {CompressionService} from './compression.service';

@Injectable()
export class IdpService {

  openCalls = 0;
  meta: MetaInfo = null;
  history: object[] = [];
  spec: string = null; // logic theory
  previousSpec: string = null;
  previous_active: object = null;
  noProp = false;
  noRel = false;

  // for abstract models
  universal: string[] = [];
  irrelevant: string[] = [];
  given: string[] = [];
  fixed: string[] = [];
  models = '';
  expansions: string[][][] = [[['']]];

  versionInfo = 'Unknown';
  versions = {};
  editor = null;
  IDE = false; // are we on the IDE page ?
  runResult: string[] = [];

  header = null;

  ignoredLaws = [];
  allowIgnoringLaws = false;

  public explanation = null;
  public explanationlaws = null;

  public onEmptyRelevance = new EventEmitter<boolean>();

  constructor(
    public http: HttpClient,
    private settings: ConfigurationService,
    public appRef: ApplicationRef,
    private messageService: MessageService
  ) {
    void this.initObject();
  }

  // utilities

  public ignoredLawsString() {
    const lawIds: string[] = [];
    for (const lawTuple of this.ignoredLaws) {
      lawIds.push(lawTuple[0]);
    }
    return JSON.stringify(lawIds);
  }

  public call(url, call: Object): Observable<Object> {
    this.openCalls++;
    const out = this.http.post<Object>(url, call).pipe(share());
    out.subscribe(x => this.openCalls--, err => {
      console.log(err);
      this.messageService.add({severity: 'error', summary: 'Error', detail: err.statusText});
      this.openCalls--;
      return err;
    });
    return out;
  }

  public async call_eval(meta: MetaInfo, input: Object, extra: string = ''): Promise<object|string> {
    input['code'] = this.spec;
    return this.call(AppSettings.IDP_URL, input).pipe(map(x => {
      if (typeof x === 'string') {
        console.log('Error: ' + x);
        this.messageService.add({severity: 'error', summary: 'Error', detail: x});
        return x;
      }
      return x;
    })).toPromise();
  }

  private async get_latest(URL) {
    const salt = (new Date()).getTime();
    return await this.http.get(`${URL}?${salt}`, {responseType: 'text'}).toPromise();
  }

  // get version, initial idp code + reloadMeta
  public async initObject() {
    this.openCalls++;
    // avoid error message on load
    this.meta = new MetaInfo;
    this.spec = 'vocabulary {} theory {}';
    this.IDE = window.location.pathname.search(/IDE/) !== -1;

    // get versionInfo
    let versions_: string;
    try {
      versions_ = await this.get_latest(AppSettings.VERSIONS_URL);
      this.versions = JSON.parse(JSON.parse(versions_)['files']['versions.json']['content']);
    } catch (e) {
      this.versions = {};
      this.versionInfo = 'Unknowable';
    }
    for (let key in this.versions) {
      if (this.versions[key] === window.location.hostname) {
        this.versionInfo = key;
      }
    }

    if (window.location.search !== '') {
      //    /?gist=1234&file=abcd.idp
      // or /?gist=1234  (specification.idp by default)
      // or /?file=spec.idp
      // or /?weagqswer (lzw encoded)
      const queryString = window.location.search.substr(1);
      const queries = queryString.split('&');
      const query0 = queries[0].split('=');

      if (query0[0] === 'gist' && query0[1] !== '') {
        const URL = 'https://api.github.com/gists/' + query0[1];
        const res = await this.get_latest(URL);
        let specFile: string;
        if (queries.length === 2 ) {
          specFile = queries[1].split('=') [1];
        } else {
          specFile = 'specification.idp';
        }
        this.spec = JSON.parse(res)['files'][specFile]['content'];
      } else if (query0[0] === 'file' && query0[1] !== '') {
        this.spec = await this.get_latest(AppSettings.SPECIFICATION_URL.replace(/specification\.idp/, query0[1]));
      } else {
        const lzw = decodeURIComponent(query0[0]);
        this.spec = (new CompressionService()).decompressString(lzw);
      }
    } else if (this.IDE) {
      this.spec = await this.get_latest(AppSettings.SPECIFICATION_URL.replace(/specification/, 'newIDE'));
    } else {
      this.spec = await this.get_latest(AppSettings.SPECIFICATION_URL);
    }
    this.reloadMeta();
    this.openCalls--;
  }

  private shebang() {
    // redirect using Shebang
    const versionRegex = /^#!\s*(.*)/;
    if (versionRegex.test(this.spec)) {
      const version = versionRegex.exec(this.spec)[1];
      if (! (version in this.versions)) {
        this.messageService.clear();
        this.messageService.add({severity: 'error', summary: 'Unknown version in Shebang', detail: version});
        return;
      }
      if (this.versions[version] !== window.location.hostname) {
        // remove shebang when unsupported by version
        if (['IDP-Z3 0.5.4', 'IDP-Z3 0.5.3', 'IDP-Z3 0.5.1'].includes(version)) {
          this.spec = this.spec.substring(this.spec.indexOf('\n') + 1);
        }
        const search = (window.location.search !== '')
          ? window.location.search
          : '?' + encodeURIComponent((new CompressionService()).compressString(this.spec));
        window.location.href = 'https://' + this.versions[version] + '/' + window.location.pathname + search;
      }
    }
  }

  public toggleIDE() {
    if (this.IDE) {
      this.IDE = false;
      this.previousSpec = ''; // to force meta
      this.reloadMeta().then(() => true);
    } else {
      this.IDE = true;
      if (!this.spec.includes('procedure main()')) {
        alert('A main block will be added.  Please verify it.')
        this.spec = this.spec.concat(`
procedure main() {
  pretty_print(model_expand(T))
}
        `);
      }
    }
    this.appRef.tick()
  }
  public async run() {
    this.shebang();
    this.openCalls++;
    const result = await this.call(AppSettings.IDE_URL, {code: this.spec}).toPromise();
    if (typeof result === 'string') {
      this.runResult = result.split('\n');
    }
    this.openCalls--;
    this.appRef.tick();
  }

  public async reload(URL) {
    this.openCalls++;
    this.spec = await this.get_latest(URL);
    this.reloadMeta();
    this.openCalls--;
  }

  // get meta, init

  public async reloadMeta() {
    this.shebang();

    if (this.IDE) {return; }
    if (this.spec !== this.previousSpec) {
      // call meta
      this.previousSpec = this.spec;

      const metaStr = await this.call(AppSettings.META_URL, {code: this.spec}).toPromise();

      if (typeof metaStr === 'string') {
        this.meta = null;
        this.appRef.tick();
        console.log('Error: ' + metaStr);
        this.messageService.clear();
        this.messageService.add({severity: 'error', summary: 'Syntax Error', detail: metaStr});
        return;
      }
      const meta = MetaInfo.fromInput(metaStr as InputMetaInfo);
      this.meta = meta;
      this.settings.visibility.subscribe(x => this.meta.visibility = x);
      this.ignoredLaws = [];
      this.allowIgnoringLaws = false;

      // If manual propagation is enabled, set noProp to true and add a propagation button to the headers.
      // If it is disabled, remove the prop button if it is present.
      if (this.meta.manualPropagation) {
        this.noProp = true;
        this.header.addPropagationButton();
      } else {
        this.noProp = false;
        this.header.removePropagationButton();
      }
      if (this.meta.manualRelevance) {
        this.noRel = true;
        this.header.addRelevanceButton();
      } else {
        this.noRel = false;
        this.header.removeRelevanceButton();
      }

      this.applyPropagation(this.meta, this.meta.valueinfo);
      this.history.push(this.meta.valueinfo);

      this.appRef.tick();

      if (window['pckry']) {
        window['pckry'].reloadItems();
        window['pckry'].layout();
      }

      await this.doPropagation();

    }
  }

  public ready(): boolean {
    return (this.meta !== null) && (this.spec !== null);
  }

  // eval / propagate

  /*
   * Toggles the propagation.
   */
  public togglePropagation(checked) {
    this.noProp = !checked;
    // If propagation has been turned on, propagate.
    if (!this.noProp) {
      this.doPropagation();
    }
  }

  public toggleRelevance(checked) {
    this.noRel = !checked;
    // If propagation has been turned on, propagate.
    if (!this.noRel) {
      this.doRelevance();
    }
  }

  public async doPropagation(forced = false) {
    if (this.noProp && !forced) {
        return;
    }
    const input = {
      method: 'propagate',
      with_relevance: !this.noRel,
      active: this.meta.idpRepr(false),
      previous_active: this.previous_active,
      expanded: this.meta.expanded(),
      ignore: this.ignoredLawsString()
    };
    let outp = await this.call_eval(this.meta, input);
    if (typeof outp === 'string') { // error
      // Explain error when this occurs
      outp = this.history[this.history.length - 1]; // use last valid result      console.log(outp)
      this.applyPropagation(this.meta, outp);
    } else {
      if(!this.checkUnsat(outp)){
        this.applyPropagation(this.meta, outp);
        if(this.ignoredLaws.length==0){
          this.previous_active = this.meta.idpRepr(true)
        }
        this.history.push(outp);
      }
    }
    this.appRef.tick();
    // void this.doRelevance();
  }

  public async doRelevance(forced = false) {
    if (this.noRel && !forced) {
      return;
    }
    // TODO: ignoredLaws?
    const input = {
      method: 'relevance',
      active: this.meta.idpRepr(false),
      previous_active: this.previous_active,
      expanded: this.meta.expanded()
    };
    let outp = await this.call_eval(this.meta, input);
    if (typeof outp !== 'string') { // no error
      if(!this.checkUnsat(outp)){
        this.applyPropagation(this.meta, outp);
        this.history.push(outp);
      }
    }
    this.appRef.tick();
  }

  public async get_range(info: ValueInfo) {
    if (this.noProp) {
        return;
    }
    const field = info.assignment.valueName
    const input = {
      method: 'get_range',
      active: this.meta.idpRepr(false),
      previous_active: this.previous_active,
      expanded: this.meta.expanded(),
      ignore: this.ignoredLawsString(),
      field: field
    };
    let outp = await this.call_eval(this.meta, input);
    if (typeof outp === 'string') { // error
      // nothing to do.  The message was displayed in call_eval
    } else {
      info.assignment.values =
        [{label: '', value: ''}].concat(
          (outp as string[]).map(
            v => ({label: v.split('_').join(' '), value: v})))
    }
    this.appRef.tick();
  }

  private applyPropagation(meta: MetaInfo, outp: object) {
    meta.env_dec = outp[' Global']['env_dec'];

    for (const s of meta.symbols) {
      for (const val of s.values) {
        const info = outp[s.idpname][val.atom];
        if (info !== undefined) {
          val.assignment.typ = info['typ'];
          val.assignment.normal = info['normal'];
          if (val.assignment.status !==  'EXPANDED' || (info['status'] || '') !== 'GIVEN') {
            val.assignment.status = info['status'] || '';  // else keep the expanded status
          }
          val.assignment.environmental = 'environmental' in info ? info['environmental'] : false;
          val.assignment.is_assignment = 'is_assignment' in info ? info['is_assignment'] : false;
          val.assignment.relevant = 'relevant' in info ? info['relevant'] : true;
          val.assignment.reading = 'reading' in info ? info['reading'] : '';
          if ('values' in info) {
            val.assignment.values = [{label: '', value: ''}].concat(info['values'].map(v => ({label: v.split('_').join(' '), value: v})));
          } else {
            val.assignment.values = null;
          }
          val.assignment.unknown = 'unknown' in info && info['unknown'];
          val.assignment.value = 'value' in info ? info['value'] : null;
          val.assignment.value2 = String(val.assignment.value);
          if (val.assignment.value2 != null && val.assignment.value2.includes('/') && 4<val.assignment.value2.length) {
            const m = val.assignment.value2.match(/(.*)\/(.*)/);
            if (m) {
              console.log(val.assignment.value2, m[1], m[2])
              val.assignment.value2 = String((+m[1])/(+m[2]))
            }
          }
        }
      }
    }
  }

  // eval explain

  public async explain(symbol: string, value: string): Promise<object> {
    const obj = this.meta.idpRepr(false);
    const vInfo = this.getValueInfo(symbol, value);
    const assignment = vInfo.assignment;
    let prefix = '';
    if (assignment.typ === 'Bool' && ! assignment.value) {
      prefix = '~';
    }

    const input = {
      method: 'explain',
      active: obj,
      symbol: symbol,
      value: prefix + value,
      expanded: this.meta.expanded(),
      ignore: this.ignoredLawsString()
    };
    const outp = await this.call_eval(this.meta, input);
    if (typeof outp !== 'string') { // no error
      const paramTree = this.toTree(outp);
      paramTree['*laws*'] = outp['*laws*'];
      return paramTree;
    }
  }

  public getValueInfo(symbol: string, value: string): ValueInfo {
    return this.meta.getSymbol(symbol).getValue(value);
  }

  public getReading(law: string): string {
    if (this.settings.useReading()) {
      return law[1];
    } else {
      return law[0];
    }
  }

  private toTree(outp: object) {
    const paramTree = {};
    for (const key of Object.getOwnPropertyNames(outp)) {
      const current = outp[key];
      const valueList = [];
      for (const val of Object.getOwnPropertyNames(current)) {
        if (current[val].ct || current[val].cf) {
          valueList.push(val);
        } else if (current[val].value !== undefined) {
          valueList.push(val);
        }
      }
      if (valueList.length > 0) {
        paramTree[key] = valueList;
      }
    }
    return paramTree;
  }

  checkUnsat(outp) {
    this.explanation = null;
    this.header.showExplanation = false;
    if (outp['*laws*'] == null) {
      return false;
    }
    // else parse explanation
    this.explanationlaws = outp['*laws*'];
    delete outp['*laws*'];
    this.explanation = this.toTree(outp);
    this.header.showExplanation = true;
    return true;
  }

  // eval optimise

  public async optimise(symbol: string, minimize: boolean) {
    for (const s of this.meta.symbols) { // reset all assignments of this symbol
      if (s.idpname === symbol) {
        for (const v of s.values) {
          v.assignment.reset();
        }
      }
    }
    const extraline = 'term t : V { sum{:true:' + (minimize ? '' : '-') + symbol + '}}';
    const input = {
      method: 'minimize',
      propType: 'approx',
      active: this.meta.idpRepr(false),
      previous_active: this.previous_active,
      symbol: symbol, minimize: minimize,
      expanded: this.meta.expanded(),
      ignore: this.ignoredLawsString()
    };
    const outp = await this.call_eval(this.meta, input, extraline);
    if (typeof outp !== 'string') { // no error
      if(!this.checkUnsat(outp)) {
        this.applyPropagation(this.meta, outp);
        this.doPropagation();
      }
    }
  }

  // eval modelexpand

  public async mx() {
    const input = {
      method: 'modelexpand',
      active: this.meta.idpRepr(false),
      previous_active: this.previous_active,
      expanded: this.meta.expanded(),
      ignore: this.ignoredLawsString()
    };
    const outp = await this.call_eval(this.meta, input);
    if (typeof outp !== 'string') { // no error
      if(!this.checkUnsat(outp)){
        this.applyPropagation(this.meta, outp);
      }
    }else{
      console.log(outp);
    }
  }

  // eval checkCode

  public async checkCode() {
    const selection = this.editor.getModel().getValueInRange(this.editor.getSelection()).trim();
    const input = {method: 'checkCode', active: '', symbol: selection,
                  expanded: false};
    const outp = await this.call_eval(this.meta, input);

    if (typeof outp !== 'string') { // no error
      alert(outp["result"])
    }
  }

  // eval abstract

  public async abstract() {
    this.universal = [];
    this.irrelevant = [];
    this.given = [];
    this.fixed = [];
    this.expansions = [[['']]];
    // TODO: ignoredLaws?
    const input = {method: 'abstract', active: this.meta.idpRepr(false),
                  symbol: '', expanded: this.meta.expanded()};
    const outp = await this.call_eval(this.meta, input);

    if (typeof outp !== 'string') { // no error
      if(!this.checkUnsat(outp)) {
        // copy outp in this.expansions
        this.expansions = [];
        const rows = outp['variable'];
        for (const row of Object.keys(rows)) {
          this.expansions[row] = [];
          const cols = Object.values(rows[row]);
          for (const col of Object.keys(cols)) {
            // @ts-ignore:
            this.expansions[row][col] = [];
            // @ts-ignore:
            const lines = Object.values(cols[col]);
            for (const line of Object.keys(lines)) {
              // @ts-ignore:
              this.expansions[row] [col] [line] = lines[line];
            }
          }
        }
        this.universal = outp['universal'];
        this.irrelevant = outp['irrelevant'];
        this.given = outp['given'];
        this.fixed = outp['fixed'];
        this.models = outp['models'];
      }
    }
  }

  // reset some choices
  public async resetSome(status: string[]) {
    this.meta.resetBasedOnStatus(status);
    this.doPropagation();
  }

  // reset choices, ignored laws, defaults
  public async reset() {
    this.ignoredLaws = [];
    this.allowIgnoringLaws = false;
    const input = {
      method: 'propagate', propType: 'exact',
      active: "{}",
      previous_active: "{}",
      expanded: this.meta.expanded(),
      ignore: "[]"
    };
    let outp = await this.call_eval(this.meta, input);
    if (typeof outp === 'string') { // error
      // Explain error when this occurs
    } else {
      this.history = [];
      this.applyPropagation(this.meta, outp);
      this.history.push(outp);
    }
    this.appRef.tick();
    await this.doPropagation();
    // void this.doRelevance();
  }

  // compare
  public async compare(symbol: string, values: string[]): Promise<object []> {
    const out = await Promise.all(values.map(val => this.cPropagate(symbol, val)));
    this.compareDicts(out);
    return out;
  }

  public async cPropagate(symbol: string, value: string): Promise<object> {
    let obj = this.meta.idpRepr(false);
    if (!(symbol in Object.getOwnPropertyNames(obj))) {
      const symbObj = this.meta.getSymbol(symbol).idpRepr(true);
      obj = {...obj, ...symbObj};
    }
    obj[symbol][value] = {ct: true, cf: false};

    // TODO: ignoredLaws?
    const input = {
      method: 'propagate', propType: 'exact', active: obj,
      expanded: this.meta.expanded()
    };
    const outp = await this.call_eval(this.meta, input);
    if (typeof outp !== 'string')  // no error
      return outp;
  }

  public compareDicts(dicts: object[]) {
    let keys = [];
    try {
      keys = Object.getOwnPropertyNames(dicts[0]).sort();
    } catch (e) {
      return;
    }
    for (const key of keys) {
      if (deepCompare(dicts.map(d => d[key]))) {
        dicts.map(d => delete d[key]);
        continue;
      }
      this.compareDicts(dicts.map(d => d[key]));
    }
  }

  symbolTypes(explanation=this.explanation) {
    if (!this.meta.env_dec) {
      return [''];
    } else {
      const result = [];
      if (0 < this.dependencySymbols('Decisions:',explanation).length) {
        result.push('Decisions:');
      }
      if (0 < this.dependencySymbols('Environment:',explanation).length) {
        result.push('Environment:');
      }
      return result;
    }
  }
  dependencySymbols(type: string, explanation=this.explanation) {
    const expl = Object.getOwnPropertyNames(explanation).filter(symbolName =>
          type === ''
      || (type === 'Decisions:'   && !this.meta.getSymbol(symbolName).environmental)
      || (type === 'Environment:' &&  this.meta.getSymbol(symbolName).environmental)
      );
    return expl;
  }
  getDependencyValues(symbolName: string, explanation=this.explanation) {
    return explanation[symbolName].sort();
  }

  public ignoreLaw(lawTuple) {
    if (this.ignoredLaws.includes(lawTuple)) { return; }
    this.ignoredLaws.push(lawTuple);
    this.doPropagation();
  }

  public restoreLaw(lawTuple) {
    if (!this.ignoredLaws.includes(lawTuple)) { return; }
    this.ignoredLaws = this.ignoredLaws.filter(l => l !== lawTuple);
    this.allowIgnoringLaws = this.ignoredLaws.length > 0;
    this.doPropagation();
  }



  public async lint(): Promise<[]> {
    const input = {
      method: 'lint',
      code: this.spec
    };
    const msgs = this.call_eval(this.meta, input);
    //@ts-ignore
    return await msgs;
    // void this.doRelevance();
  }
}
