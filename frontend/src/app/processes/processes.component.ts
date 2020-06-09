import { Component, OnInit } from '@angular/core';

declare const wheelzoom: any;

@Component({
  selector: 'app-processes',
  templateUrl: './processes.component.html',
  styleUrls: ['./processes.component.css']
})
export class ProcessesComponent implements OnInit {



  constructor() { }

  ngOnInit(): void {
    wheelzoom(document.querySelector('img.zoom'));
  }

}
