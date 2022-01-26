import {Component, OnInit} from '@angular/core';
import {IdpService} from '../services/idp.service';
import {MessageService} from 'primeng/api';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = '';

  constructor(public idpService: IdpService,
              private messageService: MessageService,
              private titleService: Title) {
    idpService.onEmptyRelevance.subscribe(() => {
      this.messageService.add({severity: 'success', summary: 'Model Obtained', detail: 'There are no relevant symbols left'});
    });

  }

  ngOnInit() {
    this.title = this.idpService.IDE ? 'IDP webIDE' : 'Interactive Consultant';
    this.titleService.setTitle( this.title );
    }

}
