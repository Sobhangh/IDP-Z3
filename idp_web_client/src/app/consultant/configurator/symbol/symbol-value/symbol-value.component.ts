import {Component, Input, OnInit} from '@angular/core';
import {SymbolInfo, ValueInfo} from '../../../../../domain/metaInfo';

@Component({
  selector: 'app-symbol-value',
  templateUrl: './symbol-value.component.html',
  styleUrls: ['./symbol-value.component.css']
})
export class SymbolValueComponent implements OnInit {

  @Input()  valueInfo: ValueInfo;
  @Input()  symbolInfo: SymbolInfo;
  @Input()  onlyone: number;
  @Input()  withHeader: boolean;

  longInfoVisible = false;

  constructor() {
  }

  ngOnInit() {
  }

}
