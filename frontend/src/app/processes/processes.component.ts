import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../data.service';
import {  takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { HttpResponse } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl, SafeUrl } from '@angular/platform-browser';

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
  trustedImageUrl : SafeUrl;
  
  imageEncodedInBase64 = '';

  approaches: Approach[] = [
    {item: 'REDIRECT', viewValue: 'REDIRECT'},
    {item: 'EMBEDDED', viewValue: 'EMBEDDED'}
  ];
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

 changeApproach(data){
    console.log("Approach selected: " + data.value);
  }

  public loadGraph() {
      this.dataService.sendGetRequestForImageGraph().pipe(takeUntil(this.destroy$)).subscribe((res: HttpResponse < any[] > ) => {
        this.loadNewImageToImageViewer(JSON.stringify(res.body[0].image));
    });
  }

  public loadNewImageToImageViewer(encodedImage){
        this.imageEncodedInBase64 = encodedImage.substr(1);
        this.imageEncodedInBase64 = this.imageEncodedInBase64.slice(0, -1);
        this.trustedImageUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.imageEncodedInBase64);
  }
}


