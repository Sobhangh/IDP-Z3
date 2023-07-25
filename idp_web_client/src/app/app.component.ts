import {Component, OnInit} from '@angular/core';
import {IdpService} from '../services/idp.service';
import {MessageService} from 'primeng/api';
import { Title } from '@angular/platform-browser';
import {AppSettings} from '../services/AppSettings';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = '';
  specification_url = '';

  constructor(public idpService: IdpService,
              private messageService: MessageService,
              private titleService: Title) {
    idpService.onEmptyRelevance.subscribe(() => {
      this.messageService.add({severity: 'success', summary: 'Model Obtained', detail: 'There are no relevant symbols left'});
    });

  }

  ngOnInit() {
    this.title = this.idpService.IDE ? 'IDP webIDE' : 'Interactive Consultant';
    this.titleService.setTitle( this.title )

    this.specification_url = AppSettings.SPECIFICATION_URL;

    }

}
