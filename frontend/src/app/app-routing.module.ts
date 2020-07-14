import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ProcessesComponent } from './processes/processes.component';



const routes: Routes = [
  { path: '', redirectTo: 'processes', pathMatch: 'full'},
  { path: 'home', component: HomeComponent },
  { path: 'processes', component: ProcessesComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
