import { Component, OnInit } from '@angular/core';

export interface Approach {
  item: string;
  viewValue: string;
}

export interface Bank {
  item: string;
  viewValue: string;
}


@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.css']
})
export class LogsComponent implements OnInit {

  approaches: Approach[] = [
    {item: 'REDIRECT', viewValue: 'REDIRECT'},
    {item: 'EMBEDDED', viewValue: 'EMBEDDED'}
  ];

  banks: Bank[] = [
    {item: 'Commerzbank', viewValue: 'Commerzbank'},
    {item: 'Sparkasse', viewValue: 'Sparkasse'}
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
