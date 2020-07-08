import { Component, Input, OnChanges } from '@angular/core';
import { graphviz } from 'd3-graphviz';

@Component({
  selector: 'app-graph-display',
  templateUrl: './graph-display.component.html',
  styleUrls: ['./graph-display.component.css']
})
export class GraphDisplayComponent implements OnChanges {

  @Input() dotString: string;

  constructor() { }

  ngOnChanges(): void {
    graphviz('#graph')
      .width(1000)
      .height(1000)
      .fit(true)
      .scale(0.5)
      .renderDot(this.dotString);
  }
}
