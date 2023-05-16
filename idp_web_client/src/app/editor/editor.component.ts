import {Component} from '@angular/core';
import {IdpService} from '../../services/idp.service';
import {MessageService} from 'primeng/api';
import {DOCUMENT} from '@angular/common';
import {Inject} from '@angular/core';


@Component({
  selector: 'app-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.css']
})

export class EditorComponent {
  editorOptions = {theme: 'IDP', language: 'IDP', fontFamily: 'Noto mono'};

  private change = false;
  textModeUnicode = false;

  private lintTimeout = null;

  private doLint(idpService) {
    idpService.lint().then((msgs) => {
      const marker_msgs = [];
      for (let i = 0; i < msgs.length; i++) {
        const msg = msgs[i];
        let severity = null;
        if (msg['type'] === 'Warning') {
            severity = monaco.MarkerSeverity.Warning;
        } else {
            severity = monaco.MarkerSeverity.Error;
        }
        const marker_msg = {
            startLineNumber: msg['line'],
            startColumn: msg['colStart'],
            endLineNumber: msg['line'],
            endColumn: msg['colEnd'],
            message: msg['details'],
            severity: severity
        };
        marker_msgs.push(marker_msg);
      }
      const model = idpService.editor.getModel();
      monaco.editor.setModelMarkers(model, 'owner', marker_msgs);
    });
  }

  public onInitEditor(editor: any) {
    this.idpService.editor = editor;
    const idpService = this.idpService;

    this.idpService.editor.addCommand([monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_S], function() {
      if (idpService.IDE) {
        idpService.run();
      } else {
        idpService.header.display = false;
        idpService.appRef.tick();
      }
    });
    this.idpService.editor.model.onDidChangeContent((event) => {
      // Do nothing if the change came from an executeEdits
      if (this.change) {
        this.change = false;
        return;
      } else if (this.textModeUnicode) {
        // Whenever a user has typed, switch back to ASCII
        this.textModeUnicode = false;
        return;

      } else {
        // Run the static code analysis after 1 second of no inputs.
        // We also save the current state of the spec to the localStorage.
        // This will allow the IC to load the spec, even after refreshing. 
        // Helpful to prevent frustration when accidentally opening a new tab or something.
        clearTimeout(this.lintTimeout);
        this.lintTimeout = setTimeout(() => {
            this.doLint(idpService);

            if (idpService.IDE) {
                localStorage.setItem('idpSpecIDE', idpService.editor.model.getLinesContent().join('\n'));
            } else {
                localStorage.setItem('idpSpecIC', idpService.editor.model.getLinesContent().join('\n'));
            }
        }, 1000);
      }
    });

  }


  constructor(public idpService: IdpService, private messageService: MessageService, @Inject(DOCUMENT) document: Document) {

  }

  switchTextMode(encoding) {
    let spec = '';
    if (encoding === 'ascii') {
      // Convert to ASCII
      spec = this.unicodeToAscii(this.idpService.editor.model.getLinesContent());
    } else {
      // Convert to Unicode
      spec = this.asciiToUnicode(this.idpService.editor.model.getLinesContent());
    }
    // Range accepts 4 args: beginLine, beginCol, endLine, endCol.
    // To select the entire text, we can just set the latter two to very large numbers, i.e. the length of the current text.
    const range = new monaco.Range(0, 0, spec.length, spec.length);
    const replaceOp = {identifier: {major: 1, minor: 1}, range: range, text: spec};
    this.change = true;
    this.idpService.editor.executeEdits('symbol-replace', [replaceOp]);

    // Switch the text mode.
    this.textModeUnicode = !this.textModeUnicode;
    this.doLint(this.idpService);
  }

  private unicodeToAscii(lines) {
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];
      let comment = '';

      // Check if there is a comment present, and remove it so that its contents aren't replaced.
      if (line.match('//')) {
        comment = line.match(/\/\/(.*)/g);
        line = line.replace(/\/\/(.*)/g, '');
      }

      // If an annotation is present, replace it by a placeholder and put it back later.
      // As there can be multiple annotations per line (theoretically, at least), we want to capture and replace all of them.
      let annotations = []
      if (line.match(/\[.*]/g)) {
        annotations = line.match(/\[.*?]/g);
        for (let idx in annotations) {
            line = line.replace(annotations[idx], 'ANNOT'+idx);
        }
      }


      line = line.replace(/→/g, '->');
      line = line.replace(/←/g, '<-');
      line = line.replace(/∈/g, 'in');
      line = line.replace(/𝔹/g, 'Bool');
      line = line.replace(/ℤ/g, 'Int');
      line = line.replace(/ℝ/g, 'Real');
      line = line.replace(/⇔/g, '<=>');
      line = line.replace(/⇒/g, '=>');
      line = line.replace(/⇐/g, '<=');
      line = line.replace(/≤/g, '=<');
      line = line.replace(/⊇/g, '>>');
      line = line.replace(/≥/g, '>=');
      line = line.replace(/≜/g, ':=');
      line = line.replace(/≠/g, '~=');
      line = line.replace(/∀/g, '!');
      line = line.replace(/∃/g, '?');
      line = line.replace(/∧/g, '&');
      line = line.replace(/∨/g, '|');
      line = line.replace(/¬/g, '~');
      line = line.replace(/⨯/g, '*');

      // Re-add the annotations.
      for (let idx in annotations) {
        line = line.replace('ANNOT'+idx, annotations[idx])
      }

      // Re-add the comment.
      line += comment;
      lines[i] = line;
    }
    return lines.join('\n');
  }

  private asciiToUnicode(lines) {
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];
      let comment = '';

      // Check if there is a comment present, and remove it so that its contents aren't replaced.
      if (line.match('//')) {
        comment = line.match(/\/\/(.*)/g);
        line = line.replace(/\/\/(.*)/g, '');
      }

      // If an annotation is present, replace it by a placeholder and put it back later.
      // As there can be multiple annotations per line (theoretically, at least), we want to capture and replace all of them.
      let annotations = []
      if (line.match(/\[.*]/g)) {
        annotations = line.match(/\[.*?]/g);
        for (let idx in annotations) {
            line = line.replace(annotations[idx], 'ANNOT'+idx);
        }
      }

      line = line.replace(/->/g, '→');
      line = line.replace(/<-/g, '←');
      line = line.replace(/\bin\b/g, '∈');
      line = line.replace(/\bBool\b/g, '𝔹');
      line = line.replace(/\bInt\b/g, 'ℤ');
      line = line.replace(/\bReal\b/g, 'ℝ');
      line = line.replace(/<=>/g, '⇔');
      line = line.replace(/<⇒/g, '⇔');
      line = line.replace(/⇐>/g, '⇔');
      line = line.replace(/=>/g, '⇒');
      line = line.replace(/<=/g, '⇐');
      line = line.replace(/=</g, '≤');
      line = line.replace(/>>/g, '⊇');
      line = line.replace(/>=/g, '≥');
      line = line.replace(/¬=/g, '≠');
      line = line.replace(/:=/g, '≜');
      line = line.replace(/~=/g, '≠');
      line = line.replace(/\!/g, '∀');
      line = line.replace(/\?/g, '∃');
      line = line.replace(/\&/g, '∧');
      line = line.replace(/~/g, '¬');
      line = line.replace(/\*/g, '⨯');

      // replace first "|" in set expressions by ENQ, to protect it
      const ENQ = "\u0005";
      class CustomReplacer {
        value: string;
        constructor(value) {
          this.value = value;
        }
        [Symbol.replace](string) {
          const matches = string.match(/\{.*?\|.*?\}/g)
          if (matches) {
            for (var match of matches) {
              string = string.replace(match, match.replace('|', ENQ))
            }
          };
          return string;
        }
      }
      line = line.replace(new CustomReplacer(ENQ))
      line = line.replace(/\|/g, '∨');
      line = line.replaceAll(ENQ, "|"); // restore "|"


      // Re-add the annotations.
      for (let idx in annotations) {
        line = line.replace('ANNOT'+idx, annotations[idx])
      }

      // Re-add the comment.
      line += comment;
      lines[i] = line;
    }
    return lines.join('\n');
  }

  public type(char: string) {
    this.idpService.editor.trigger('keyboard', 'type', {text: char});
    this.idpService.editor.focus();
  }

}
