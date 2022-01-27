import {Component, ElementRef, Input, OnInit} from '@angular/core';
import {SymbolInfo} from '../../../domain/metaInfo';
import {ConfigurationService} from '../../../services/configuration.service';
import {Visibility} from '../../../model/Visibility';
import {IdpService} from '../../../services/idp.service';

declare var Packery: any;


@Component({
  selector: 'app-configurator',
  templateUrl: './configurator.component.html',
  styleUrls: ['./configurator.component.css']
})
export class ConfiguratorComponent implements OnInit {
  @Input() category: string;

  constructor(private idpService: IdpService, private configurationService: ConfigurationService, private elementRef: ElementRef) {
  }

  get shownSymbols(): SymbolInfo[] {
    const meta = this.idpService.meta;
    if (meta.symbols) {
      const cands = meta.symbols.filter(x => x.category===this.category && x.values.length > 0 && x.idpname.charAt(0) !== '_' && x.view !== 'hidden');
      switch (this.idpService.meta.visibility) {
        case Visibility.ALL:
          return cands;
          break;
        case Visibility.CORE:
          return cands.filter(x => this.idpService.meta.visibility >= x.priority);
          break;
        case Visibility.RELEVANT:
          return cands.filter(x => x.relevant || x.known || x.priority === 0);
          break;
      }
    }
    return [];
  }

  ngOnInit() {

    const pckry = new Packery(this.elementRef.nativeElement, {
      itemSelector: 'app-configurator > app-symbol',
      packery: {
        gutter: 50
      }
    });
    window['pckry'] = pckry;

    const mo = new MutationObserver(x => {
      pckry.reloadItems();
      pckry.layout();
    });
    // auto-layout
    mo.observe(this.elementRef.nativeElement, {childList: true, subtree: true});
  }

}
