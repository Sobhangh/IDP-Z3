import {Component, Input, OnInit} from '@angular/core';
import {SymbolInfo} from '../../../../../domain/metaInfo';
import {IdpService} from '../../../../../services/idp.service';
import {DialogService} from 'primeng/api';
import {ShowcompareComponent} from '../../showcompare/showcompare.component';

@Component({
  selector: 'app-symbol-header',
  templateUrl: './symbol-header.component.html',
  styleUrls: ['./symbol-header.component.css'],
  providers: [DialogService]
})
export class SymbolHeaderComponent implements OnInit {

  @Input()
  info: SymbolInfo;

  longInfoVisible = false;

  constructor(private idpService: IdpService, private dialogService: DialogService) {
  }
  show() {
    const ref = this.dialogService.open(ShowcompareComponent, {
      header: 'comparison',
      data: {
        symbolName: this.info.idpname,
        valueNames: this.compareValues
      }
    });
  }

  ngOnInit() {
  }
  get compareValues() {
    return this.info.values.filter(x => x.comparison).map(v => v.assignment.valueName);
  }
  resetCompareValues() {
    this.info.values.map(x => x.comparison = false);
  }
}
