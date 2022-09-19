import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {APP_BASE_HREF} from '@angular/common';

import {AppComponent} from './app.component';
import {IdpService} from '../services/idp.service';
import { CompressionService } from '../services/compression.service';
import {HttpClientModule} from '@angular/common/http';
import {SliderModule} from 'primeng/slider';
import {InputSwitchModule} from 'primeng/inputswitch';
import {FormsModule} from '@angular/forms';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ButtonModule} from 'primeng/button';
import {HeaderComponent} from './header/header.component';
import {ListboxModule} from 'primeng/listbox';
import {SymbolComponent} from './consultant/configurator/symbol/symbol.component';
import {ConfiguratorComponent} from './consultant/configurator/configurator.component';
import {CommonModule} from '@angular/common';
import {
  CalendarModule,
  DialogModule,
  DialogService,
  DropdownModule,
  InputTextModule,
  MenubarModule,
  MessageModule,
  MessageService,
  MessagesModule,
  OverlayPanelModule,
  PanelModule,
  ProgressSpinnerModule,
  SelectButtonModule,
  SidebarModule,
  SplitButtonModule,
  TabViewModule,
  TooltipModule
} from 'primeng/primeng';
import {FlexLayoutModule} from '@angular/flex-layout';
import {SymbolValueComponent} from './consultant/configurator/symbol/symbol-value/symbol-value.component';
import {SymbolHeaderComponent} from './consultant/configurator/symbol/symbol-header/symbol-header.component';
import {SymbolValueSelectorComponent} from './consultant/configurator/symbol/symbol-value/symbol-value-selector/symbol-value-selector.component';
import {ConfigurationService} from '../services/configuration.service';
import {ShowexplainComponent} from './consultant/configurator/showexplain/showexplain.component';
import {UndoComponent} from './consultant/configurator/showexplain/undo/undo.component';
import {LawComponent} from './consultant/configurator/showexplain/law/law.component';
import {ShowcompareComponent} from './consultant/configurator/showcompare/showcompare.component';
import {SymbolValueSelectorButtonsComponent} from './consultant/configurator/symbol/symbol-value/symbol-value-selector/symbol-value-selector-buttons/symbol-value-selector-buttons.component';
import {EditorComponent} from './editor/editor.component';
import {MonacoEditorModule, NgxMonacoEditorConfig} from 'ngx-monaco-editor';
import {ToastModule} from 'primeng/toast';
import {DynamicDialogModule} from 'primeng/dynamicdialog';
import { SymbolValueSliderComponent } from './consultant/configurator/symbol/symbol-value/symbol-value-slider/symbol-value-slider.component';
import { IDEComponent } from './IDE/IDE.component';
import { IDELineComponent } from './IDE/IDELine/IDELine.component';
import { ConsultantComponent } from './consultant/consultant.component';

export function monacoLoad() {
  // Register IDP language
  monaco.languages.register({id: 'IDP' });

  // Register a tokens provider for IDP
  monaco.languages.setMonarchTokensProvider('IDP', {
      tokenizer: {
          root: [
              // Block names
              // @ts-ignore
              [/vocabulary|theory|structure|display|procedure/, 'block'],

              // Keys
              // @ts-ignore
              [/\b(type) (?=\w)|\:=?|constructed from|\+|\.|\,|\(|\)|\{|\}|\*|;/, 'key'],
              // @ts-ignore
              [/(lambda)\b/, 'key'],

              // Built-in types
              // For some reason, Monaco's regex does not properly detect a leading \b (which we need to avoid highlighting e.g. ArtInt).
              // Instead, we manually enumerate the possible leading characters for our types
              // @ts-ignore
              [/→(Real|Int|Bool)\b/, 'builtin'],
              // @ts-ignore
              [/>(Real|Int|Bool)\b/, 'builtin'],
              // @ts-ignore
              [/\s(Real|Int|Bool)\b/, 'builtin'],
              // @ts-ignore
              [/(ℝ|𝔹|ℤ)/, 'builtin'],

              // Comments
              // @ts-ignore
              [/\/\/.*$/, 'comment'],

              // Annotations
              // @ts-ignore
              [/\[[a-zA-Z 0-9:]+\]/, 'annotation'],
          ],
      },
  });

  // Define a new theme that contains only rules that match this language
  // 'key' and 'block' are vs-code defaults.
  // @ts-ignore
  monaco.editor.defineTheme('IDP', {
     base: 'vs',
     inherit: true,
     rules: [
         { token: 'block', foreground: '3300AA'},
         { token: 'builtin', foreground: 'aa0022'},
         { token: 'annotation', foreground: '0022aa'},
     ]
   });
 }

const monacoConfig: NgxMonacoEditorConfig = {
  baseUrl: 'assets/',
  onMonacoLoad: monacoLoad,
};


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    SymbolComponent,
    ConfiguratorComponent,
    SymbolValueComponent,
    SymbolHeaderComponent,
    SymbolValueSelectorComponent,
    ShowexplainComponent,
    ShowcompareComponent,
    SymbolValueSelectorButtonsComponent,
    EditorComponent,
    SymbolValueSliderComponent,
    IDEComponent,
    IDELineComponent,
    ConsultantComponent,
    UndoComponent,
    LawComponent
  ],
  imports: [
    CalendarModule,
    CommonModule,
    BrowserModule,
    BrowserAnimationsModule,
    DropdownModule,
    HttpClientModule,
    FormsModule,
    SliderModule,
    InputSwitchModule,
    ButtonModule,
    ListboxModule,
    SelectButtonModule,
    FlexLayoutModule,
    PanelModule,
    SplitButtonModule,
    TooltipModule,
    DialogModule,
    MessagesModule,
    OverlayPanelModule,
    ProgressSpinnerModule,
    MenubarModule,
    MonacoEditorModule.forRoot(monacoConfig),
    SidebarModule,
    MessageModule,
    TabViewModule,
    DynamicDialogModule,
    ToastModule,
    InputTextModule,
  ],
  providers: [IdpService, ConfigurationService, MessageService,
    DialogService, CompressionService,
    {provide: APP_BASE_HREF, useValue: '/'}],
  bootstrap: [AppComponent],
  entryComponents: [ShowcompareComponent]
})
export class AppModule {
}
