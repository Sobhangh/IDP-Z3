import {Relevance} from '../model/Relevance';
import {Visibility} from '../model/Visibility';
import {Collapse} from '../model/Collapse';
import {Formula} from '../model/Formula';

export class AppSettings {
  // adapt URL for local development  
  public static ORIGIN            = window.location.origin.replace(':4201', ':5000');

  public static IDP_URL           = window.location.origin.replace(':4201', ':5000') + '/eval';
  public static SPECIFICATION_URL = window.location.origin.replace(':4201', ':5000') + '/examples/specification.idp';
  public static META_URL          = window.location.origin.replace(':4201', ':5000') + '/meta';
  public static IDE_URL           = window.location.origin.replace(':4201', ':5000') + '/run';

  public static VERSIONS_URL = 'https://api.github.com/gists/5d82c61fa39e8aa23da1642a2e2b420a';
  public static DEFAULT_VISIBILITY = Visibility.CORE;
  public static DEFAULT_COLLAPSE   = Collapse.ALL;
  public static DEFAULT_FORMULA    = Formula.READING;
  public static DEFAULT_TIMEOUT = 3;
}
