import { environment } from './../../environments/environment';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../data.service';
import {  takeUntil } from 'rxjs/operators';
import { Subject, pipe } from 'rxjs';
import { HttpResponse } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';

declare const wheelzoom: any;

const REST_API_HN = 'graphs/hn/get';
const REST_API_DFG = 'graphs/dfg/get';
const REST_API_LR = 'logs/refresh';

const ARG_APPROACH = 'approach';
const ARG_METHOD_TYPE = 'method_type';
const ARG_BANK = 'bank';
const ARG_ERROR_TYPE = 'error_type';
const ARG_FORMAT = 'format';
const ARG_FORCE_REFRESH = 'force';

export interface Approach {
  item: string;
  viewValue: string;
}

export interface Method {
  item: string;
  viewValue: string;
}

export interface GraphType {
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
  selectedGraphType = '';
  selectedError = '';
  forceRefresh = false;
  destroy$: Subject<boolean> = new Subject<boolean>();
  trustedImageUrl: SafeUrl;
  imageEncodedInBase64 = '';
  dotString: string;
  selectedBank: string;
  spinnerWait: boolean;
  bankChartData: any = [];
  methodChartData: any = [];
  approaches: Approach[] = [
    {item: 'redirect', viewValue: 'Redirect'},
    {item: 'embedded', viewValue: 'Embedded'}
  ];
  graphTypes: GraphType[] = [
    {item: 'HN', viewValue: 'Heuristic Net'},
    {item: 'DFG', viewValue: 'Directly-Follows Graph'}
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
    this.spinnerWait = false;
    // Unsubscribe from the subject
    this.destroy$.unsubscribe();
  }

  private getGraphParameters() {
    const parameters = {};
    parameters[ARG_FORMAT] = 'dot';
    if (this.selectedApproach) {
      parameters[ARG_APPROACH] = this.selectedApproach;
    }
    if (this.selectedMethod) {
      parameters[ARG_METHOD_TYPE] = this.selectedMethod;
    }
    if (this.selectedBank) {
      parameters[ARG_BANK] = this.selectedBank;
    }
    if (this.selectedError) {
      parameters[ARG_ERROR_TYPE] = this.selectedError;
    }
    return parameters;
  }

  public loadGraph() {
    this.spinnerWait = true;
    const parameters = this.getGraphParameters();

    let url;
    if (this.selectedGraphType === 'DFG'){
      url = this.getUrl(REST_API_DFG);
    }else{
      url = this.getUrl(REST_API_HN);
    }

    this.dataService.requestData<QueryResult>(url, parameters).pipe(takeUntil(this.destroy$)).subscribe(data => {
      this.spinnerWait = false;
      this.bankChartData = Object.entries(data.metadata.banks).map((f) => ({bank: f[0], amount: f[1]}));
      this.methodChartData = Object.entries(data.metadata.methods).map((f) => ({bank: f[0], amount: f[1]}));
      this.loadNewImageToImageViewer(data.image);
      this.loadErrors(data.metadata.errors, data.numberOfSessions);
    },
    error => {
      this.spinnerWait = false;
    });
  }

  private getUrl(endpointPath: string) {
    const host = environment.backendHost;
    const port = environment.backendPort;
    return `http://${host}:${port}/${endpointPath}`;
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
    this.selectedApproach = '';
    this.selectedMethod = '';
    this.selectedGraphType = '';
    this.selectedError = '';
    this.selectedBank = '';
    this.loadGraph();
  }

  public reloadLogs(){

    this.spinnerWait = true;
    const url = this.getUrl(REST_API_LR);
    this.dataService.requestData<QueryResult>(url, {force: this.forceRefresh}).pipe(takeUntil(this.destroy$)).subscribe(data => {
      this.spinnerWait = false;
    },
    error => {
      this.spinnerWait = false;
    });
  }

}
