import {Component, Input, OnInit, ViewChild, AfterViewInit, DoCheck} from '@angular/core';
import {ConfigurationService} from '../../../../../../services/configuration.service';
import {ValueInfo, SymbolInfo} from '../../../../../../domain/metaInfo';
import {IdpService} from '../../../../../../services/idp.service';

@Component({
  selector: 'app-symbol-value-slider',
  templateUrl: './symbol-value-slider.component.html',
  styleUrls: ['./symbol-value-slider.component.css']
})
export class SymbolValueSliderComponent implements OnInit, AfterViewInit, DoCheck {

  // These variables define the sliders.
  lower_symb: string;
  upper_symb: string;
  lower_bound: number;
  upper_bound: number;

  // The symbolInfo's of the symbols which the sliders affect.
  upperValueInfo: ValueInfo;
  lowerValueInfo: ValueInfo;

  @Input()
  valueInfo: ValueInfo;
  @Input()
  symbolInfo: SymbolInfo;

  @ViewChild('customSlider') slidercomponent;

  // These variable are used to represent the input values.
  lowerInputVal: number;
  upperInputVal: number;

  // These variables are used to check whether the assignment value has updated (in order to update the sliders)
  dirtyLowerInputVal: number;
  dirtyUpperInputVal: number;

  sliderValues: number[] = [0, 100];
  lowerSliderVal = 0;
  upperSliderVal = 100;

  reading = 0;

  constructor(private idpService: IdpService, private configurationService: ConfigurationService) {
    this.configurationService.formula.subscribe(x => this.reading = x);
  }

  ngOnInit() {
    if (this.symbolInfo.slider) {
        // Fetch all the meta information.
        // Because the sliders affect the lower_symb and upper_symb instead of this symbol itself,
        // we need to fetch their info as well.
        this.lower_symb = this.symbolInfo.slider.lower_symbol.replace(' ', '');
        this.upper_symb = this.symbolInfo.slider.upper_symbol.replace(' ', '');
        this.lower_bound = this.symbolInfo.slider.lower_bound;
        this.upper_bound = this.symbolInfo.slider.upper_bound;

        // Fetch the value info's from the idpService.
        if (this.upper_symb !== '') { this.upperValueInfo = this.idpService.getValueInfo(this.upper_symb, this.upper_symb); }
        if (this.lower_symb !== '') { this.lowerValueInfo = this.idpService.getValueInfo(this.lower_symb, this.lower_symb); }


    }
  }

  ngDoCheck() {
      if (this.upperValueInfo && this.upperValueInfo.assignment.value !== this.dirtyUpperInputVal) {
        this.dirtyUpperInputVal = this.upperValueInfo.assignment.value;
        this.setSlider(this.upperValueInfo.assignment.value, true);
      }
      if (this.lowerValueInfo && this.lowerValueInfo.assignment.value !== this.dirtyLowerInputVal) {
        this.dirtyLowerInputVal = this.lowerValueInfo.assignment.value;
        this.setSlider(this.lowerValueInfo.assignment.value, false);
      }
  }


  ngAfterViewInit() {
      // If only a max slider is needed, make the min slider invisible.
      if (this.slidercomponent && !this.lowerValueInfo) {  // Here be dragons.
        this.slidercomponent.el.nativeElement.children.item(0).children.item(1).style['display'] = 'None';
      }
      // If only a min slider is needed, make the man slider invisible.
      if (this.slidercomponent && !this.upperValueInfo) {  // Here be dragons.
        this.slidercomponent.el.nativeElement.children.item(0).children.item(2).style['display'] = 'None';
      }

  }

  update(info: ValueInfo, value) {
    if (info.assignment.value !== value) {
      info.assignment.value = '' + value;  // Cast to string.
      info.assignment.status = 'GIVEN';
      this.idpService.doPropagation();
    }
  }
  confirm(info: ValueInfo, value) {
    info.assignment.status = 'GIVEN';
    this.idpService.doPropagation();
  }

  sliderUpdated(event) {
      // If the sliders were updated, we need to also update the inputfield.
      if (this.lowerSliderVal !== event.values[0]) {
          const lowerVal = event.values[0];

          const lowerSliderPercentage = (lowerVal) / 100;
          this.lowerInputVal = Number(this.lower_bound) + (this.upper_bound - this.lower_bound) * lowerSliderPercentage;
      }
      if (this.upperSliderVal !== event.values[1]) {
          const upperVal = event.values[1];

          const upperSliderPercentage = (upperVal) / 100;
          this.upperInputVal = Number(this.lower_bound) + (this.upper_bound - this.lower_bound) * upperSliderPercentage;
      }

  }

  sliderLetGo(event) {
      // If the slider was let go, update the edited SliderVal and perform propagation with the change!
      if (this.lowerSliderVal !== event.values[0]) {
          this.lowerSliderVal = event.values[0];
          if (this.lowerValueInfo) { this.update(this.lowerValueInfo, this.lowerInputVal); }
      }
      if (this.upperSliderVal !== event.values[1]) {
          this.upperSliderVal = event.values[1];
          if (this.upperValueInfo) { this.update(this.upperValueInfo, this.upperInputVal); }
      }
  }

  setSlider(value, upper) {
            if (!value) {
                // If the value is null, set the slider to an extremum.
                if (upper) {
                    this.sliderValues = [this.sliderValues[0], 100];
                } else {
                    this.sliderValues = [0, this.sliderValues[1]];
                }
            } else {
                // Calculate the position at which the slider should be.
                const sliderPercentage = (value - this.lower_bound) / (this.upper_bound - this.lower_bound);

                // Depending on which slider should be set, set the correct one.
                if (upper) {
                    this.sliderValues = [this.sliderValues[0], Math.round(sliderPercentage * 100)];
                } else {
                    this.sliderValues = [Math.round(sliderPercentage * 100), this.sliderValues[1]];
            }
      }
}


  upperInputUpdated(event) {
      // If the input field is updated, the slider needs to be repositioned accordingly.
      // Check if the value is between the boundaries.
      if (this.upperInputVal < this.lower_bound) { this.upperInputVal = this.lower_bound; }
      if (this.upperInputVal > this.upper_bound) { this.upperInputVal = this.upper_bound; }
      if (this.upperInputVal < this.lowerInputVal) { this.upperInputVal = this.lowerInputVal; }

      // We calculate the relative position of the picked value to its boundaries, then we update the input.
      this.setSlider(this.upperInputVal, true);

      // We finish by confirming that a value was selected.
      if (this.upperValueInfo) { this.update(this.upperValueInfo, this.upperInputVal); }
  }

  lowerInputUpdated(event) {
      // If the input field is updated, the slider needs to be repositioned accordingly.
      // Check if the value is between the boundaries.
      if (this.lowerInputVal < this.lower_bound) { this.lowerInputVal = this.lower_bound; }
      if (this.lowerInputVal > this.upper_bound) { this.lowerInputVal = this.upper_bound; }
      if (this.lowerInputVal > this.upperInputVal) { this.lowerInputVal = this.upperInputVal; }

      // We calculate the relative position of the picked value to its boundaries, then we update the input.
      this.setSlider(this.lowerInputVal, false);

      // We finish by confirming that a value was selected.
      if (this.lowerValueInfo) { this.update(this.lowerValueInfo, this.lowerInputVal); }

  }
}
