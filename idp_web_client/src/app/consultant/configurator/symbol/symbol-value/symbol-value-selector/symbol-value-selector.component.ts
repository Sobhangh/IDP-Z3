import {Component, Input, OnInit} from '@angular/core';
import {ConfigurationService} from '../../../../../../services/configuration.service';
import {ValueInfo, SymbolInfo} from '../../../../../../domain/metaInfo';
import {IdpService} from '../../../../../../services/idp.service';

@Component({
  selector: 'app-symbol-value-selector',
  templateUrl: './symbol-value-selector.component.html',
  styleUrls: ['./symbol-value-selector.component.css']
})
export class SymbolValueSelectorComponent implements OnInit {

  @Input()
  info: ValueInfo;
  @Input()
  symbolInfo: SymbolInfo;
  @Input()
  withHeader: boolean;

  reading = 0;

  constructor(private idpService: IdpService, private configurationService: ConfigurationService) {
    this.configurationService.formula.subscribe(x => this.reading = x);
  }

  ngOnInit() {
  }
  calendar_update(info) {
    // hack: https://github.com/primefaces/primeng/issues/2426
    if (info.assignment.value) {
      let d = new Date(info.assignment.value.getTime()
                       - (info.assignment.value.getTimezoneOffset() * 60 * 1000));
      info.assignment.value2 = '#'+d.toISOString().slice(0,10);
      info.assignment.status = 'GIVEN';
      this.idpService.meta.atomConsistency(this.info.assignment);
      this.idpService.doPropagation();
    } else if (info.assignment.value2 != null) {  // value has been emptied
      info.assignment.status = 'UNKNOWN';
      info.assignment.value2 = null;
      this.idpService.meta.atomConsistency(this.info.assignment);
      this.idpService.doPropagation();
    }
  }
  update(info: ValueInfo, event) {
    if (info.assignment.value2 !==event.target.value) {
      info.assignment.value = event.target.value;
      info.assignment.value2 = String(info.assignment.value)
      info.assignment.status = 'GIVEN';
      this.idpService.meta.atomConsistency(this.info.assignment);
      this.idpService.doPropagation();
    }
  }
  confirm(info) {
    info.assignment.status = 'GIVEN';
    this.idpService.doPropagation();
  }

  updateDropdown(info) {
    if (info.assignment.value !== '') {
        info.assignment.status = 'GIVEN';
    } else {
        info.assignment.status = 'UNKNOWN';
        info.assignment.value = null;
    }
    this.idpService.meta.atomConsistency(this.info.assignment);
    this.idpService.doPropagation();
  }

  name() {
    // If there is no header, or the symbol shown is not "normal" (i.e., part of extended view) and is not an assignment,
    // nothing special needs to be done.
    if (!this.withHeader || (!this.info.assignment.is_assignment && !this.info.assignment.normal)) {
      let symbolName = '';
      if (!this.reading || this.info.assignment.reading === '') {
        symbolName += this.info.atom.replace(/\_/g, ' ');
      } else {
        symbolName += this.info.assignment.reading.replace(/\_/g, ' ');
      }
      if (this.info.assignment.typ !== 'Bool') {
        symbolName += ' =\xa0';
      }
      return symbolName;
    }

    const reading = this.info.assignment.reading.replace(/\_/g, ' ');
    // If it is 0-ary, show nothing or only the assigned value.
    if (!reading.includes('(')) {
      if (!reading.includes('=')) {
        return '';
      } else {
        return reading.split('=')[1];
      }
    } else {
      var out = /\w*\((.*)\)/.exec(reading)[1];
      if (this.info.assignment.typ !== 'Bool') {
        return out + ' :\xa0';
      } else {
        return out;
      }
    }
  }
}
