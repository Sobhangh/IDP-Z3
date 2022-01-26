import {Component, Input, OnInit} from '@angular/core';
import {IdpService} from '../../../../services/idp.service';
import {CurrentAssignment, ValueInfo} from '../../../../domain/metaInfo';
import {DynamicDialogConfig, DynamicDialogRef} from 'primeng/api';

@Component({
  selector: 'app-showcompare',
  templateUrl: './showcompare.component.html',
  styleUrls: ['./showcompare.component.css']
})
export class ShowcompareComponent implements OnInit {

  @Input()
  symbolName: string;

  @Input()
  valueNames: string [];

  comparisons: object [];

  constructor(public idpService: IdpService, public ref: DynamicDialogRef, public config: DynamicDialogConfig) {
    this.symbolName = config.data['symbolName'];
    this.valueNames = config.data['valueNames'];
  }

  get dependencySymbols() {
    return Object.keys(this.comparisons[0]);
  }
  get dependencyValuesExist() {
    return Object.keys(this.comparisons[0][this.dependencySymbols[0]]).length > 0;
  }

  getDependencyValues(symbolName: string): string [] {
    return Object.keys(this.comparisons[0][symbolName]).sort();
  }
  makeValueInfo(comparison: object, symbol: string, value: string) {
    const info = ValueInfo.clone(this.idpService.getValueInfo(symbol, value)); // make copy?
    // info.assignment = new CurrentAssignment();
    if (comparison[symbol][value].ct) {
      info.assignment.value = true;
    }
    if (comparison[symbol][value].cf) {
      info. assignment.value = false;
    }
    return info;
  }
  range(len) {
    return Array(len).keys();
  }

  ngOnInit() {
    console.log('compare called', this.symbolName, this.valueNames);

    this.idpService.compare(this.symbolName, this.valueNames).then(x => {
        // Remove yourself from the explanation
        this.comparisons = x;
        for (const c of this.comparisons) {
          console.log(this.comparisons, c, this.symbolName);
          if (c[this.symbolName]) {delete c[this.symbolName]; }
        }
      }
    );
    console.log(this.comparisons);
  }

}
