import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../data.service';
import {  takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { HttpResponse } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';

declare const wheelzoom: any;

const REST_API_HN = 'http://127.0.0.1:5000/graphs/hn/get';

const ARG_APPROACH = 'approach';
const ARG_THRESHOLD = 'threshold';
const ARG_METHOD_TYPE = 'method_type';
const ARG_ERROR_TYPE = 'error_type';
const ARG_FORMAT = 'format';

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
  errorNum: string;
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
  destroy$: Subject<boolean> = new Subject<boolean>();
  trustedImageUrl: SafeUrl;
  imageEncodedInBase64 = '';
  dotString: string;
  selectedBank: string;
  bankChartData: any=[{"bank":"ADORSYS","amount":45},{"bank":"not available","amount":4}];
  methodChartData: any=[{"bank":"ADORSYS","amount":45},{"bank":"not available","amount":4}];
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

  private getParameters() {
    const parameters = {};
    parameters[ARG_FORMAT] = 'dot';
    if (this.selectedApproach) {
      parameters[ARG_APPROACH] = this.selectedApproach;
    }
    if (this.selectedMethod) {
      parameters[ARG_METHOD_TYPE] = this.selectedMethod;
    }
    if (this.selectedError) {
      parameters[ARG_ERROR_TYPE] = this.selectedError;
    }
    return parameters;
  }

  public loadGraph() {
    const parameters = this.getParameters();
    this.dataService.requestData<QueryResult>(REST_API_HN, parameters).subscribe(data => {
      this.bankChartData = Object.entries(data.metadata.banks).map((f) => ({'bank': f[0], 'amount': f[1]}));
      this.methodChartData = Object.entries(data.metadata.methods).map((f) => ({'bank': f[0], 'amount': f[1]}));
      this.loadNewImageToImageViewer(data.image);
      this.loadErrors(data.metadata.errors, data.numberOfSessions);
    });
  }

  public loadErrors(responseErrors, responseNumberOfSessions){
    this.errors = [];
    let percentage: string;
    for (const error of Object.keys(responseErrors)) {
          percentage = ((responseErrors[error] * 100) / responseNumberOfSessions).toFixed(2);
          this.errors.push({viewValue: error + '       -  ' + percentage + '%', item: error, errorNum: responseErrors[error]});
    }
    const sortByErrorNum = (a, b) => {
      if (a.errorNum > b.errorNum) {
        return -1;
      }
      if (a.errorNum < b.errorNum) {
        return 1;
      }
      return 0;
    };
    this.errors.sort(sortByErrorNum);
    this.selectedError = '';
  }

  public loadNewImageToImageViewer(encodedImage){
    this.dotString = atob(encodedImage.split(',')[1]);
  }

  public selectBank(selected: string) {
    this.selectedBank = selected;
  }
  public selectMethod(selected: string) {
    this.selectedMethod = selected;
  }
  public resetPage(){
    window.location.reload();
  }

  public reset(){
    this.selectedApproach = 'None';
    this.selectedMethod = 'None';
    this.selectedError = '';

    this.loadGraph();
  }




}
