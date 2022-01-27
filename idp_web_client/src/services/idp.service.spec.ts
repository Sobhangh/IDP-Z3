import {TestBed} from '@angular/core/testing';

import {IdpService} from './idp.service';
import {RemoteIdpCall} from '../domain/remote-data';
import {HttpClient, HttpHandler} from '@angular/common/http';

describe('IdpService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    providers: [IdpService, HttpClient, HttpHandler]
  }));

  it('should be created', () => {
    const service: IdpService = TestBed.get(IdpService);
    expect(service).toBeTruthy();
  });

  it('can get hello world from the remote', () => {
    const service: IdpService = TestBed.get(IdpService);
    service.callIDP(new RemoteIdpCall('procedure main() {print("hello world")}')).subscribe(
      out => expect(out.stdout).toBe('hello world'));
  });
});
