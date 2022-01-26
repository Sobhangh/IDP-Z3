import {Component, Input, OnInit} from '@angular/core';
import {IdpService} from '../../../../services/idp.service';

@Component({
  selector: 'app-showexplain',
  templateUrl: './showexplain.component.html',
  styleUrls: ['./showexplain.component.css']
})
export class ShowexplainComponent implements OnInit {

  @Input()
  symbolName: string;

  @Input()
  valueName: string;

  @Input()
  status: string;

  @Input()
  environmental: boolean;

  explanation: object;
  laws: string[] = [];

  constructor(public idpService: IdpService) {
  }

  ngOnInit() {
    this.idpService.explain(this.symbolName, this.valueName).then(x => {
      this.laws = x['*laws*'];
      delete x['*laws*'];
      this.explanation = x;
    });
  }

}
