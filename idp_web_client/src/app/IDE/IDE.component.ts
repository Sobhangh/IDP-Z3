import { Component, OnInit } from '@angular/core';
import {IdpService} from '../../services/idp.service';

@Component({
  selector: 'app-IDE',
  templateUrl: './IDE.component.html',
  styleUrls: ['./IDE.component.css']
})
export class IDEComponent implements OnInit {

  constructor(public idpService: IdpService) { }

  ngOnInit() {
      const resizer = document.getElementById('resizer_IDE');
      const editor = document.getElementById('editor_IDE');
      const output = document.getElementById('output');
      const idpService = this.idpService;
      let dragging = false;

      /*
       * Resize the editor & output if dragging is enabled.
       */
      function resize (e)  {
          if (!dragging) {
              return;
          }
          const leftWidth = (e.clientX - 10) + 'px';
          const rightWidth = (window.innerWidth - e.clientX - 50) + 'px';
          editor.style.width = leftWidth;
          output.style.width = rightWidth;

          /* Auto-resize the editor to the size of its div */
          idpService.editor.layout();
      }

      // Set the mousemove event listener.
      document.addEventListener('mousemove', resize);

      // Enable dragging when clicking the resizer.
      resizer.addEventListener('mousedown', function () {dragging = true; });

      // Disable dragging when mouseup -- anywhere on the screen.
      document.addEventListener('mouseup', function () {dragging = false; });
  }

}
