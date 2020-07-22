import { Component, Input, OnChanges } from '@angular/core';
import { graphviz } from 'd3-graphviz';

@Component({
  selector: 'app-graph-display',
  templateUrl: './graph-display.component.html',
  styleUrls: ['./graph-display.component.css']
})
export class GraphDisplayComponent implements OnChanges {

  @Input() dotString: string;
  @Input() width: string;
  @Input() height: string;

  constructor() { }

  ngOnChanges(): void {
    graphviz('#graph')
      .width(parseInt(this.width, 10))
      .height(parseInt(this.height, 10))
      .fit(true)
      .renderDot(this.dotString);
  }
}
