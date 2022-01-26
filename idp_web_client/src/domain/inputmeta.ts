// These interfaces are used as scheme for the CSV
export interface InputSymbolInfo {  // corresponds to box heading
  idpname: string;
  type: string;
  priority?: string;
  showOptimize?: boolean;
  view: string;
  environmental: string;
  guiname?: string;
  shortinfo?: string;
  longinfo?: string;
  unit?: string;
  category?: string;
  slider: InputSliderInfo;
}

export interface InputValueInfo { // one line in box
  idpname: string;
  shortinfo?: string;
  longinfo?: string;
  category?: string;
  guiname?: string;
}

export interface InputMetaInfo {  // list of symbol & value info
  symbols: InputSymbolInfo[];
  valueinfo: any;

  timeout: number;
  optionalPropagation: boolean;
  manualPropagation: boolean;
  optionalRelevance: boolean;
  manualRelevance: boolean
}

export interface InputSliderInfo {
  lower_bound: number;
  upper_bound: number;
  lower_symbol: string;
  upper_symbol: string;
}
