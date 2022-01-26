import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-IDELine',
  templateUrl: './IDELine.component.html',
  styleUrls: ['./IDELine.component.css']
})
export class IDELineComponent {
  @Input()
  line = '';

  constructor() {
  }
}
