import { Component, OnInit } from '@angular/core';

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
export class ProcessesComponent implements OnInit {

  approaches: Approach[] = [
    {item: 'REDIRECT', viewValue: 'REDIRECT'},
    {item: 'EMBEDDED', viewValue: 'EMBEDDED'}
  ];

  constructor() { }

  ngOnInit(): void {
    wheelzoom(document.querySelector('img.zoom'));
  }

}
