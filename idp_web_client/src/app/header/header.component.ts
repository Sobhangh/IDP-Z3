import {Component, OnInit, AfterViewInit} from '@angular/core';
import {MenuItem} from 'primeng/api';
import {DialogModule} from 'primeng/dialog';
import {InputSwitchModule} from 'primeng/inputswitch';
import {Relevance} from '../../model/Relevance';
import {Collapse} from '../../model/Collapse';
import {Formula} from '../../model/Formula';
import {ConfigurationService} from '../../services/configuration.service';
import {Visibility} from '../../model/Visibility';
import {IdpService} from '../../services/idp.service';
import {CompressionService} from '../../services/compression.service';
import {AppSettings} from '../../services/AppSettings';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, AfterViewInit {
  display = false;
  showFileShare = false;
  showFileSave = false;
  showExpansions = false;
  showExplanation = false;
  URL = '';
  origin = '';
  propToggle = true;
  propButton = false;
  relToggle = true;
  relButton = false;

  items: MenuItem[] = [];
  normalItems: MenuItem[] = [];
  printItems: MenuItem[] = [];
  visibility: Visibility;
  collapse: Collapse;
  formula: Formula;

  editorStyle = {width: '50%', padding: '0px'};

  constructor(private configurationService: ConfigurationService, public idpService: IdpService) {
    this.visibility = AppSettings.DEFAULT_VISIBILITY;
    this.collapse   = AppSettings.DEFAULT_COLLAPSE;
    this.formula    = AppSettings.DEFAULT_FORMULA;
  }

  ngAfterViewInit() {
      this.initResizing()
  }

  ngOnInit() {
    // So that idpService can dynamically change the header by manipulating `this.items`.
    this.idpService.header = this;

    if (! this.idpService.IDE) {
      this.items = [
        { label: 'File',
        items: [{
            label: 'New', command: () => {
              const URL = AppSettings.SPECIFICATION_URL.replace(/specification/, 'new');
              this.idpService.reload(URL);
              this.display = true;
            }
          }, {
            label: 'Covid', command: () => {
              this.idpService.reload(AppSettings.SPECIFICATION_URL);
            }
          }, {
            label: 'Polygon', command: () => {
              const URL = AppSettings.SPECIFICATION_URL.replace(/specification/, 'polygon');
              this.idpService.reload(URL);
            }
          }, {
            label: 'Simple Registration', command: () => {
              const URL = AppSettings.SPECIFICATION_URL.replace(/specification/, 'simple_registratie');
              this.idpService.reload(URL);
            }
          }, {
            label: 'Registration', command: () => {
              const URL = AppSettings.SPECIFICATION_URL.replace(/specification/, 'registratie');
              this.idpService.reload(URL);
            }
          }, {
            label: 'Share...', command: () => {
              // don't use "?lzw=..." because parameter is length-limited
              this.origin = window.location.origin;
              var page = window.location.href.split('?')[0].split('IDE')[0];
              page = page + (this.idpService.IDE ? 'IDE' : '');
              this.URL = page + '?' + encodeURIComponent((new CompressionService()).compressString(this.idpService.spec));
              this.showFileShare = true;
            }
          }, {
            label: 'Save...', command: () => {
              console.log(this.idpService.spec);
              var dataURI = "data:" + "theory.idp" + ";utf-8," + this.idpService.spec;
              var a = document.createElement("a");
              // ... set a.href and a.download
              a.href = dataURI;
              a['download'] = "theory.idp";
              // Then click the link:
              var clickEvent = new MouseEvent("click", { "view": window, "bubbles": true, "cancelable": false});
              a.dispatchEvent(clickEvent);
              this.showFileSave = true;
            }
          }]
        },
        {
          label: 'Edit',
          command: () => {this.display = true; }
        },
        {
          /*      label: 'Visibility', icon: 'pi pi-fw pi-eye',
                items: [{
                  label: 'Core', command: () => {
                    this.onVisibilityChanged(Visibility.CORE);
                  }
                }, {
                  label: 'Relevant', command: () => {
                    this.onVisibilityChanged(Visibility.RELEVANT);
                  }
                }, {
                  label: 'All', command: () => {
                    this.onVisibilityChanged(Visibility.ALL);
                  }
                }]
              },
              {
          */
        label: 'View',
          items: [{
            label: 'All', command: () => {
              this.onCollapseChanged(Collapse.ALL);
            }
          }, {
            label: 'Possibly true', command: () => {
              this.onCollapseChanged(Collapse.POSSIBLE);
            }
          }, {
            label: 'Certainly true', command: () => {
              this.onCollapseChanged(Collapse.CERTAIN);
            }
          }, {
            label: 'Print', command: () => {
              this.onCollapseChanged(Collapse.PRINT);
            }
          }, {
            label: 'Formulas',
            items: [{
              label: 'View formulas',
              command: () => {
                this.onFormulaChanged(Formula.FORMULA);
              }
            },
              {
                label: 'View readings',
                command: () => {
                  this.onFormulaChanged(Formula.READING);
                }
              }
            ]
          }, {
            label: 'View in IDE', command: () => {
              this.idpService.toggleIDE();
            }
          }]
        },
        {
          label: 'Reset',
          items: [
            {
              label: 'Full',
              command: () => this.idpService.reset()
            },
            {
              label: 'System choices',
              command: () => this.idpService.resetSome(['CONSEQUENCE', 'ENV_CONSQ', 'EXPANDED'])
            }
          ]
        },
        {
          label: 'Inferences',
          items: [
            {
              label: 'Show 1 model',
              command: () => {
                this.idpService.mx();
              }
            },
            { label: 'Show all models',
              command: () => {
                this.idpService.abstract();
                this.showExpansions = true;
              }
            }
          ]
        },
        { label: 'Help',
          items: [
            { label: 'Video tutorial', command: () => window.open('/assets/Interactive_Consultant.mp4', '_blank')},
            { label: 'Reference', command: () => {
                const version = (this.idpService.versionInfo === 'local' || this.idpService.versionInfo === 'unknown')
                  ? 'latest' : this.idpService.versionInfo.replace('IDP-Z3 ', '');
                window.open('https://docs.idp-z3.be/en/' + version + '/', '_blank'); }},
            { label: 'Cheatsheet', command: () => {
                const version = (this.idpService.versionInfo === 'local' || this.idpService.versionInfo === 'unknown')
                  ? 'latest' : this.idpService.versionInfo.replace('IDP-Z3 ', '');
                window.open('https://docs.idp-z3.be/en/' + version + '/summary.html', '_blank'); }},
          ]
        }
      ];
    } else {
      this.items = [
        { label: 'File',
        items: [{
            label: 'New', command: () => {
              const URL = AppSettings.SPECIFICATION_URL.replace(/specification/, 'newIDE');
              this.idpService.reload(URL);
            }
          }, {
            label: 'Share...', command: () => {
              // don't use "?lzw=..." because parameter is length-limited
              this.origin = window.location.origin;
              var page = window.location.href.split('?')[0].split('IDE')[0];
              page = page + (this.idpService.IDE ? 'IDE' : '');
              this.URL = page + '?' + encodeURIComponent((new CompressionService()).compressString(this.idpService.spec));
              this.showFileShare = true;
            }
          }, {
            label: 'Save...', command: () => {
              console.log(this.idpService.spec);
              var dataURI = "data:" + "theory.idp" + ";utf-8," + this.idpService.spec;
              var a = document.createElement("a");
              // ... set a.href and a.download
              a.href = dataURI;
              a['download'] = "theory.idp";
              // Then click the link:
              var clickEvent = new MouseEvent("click", { "view": window, "bubbles": true, "cancelable": false});
              a.dispatchEvent(clickEvent);
              this.showFileSave = true;
            }
          }]
        },
        {
          label: 'Run',
          command: () => {this.idpService.run(); }
        },
        {
          label: 'Check code',
          command: () => {this.idpService.checkCode(); }
        },
        {
          label: 'View in IC',
          command: () => {this.idpService.toggleIDE(); }
        },
        { label: 'Help',
          items: [
            { label: 'Reference', command: () => {
                const version = (this.idpService.versionInfo === 'local' || this.idpService.versionInfo === 'unknown')
                  ? 'latest' : this.idpService.versionInfo.replace('IDP-Z3 ', '');
                window.open('https://docs.idp-z3.be/en/' + version + '/', '_blank'); }},
            { label: 'Cheatsheet', command: () => {
                const version = (this.idpService.versionInfo === 'local' || this.idpService.versionInfo === 'unknown')
                  ? 'latest' : this.idpService.versionInfo.replace('IDP-Z3 ', '');
                window.open('https://docs.idp-z3.be/en/' + version + '/summary.html', '_blank'); }},
          ]
        }
      ];
    }
    this.normalItems = this.items;
    this.printItems = [
      { label: 'Print',
        command: () => {
          window.print();
        }},
      { label: 'Close',
        command: () => {
          this.onCollapseChanged(Collapse.ALL);
        }},
    ];
    // this.onVisibilityChanged(this.visibility);
    this.onCollapseChanged(this.collapse);
    this.onFormulaChanged(this.formula);
  }


/*  onVisibilityChanged(visibility: Visibility) {
    this.configurationService.setVisibility(visibility);
    const curSetting = this.items[2].items;
    for (const a of curSetting) {
      // @ts-ignore
      a.icon = '';
    }
    // @ts-ignore
    curSetting[visibility].icon = 'pi pi-fw pi-eye';
  }
  */

  onCollapseChanged(collapse: Collapse) {
    this.configurationService.setCollapse(collapse);

    if (collapse === Collapse.PRINT) {
      // Replace header by print header
      this.items = this.printItems;
    } else if (! this.idpService.IDE) {  // add icon for View menu (and not Help in IDE)
      this.items = this.normalItems;
        const curSetting = this.items[2].items;
        for (const a of curSetting) {
          // @ts-ignore
          a.icon = '';
        }

        // @ts-ignore
        curSetting[collapse].icon = 'pi pi-fw pi-eye';
    }
  }

  onFormulaChanged(formula: Formula) {
    if (! this.idpService.IDE) {
      this.configurationService.setFormula(formula);
      // @ts-ignore
      const curSetting = this.items[2].items[3].items;
      if (curSetting) {
        for (const a of curSetting) {
          // @ts-ignore
          a.icon = '';
        }
        // @ts-ignore
        curSetting[formula].icon = 'pi pi-fw pi-eye';
      }
    }
  }

  layout() {
    window['pckry'].layout();
  }

  checkCode() {
    this.idpService.checkCode();
  }

  copyURL() {
    const selBox = document.createElement('textarea');
    selBox.style.position = 'fixed';
    selBox.style.left = '0';
    selBox.style.top = '0';
    selBox.style.opacity = '0';
    selBox.value = this.URL;
    document.body.appendChild(selBox);
    selBox.focus();
    selBox.select();
    document.execCommand('copy');
    document.body.removeChild(selBox);
  }

  /*
   * onChange function for the propagation/relevance toggle.
   *
   */
  toggleProp(e) {
    this.idpService.togglePropagation(e.checked);
  }
  toggleRel(e) {
    this.idpService.toggleRelevance(e.checked);
  }

  addPropagationButton() {
    // If the button is already present, do nothing.
    if (this.propButton) {
        return;
    }
    // Add the button on index 5.
    const propButton = {label: 'Propagate', command: () => this.idpService.doPropagation(true)};
    this.items[4].items.splice(2, 0, propButton);

    this.propButton = true;
    this.propToggle = false;
  }

  removePropagationButton() {
    // If the button is not present, return.
    if (!this.propButton) {
        return;
    }
    // Delete the button.
    console.log(this.items[4].items.splice(2, 1));

    this.propButton = false;
    this.propToggle = true;
  }

  addRelevanceButton() {
    // If the button is already present, do nothing.
    if (this.relButton) {
        return;
    }
    // Add the button on index 5.
    const relButton = {label: 'Relevance', command: () => this.idpService.doRelevance(true)};
    this.items[4].items.splice(3, 0, relButton);

    this.relButton = true;
    this.relToggle = false;
  }

  removeRelevanceButton() {
    // If the button is not present, return.
    if (!this.relButton) {
        return;
    }
    // Delete the button.
    console.log(this.items[4].items.splice(3, 1));

    this.relButton = false;
    this.relToggle = true;
  }

  initResizing() {
    const resizer = document.getElementById('resizer');
    const editorStyle = this.editorStyle;
    const idpService = this.idpService;
    let dragging = false;

    function resize (e) {
      if (!dragging) {
        return;
      }

      // Modify the size of the sidepanel.
      editorStyle.width = e.clientX + 'px';

      // Auto-resize the editor to the size of its div.
      idpService.editor.layout();
    }

    // Check if panel should resize when moving the mouse.
    document.addEventListener('mousemove', resize);

    // Enable panel resizing whenever the mousedown is recorded on the resizer.
    resizer.addEventListener('mousedown', function () {dragging = true; });

    // Disable panel resizing if the mouse is let go.
    document.addEventListener('mouseup', function () {dragging = false; });
  }
}
