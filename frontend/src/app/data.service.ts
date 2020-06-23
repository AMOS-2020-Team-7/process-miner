import { Injectable } from '@angular/core';

import { HttpClient , HttpErrorResponse, HttpParams} from '@angular/common/http';
import { throwError } from 'rxjs';
import { retry, catchError, tap, take, filter, repeatWhen, delay, switchMap } from 'rxjs/operators';

const REQUEST_REPEAT_DELAY = 250;

interface RequestResponse {
  stateUrl: string;
}

interface StateResponse {
  done: boolean;
  resultUrl: string;
}

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private REST_API_SERVER_TESTS = 'assets/tests/response.json';

  constructor(private httpClient: HttpClient) { }

  handleError(error: HttpErrorResponse) {
    let errorMessage = 'Unknown error!';
    if (error.error instanceof ErrorEvent) {
      // Client-side errors
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side errors
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    window.alert(errorMessage);
    return throwError(errorMessage);
  }

  public requestData<ResultType>(url, parameters) {
    // initiate request
    return this.httpClient.get<RequestResponse>(url, {
      params: parameters,
      observe: 'body'
    }).pipe(
      catchError(this.handleError),
      switchMap((requestResponse: RequestResponse) => {
        console.log('Call: ' + requestResponse);
        const stateUrl = requestResponse.stateUrl;
        console.log(`Getting state from url ${stateUrl}`);
        // get state object
        return this.httpClient.get<StateResponse>(stateUrl).pipe(
          catchError(this.handleError),
          // repeat request to state with delay if result is not ready
          repeatWhen(obsrvbl => obsrvbl.pipe(delay(REQUEST_REPEAT_DELAY))),
          // only accept if request was already processed
          filter((stateResponse: StateResponse) => stateResponse.done),
          take(1),
          // get actual result
          switchMap((stateResponse: StateResponse) => {
            const resultUrl = stateResponse.resultUrl;
            console.log(`Getting result from url ${resultUrl}`);
            return this.httpClient.get<ResultType>(resultUrl);
          })
        );
      })
    );
  }

  public sendGetRequest() {
    return this.httpClient.get(this.REST_API_SERVER_TESTS, {
        params: new HttpParams({
            fromString: ''
        }),
        observe: 'response'
    }).pipe(retry(3), catchError(this.handleError), tap(res => {

    }));
}

public sendGetRequestForImageGraph() {
  return this.httpClient.get(this.REST_API_SERVER_TESTS, {
      params: new HttpParams({
          fromString: ''
      }),
      observe: 'response'
  }).pipe(retry(3), catchError(this.handleError), tap(res => {

  }));
}
}
