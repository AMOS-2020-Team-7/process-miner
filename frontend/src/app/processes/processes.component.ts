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

export interface Method {
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
  selectedApproach = '';
  selectedMethod = '';
  selectedError = '';
  selectedDepth = 0.0;
  destroy$: Subject<boolean> = new Subject<boolean>();
  trustedImageUrl: SafeUrl;
  imageEncodedInBase64 = '';
  dotString: string;

  approaches: Approach[] = [
    {item: 'redirect', viewValue: 'Redirect'},
    {item: 'embedded', viewValue: 'Embedded'}
  ];
  methods: Method[] = [
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
    this.dataService.requestData<QueryResult>(REST_API_HN, {approach: this.selectedApproach , threshold: this.selectedDepth, method_type: this.selectedMethod, error_type: this.selectedError, format: 'dot'}).subscribe(data => {
      this.loadNewImageToImageViewer(data.image);
      this.loadErrors(data.metadata.errors, data.numberOfSessions);
    });
  }

  public loadErrors(responseErrors, responseNumberOfSessions){
    this.errors = [];
    let percentage: string;
    for (const error of Object.keys(responseErrors)) {
          percentage = ((responseErrors[error] * 100) / responseNumberOfSessions).toFixed(2);
          this.errors.push({viewValue: error + '       -  ' + percentage + '%', item: error});
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
    this.selectedMethod = 'None';
    this.selectedDepth = 0.0;
    this.selectedError = '';

    this.loadGraph();
  }




}
