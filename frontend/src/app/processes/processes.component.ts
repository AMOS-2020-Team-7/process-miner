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
  selectedApproach: string;

  approaches: Approach[] = [
    {item: 'REDIRECT', viewValue: 'REDIRECT'},
    {item: 'EMBEDDED', viewValue: 'EMBEDDED'}
  ];

 changeApproach(data){
    console.log("Approach selected: " + data.value);
  }

  constructor() {
   }

  ngOnInit(): void {
    wheelzoom(document.querySelector('img.zoom'));
  }

}
