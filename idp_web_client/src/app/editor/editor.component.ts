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
  editorOptions = {theme: 'IDP', language: 'IDP'};

  private change = false;
  textModeUnicode = false;

  public onInitEditor(editor: any) {
    this.idpService.editor = editor;
    const idpService = this.idpService

    this.idpService.editor.addCommand([monaco.KeyMod.CtrlCmd | monaco.KeyCode.KEY_S], function() {
      if (idpService.IDE) {
        idpService.run();
      } else {
        idpService.header.display = false
        idpService.appRef.tick()
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
        return

      } else {
        // Run the static code analysis.
        this.idpService.doSCA().then((msgs) => {
          console.log(msgs);
          const marker_msgs = [];
          for (let i = 0; i < msgs.length; i++) {
            const msg = msgs[i];
            let severity = null;
            if (msg['type'] === 'Warning') {
                severity = monaco.MarkerSeverity.Info;
            } else {
                severity = monaco.MarkerSeverity.Error;
            }
            const marker_msg = {
                startLineNumber: msg['line'],
                startColumn: msg['col'],
                endLineNumber: msg['line'],
                endColumn: msg['col'],
                message: msg['details'],
                severity: severity
            };
            marker_msgs.push(marker_msg);
            console.log(msg);
          }
          const model = this.idpService.editor.getModel();
          monaco.editor.setModelMarkers(model, 'owner', marker_msgs)
        });
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
      line = line.replace(/≥/g, '>=');
      line = line.replace(/≠/g, '~=');
      line = line.replace(/∀/g, '!');
      line = line.replace(/∃/g, '?');
      line = line.replace(/∧/g, '&');
      line = line.replace(/∨/g, '|');
      line = line.replace(/¬/g, '~');
      line = line.replace(/⨯/g, '*');

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
      line = line.replace(/>=/g, '≥');
      line = line.replace(/¬=/g, '≠');
      line = line.replace(/~=/g, '≠');
      line = line.replace(/\!/g, '∀');
      line = line.replace(/\?/g, '∃');
      line = line.replace(/\&/g, '∧');
      line = line.replace(/\|/g, '∨');
      line = line.replace(/~/g, '¬');
      line = line.replace(/\*/g, '⨯');

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
