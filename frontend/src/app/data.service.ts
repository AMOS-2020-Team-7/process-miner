import { Injectable } from '@angular/core';

import { HttpClient , HttpErrorResponse, HttpParams} from '@angular/common/http';
import {  throwError } from 'rxjs';
import { retry, catchError, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  private REST_API_SERVER_TESTS = 'http://www.mocky.io/v2/5ed74c41320000d456274640';

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

  public sendGetRequest() {
    return this.httpClient.get(this.REST_API_SERVER_TESTS, {
        params: new HttpParams({
            fromString: ''
        }),
        observe: 'response'
    }).pipe(retry(3), catchError(this.handleError), tap(res => {

    }));
}
}
