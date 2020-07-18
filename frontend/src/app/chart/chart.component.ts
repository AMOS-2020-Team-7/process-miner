import { Component, OnChanges, Input } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnChanges {

  @Input()data:any;

  constructor() { }

  ngOnChanges(): void {

var margin = {
        top: 15,
        right: 25,
        bottom: 30,
        left: 80
    };

    var width = 300 - margin.left - margin.right,
        height = 150 - margin.top - margin.bottom;

    var x = d3.scaleLinear().rangeRound([0, width]);
    var y = d3.scaleBand().rangeRound([height, 0]).padding(0.2);
    const colorScale = d3.scaleOrdinal().range(['#38C976', '#22B0FC']);
    //Append the svg to body
    d3.select("#chart").selectAll("*").remove();

    var svg = d3.select("#chart").append("svg")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        this.data.forEach(function(d:any){
            d.amount = +d.amount;
        });

        x.domain([0, d3.max(this.data, function(d:any) { return +(d.amount); })]);
        y.domain(this.data.map(function(d:any) { return d.bank; }));

        svg.append('g')
            .attr('class', 'grid')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x)
                .scale(x)
                .tickSize(-height))
                //.tickFormat(''))

        svg.append('g')
            .attr('class', 'grid')
            .call(d3.axisLeft(y)
                .scale(y)
                .tickSize(-width))
              //  .tickFormat(''))
        //Create or append rectangel for graph

        svg.selectAll(".bar")
            .data(this.data)
            .enter()
            .append("rect")
            .attr("class", "bar")

            .attr("x", 0)
            .attr("width", function(d:any) { return x(d.amount);})
            .attr("y", function(d:any) { return y(d.bank); })
            .attr("height", y.bandwidth())
            .attr("fill", "#0984bf")
            .on("mouseover", function() {
                d3.select(this)
                    .style("opacity", "0.5");
                d3.select(this)
                    .transition()
                    .duration(300)
                    .attr('opacity', 0.6)
                    .attr('y', (a:any) => y(a.bank) - 5)
                    .attr('height', y.bandwidth() + 10)
                    .text(function(d:any, i:any) {
                    return d[i].amount; })
              /*  line = d3.append('line')
                    .attr('id', 'limit')
                    .attr('x1', x)
                    .attr('y1', 0)
                    .attr('x2', x)
                    .attr('y2', height)
                    .attr('stroke', 'red')*/
            })

            .on("mouseout", function(d:any, i:any) {
                d3.select(this)
                    .style("opacity", "1");
                d3.select(this)
                    .transition()
                    .duration(300)
                    .attr('opacity', 1)
                    .attr('y', (a:any) => y(a.bank))
                    .attr('height', y.bandwidth())
                });


}
}
