import { Component, OnChanges, Input, Output, EventEmitter, AfterViewInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements AfterViewInit, OnChanges {

    @Output() selectOn = new EventEmitter<string>();

    @Input() chartid: string;
    @Input() data: any;
    @Input() selected: string;


  constructor() { }

  ngOnChanges(): void {
    this.drawChart();
  }

  ngAfterViewInit(): void {
    this.drawChart();
    }

  private drawChart(){
    const margin = {
        top: 15,
        right: 25,
        bottom: 30,
        left: 80
    };

    const width = 300 - margin.left - margin.right;
    const height = 150 - margin.top - margin.bottom;

    const x = d3.scaleLinear().rangeRound([0, width]);
    const y = d3.scaleBand().rangeRound([height, 0]).padding(0.2);
    const colorScale = d3.scaleOrdinal().range(['#38C976', '#22B0FC']);
    // Append the svg to body
    d3.select(`#${this.chartid}`).selectAll('*').remove();

    const svg = d3.select(`#${this.chartid}`).append('svg')
        .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    this.data.forEach((d: any) => d.amount = +d.amount);


    x.domain([0, d3.max(this.data, ((d: any) => +(d.amount)))]);
    y.domain(this.data.map((d: any) => d.bank ));

    svg.append('g')
            .attr('class', 'grid')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x)
                .scale(x)
                .tickSize(-height));

    svg.append('g')
            .attr('class', 'grid')
            .call(d3.axisLeft(y)
                .scale(y)
                .tickSize(-width));
        // Create or append rectangel for graph

    svg.selectAll('.bar')
            .data(this.data)
            .enter()
            .append('rect')
            .attr('class', 'bar')

            .attr('x', 0)
            .attr('width', ((d: any) => x(d.amount)))
            .attr('y', ((d: any) => y(d.bank)))
            .attr('height', y.bandwidth())
            .attr('fill', (d: any) => d.bank === this.selected ? '#054f72' : '#0984bf')
            .on('click', (d: any) => this.selectOn.emit(d.bank))
            .on('mouseover', function() {
                d3.select(this)
                    .style('opacity', '0.5');
                d3.select(this)
                    .transition()
                    .duration(300)
                    .attr('opacity', 0.6)
                    .attr('y', (a: any) => y(a.bank) - 5)
                    .attr('height', y.bandwidth() + 10)
                    .text((d: any, i: any) => d.amount);

            })

            .on('mouseout', function(d: any, i: any) {
                d3.select(this)
                    .style('opacity', '1');
                d3.select(this)
                    .transition()
                    .duration(300)
                    .attr('opacity', 1)
                    .attr('y', (a: any) => y(a.bank))
                    .attr('height', y.bandwidth());
                });

}
}

