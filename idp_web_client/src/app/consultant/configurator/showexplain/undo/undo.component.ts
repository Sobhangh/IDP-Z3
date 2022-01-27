import {Component, Input, OnInit} from '@angular/core';
import {ValueInfo} from '../../../../../domain/metaInfo';
import {ShowexplainComponent} from '../showexplain.component';
import {IdpService} from '../../../../../services/idp.service';

@Component({
  selector: 'app-undo',
  templateUrl: './undo.component.html',
  styleUrls: ['./undo.component.css']
})
export class UndoComponent implements OnInit {

  @Input()
  valueInfo: ValueInfo;

  @Input()
  parent: ShowexplainComponent;

  constructor(public idpService: IdpService) {
  }

  public reset() {
    const a = this.valueInfo.assignment;
    a.value = '';
    a.status = 'UNKNOWN';
    this.idpService.meta.atomConsistency(a);
    this.idpService.doPropagation();
    this.parent.explanation = null;
  }

  ngOnInit() {
  }

}
