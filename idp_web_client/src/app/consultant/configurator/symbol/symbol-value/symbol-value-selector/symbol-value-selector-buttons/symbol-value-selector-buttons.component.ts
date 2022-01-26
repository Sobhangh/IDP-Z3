import {Component, Input, OnInit} from '@angular/core';
import {CurrentAssignment, SymbolInfo} from '../../../../../../../domain/metaInfo';
import {IdpService} from '../../../../../../../services/idp.service';

@Component({
  selector: 'app-symbol-value-selector-buttons',
  templateUrl: './symbol-value-selector-buttons.component.html',
  styleUrls: ['./symbol-value-selector-buttons.component.css']
})
export class SymbolValueSelectorButtonsComponent implements OnInit {

  @Input()
  assignment: CurrentAssignment;
  @Input()
  symbolInfo: SymbolInfo;

  constructor(public idpService: IdpService) {
  }

  ngOnInit() {
  }

  update(value) {
    this.assignment.value = value;
    this.assignment.status = value == null ? 'UNKNOWN' : 'GIVEN';
    this.idpService.meta.atomConsistency(this.assignment);
    if(value == null) this.idpService.meta.resetBasedOnStatus(['CONSEQUENCE', 'ENV_CONSQ']);
    this.idpService.doPropagation();
  }
}
