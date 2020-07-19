import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../data.service';
import {  takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { HttpResponse } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';

declare const wheelzoom: any;

const REST_API_HN = 'http://127.0.0.1:5000/graphs/';

const ARG_APPROACH = 'approach';
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
  destroy$: Subject<boolean> = new Subject<boolean>();
  trustedImageUrl: SafeUrl;
  imageEncodedInBase64 = '';
  dotString: string;

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

    let fullPath;
    if (this.selectedGraphType === 'DFG'){
      fullPath = 'dfg/get';
    }else{
      fullPath = 'hn/get';
    }

    this.dataService.requestData<QueryResult>(REST_API_HN + fullPath, parameters).subscribe(data => {
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

  public resetPage(){
    window.location.reload();
  }

  public reset(){
    this.selectedApproach = '';
    this.selectedMethod = '';
    this.selectedGraphType = '';
    this.selectedError = '';

    this.loadGraph();
  }




}
