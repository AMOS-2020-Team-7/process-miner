import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../data.service';
import {  takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { HttpResponse } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';

declare const wheelzoom: any;

const REST_API_HN = 'http://127.0.0.1:5000/graphs/hn/get';

export interface Approach {
  item: string;
  viewValue: string;
}

export interface Consent {
  item: string;
  viewValue: string;
}

export interface Errortype {
  item: string;
  viewValue: string;
}

interface QueryResult {
  image: string;
  metadata: any;
  numberOfSessions: number;
}


@Component({
  selector: 'app-processes',
  templateUrl: './processes.component.html',
  styleUrls: ['./processes.component.css']
})


export class ProcessesComponent implements OnInit, OnDestroy {
  selectedApproach = 'None';
  selectedConsent = 'None';
  selectedError = '';
  selectedDepth = 0.0;
  destroy$: Subject<boolean> = new Subject<boolean>();
  trustedImageUrl: SafeUrl;
  imageEncodedInBase64 = '';
  dotString: string;

  approaches: Approach[] = [
    {item: 'REDIRECT', viewValue: 'Redirect'},
    {item: 'EMBEDDED', viewValue: 'Embedded'}
  ];
  consents: Consent[] = [
    {item: 'all', viewValue: 'All'},
    {item: 'get_accounts', viewValue: 'Get Accounts'},
    {item: 'get_transactions', viewValue: 'Get Transactions'}
  ];
  errors: Errortype[] = [];
  encodedImage: any;

  constructor(private dataService: DataService, private sanitizer: DomSanitizer) {
  }

  ngOnInit(): void {
    wheelzoom(document.querySelector('img.zoom'));
    this.loadGraph();
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    // Unsubscribe from the subject
    this.destroy$.unsubscribe();
  }

  public loadGraph() {
    // tslint:disable-next-line:max-line-length
    this.dataService.requestData<QueryResult>(REST_API_HN, {approach: this.selectedApproach , threshold: this.selectedDepth, consent_type: this.selectedConsent, error_type: this.selectedError, format: 'dot'}).subscribe(data => {
      this.loadNewImageToImageViewer(data.image);
      this.loadErrors(data.metadata.errors, data.numberOfSessions);
    });
  }

  public loadErrors(responseErrors, responseNumberOfSessions){    
    this.errors = [];
    for (var error in responseErrors) {
          this.errors.push({viewValue: error + "       -  " + ((responseErrors[error] * 100) /responseNumberOfSessions).toFixed(2)+ "%", item: error});
      } 
    this.selectedError = '';
  }

  public loadNewImageToImageViewer(encodedImage){
    this.dotString = atob(encodedImage.split(',')[1]);
  }

  public resetPage(){
    window.location.reload();
  }

  public reset(){
    this.selectedApproach = 'None';
    this.selectedConsent = 'None';
    this.selectedDepth = 0.0;
    this.selectedError = '';

    this.loadGraph();
  }




}
