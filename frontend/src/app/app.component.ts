import { Component } from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Process Miner';
  
  constructor(private snackBar: MatSnackBar) {}
  
  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action);
  }
}
