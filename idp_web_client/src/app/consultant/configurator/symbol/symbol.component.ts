import {Component, Input} from '@angular/core';
import {SymbolInfo} from '../../../../domain/metaInfo';
import {IdpService} from '../../../../services/idp.service';
import {ConfigurationService} from '../../../../services/configuration.service';
import {Visibility} from '../../../../model/Visibility';
import {Collapse} from '../../../../model/Collapse';
import { ValueTransformer } from '@angular/compiler/src/util';

@Component({
  selector: 'app-symbol',
  templateUrl: './symbol.component.html',
  styleUrls: ['./symbol.component.css']
})
export class SymbolComponent {

  @Input()
  info: SymbolInfo;

  relevantOnly = false;
  collapseLevel = 0;

  constructor(public idpService: IdpService, private configurationService: ConfigurationService) {
    this.configurationService.visibility.subscribe(x => this.relevantOnly = x === Visibility.RELEVANT);
    this.configurationService.collapse.subscribe(x => this.collapseLevel = x );
  }

  shownRelValues(values) {
    if (this.relevantOnly) {
      return values.filter(x => x.assignment.relevant || x.assignment.known || this.info.priority === 0);
    }
    return this.info.values;
  }
  shownColValues(values) {
    switch (this.collapseLevel) {
      case Collapse.ALL: return values;
      case Collapse.POSSIBLE: return values.filter(x => x.assignment.possible);
      case Collapse.CERTAIN: return values.filter(x => x.assignment.certain);
      case Collapse.PRINT: return values.filter(x =>
        x.assignment.status === 'CONSEQUENCE' || x.assignment.status === 'ENV_CONSQ' ||
        x.assignment.status === 'GIVEN' || x.assignment.status === 'DEFAULT'
      );
    }
  }
  get shownValues() {
    return this.shownColValues(this.shownRelValues(this.info.values));
  }
  hasRelevant() {
    for (const v of this.info.values) {
      if (v.assignment.relevant) {return true; }
    }
    return false;
  }

  withHeader() {
    let count = 0;
    for (const v of this.info.values) {
      if (v.assignment.normal || this.info.view === 'expanded') {count += 1; }
      if (1 < count) {return true; }
    }
    return false;
  }

  get classes() {
    if (this.hasRelevant()) {
      if (this.info.environmental || !this.idpService.meta.env_dec) {
        if (this.withHeader()) {
          return 'my-panel';
        } else {return 'my-panel propo'; }
      } else {
        if (this.withHeader()) {
          return 'green-panel';
        } else {
            return 'green-panel green-propo';
        }
      }
    } else {
        return 'white-panel';
    }
  }

}
