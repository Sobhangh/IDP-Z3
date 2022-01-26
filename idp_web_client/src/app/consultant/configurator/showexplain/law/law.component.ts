import {Component, Input, OnInit} from '@angular/core';
import {IdpService} from '../../../../../services/idp.service';

@Component({
  selector: 'app-law',
  templateUrl: './law.component.html',
  styleUrls: ['./law.component.css']
})
export class LawComponent {
  @Input()
  lawTuple; // (string, string)

  constructor(public idpService: IdpService) {
  }

  public changeLaw(event) {
    if(event.currentTarget.checked){
      this.idpService.restoreLaw(this.lawTuple);
    }else{
      this.idpService.ignoreLaw(this.lawTuple);
    }
  }
}
