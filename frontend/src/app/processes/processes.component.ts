import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../data.service';
import {  takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { HttpResponse } from '@angular/common/http';

declare const wheelzoom: any;

export interface Approach {
  item: string;
  viewValue: string;
}

@Component({
  selector: 'app-processes',
  templateUrl: './processes.component.html',
  styleUrls: ['./processes.component.css']
})
export class ProcessesComponent implements OnInit, OnDestroy {
  
  selectedApproach: string;
  destroy$: Subject<boolean> = new Subject<boolean>();

  approaches: Approach[] = [
    {item: 'REDIRECT', viewValue: 'REDIRECT'},
    {item: 'EMBEDDED', viewValue: 'EMBEDDED'}
  ];

  constructor(private dataService: DataService) {
  }

  ngOnInit(): void {
    wheelzoom(document.querySelector('img.zoom'));
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    // Unsubscribe from the subject
    this.destroy$.unsubscribe();
  }

 changeApproach(data){
    console.log("Approach selected: " + data.value);
  }

  public loadGraph() {
      this.dataService.sendGetRequestForImageGraph().pipe(takeUntil(this.destroy$)).subscribe((res: HttpResponse < any[] > ) => {
        console.log(res);
    });
  }

}

