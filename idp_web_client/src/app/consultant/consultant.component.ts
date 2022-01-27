import {Component, HostListener} from '@angular/core';
import {IdpService} from '../../services/idp.service';
import {MessageService} from 'primeng/api';
import {ConfigurationService} from '../../services/configuration.service';
import {Collapse} from '../../model/Collapse';

@Component({
  selector: 'app-consultant',
  templateUrl: './consultant.component.html',
  styleUrls: ['./consultant.component.css']
})
export class ConsultantComponent {

  windowWidth: number = null;
  collapseLevel = 0;

  constructor(public idpService: IdpService, private messageService: MessageService, private configurationService: ConfigurationService) {
    idpService.onEmptyRelevance.subscribe(() => {
      this.messageService.add({severity: 'success', summary: 'Model Obtained', detail: 'There are no relevant symbols left'});
    });

    this.configurationService.collapse.subscribe(x => {
      this.collapseLevel = x;
      this.calculateWidth();
    });
    console.log(this.configurationService.collapse);

    this.calculateWidth();
  }

  get categories(): string[] {
    const meta = this.idpService.meta;
    if (meta.symbols) {
      // remove duplicates in order-preserving fashion
      return meta.symbols.map(x => x.category).filter(
        (value, index, array) => !array.filter((v, i) => value === v && i < index).length
      );
    }
    return [];
  }

  get style() {
    const width = this.windowWidth + 'px';
    return {width: width};
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    // Recalculate the window width.
    this.calculateWidth();
  }

  calculateWidth() {
    if (this.collapseLevel === Collapse.PRINT) {
        this.windowWidth = 1200;
    } else {
        this.windowWidth = window.innerWidth * 0.97;
    }
  }

  reset(heading: string) {
    this.idpService.meta.resetBasedOnHeading(heading);
    this.idpService.doPropagation();
  }

  restoreLaw(lawTuple) {
    this.idpService.restoreLaw(lawTuple);
  }

}
