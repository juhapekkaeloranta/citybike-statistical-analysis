function createStationPlot(stationId) {
  resetPlot()
  var svg = d3.select("#station-plot"),
    margin = {top: 10, right: 10, bottom: 20, left: 20},
    width = svg.attr("width") - margin.left - margin.right,
    height = svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var x = d3.scaleTime().range([0, width]),
      y = d3.scaleLinear().range([height, 0]),
      z = d3.scaleOrdinal(d3.schemeCategory10);

  var line = d3.line()
      .curve(d3.curveBasis)
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.temperature); });

  d3.json("http://localhost:3001/prediction/" + stationId, function (error, data) {
    if (error) throw error;

    var parseTime = d3.utcParse("%Y-%m-%dT%H:%M:%SZ");

    data = data.map(function(row) {
      return {...row, date: parseTime(row.time)}
    })

    let predictions = data.map(row => {
      return {date: row.date, temperature: row.avlBikes}
    })

    let dataRows = [{id: "Estimates", values: predictions}, {id: "Current", values: predictions}]

    console.log(dataRows)

  x.domain(d3.extent(data, function(d) { return d.date; }));

  //set y axis min and max
  y.domain([
    0,
    Math.max(15, d3.max(dataRows, function(c) { return d3.max(c.values, function(d) { return d.temperature; }); }))
  ]);

  z.domain(dataRows.map(function(c) { return c.id; }));

  //create x-axis
  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(12).tickFormat(d3.timeFormat("%I")));

  //create y-axis
  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y).tickFormat(d3.format(".0f")))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("fill", "#000");

  var bikeData = g.selectAll(".bikeData")
      .data(dataRows)
      .enter().append("g")
        .attr("class", "bikeData");

  bikeData.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return z(d.id); });
  });
}

function dataTypeDefs(d, _, columns) {
  var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%SZ");
  d.date = parseTime(d.date);
  for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
  return d;
}

function testDataFetch(stationId) {
  console.log("testDataFetch")
  d3.json("http://localhost:3001/prediction/" + stationId, function (error, data) {
    let predictions = data.map(row => {
      return {date: row.time, temperature: row.avlBikes}
    })

    let dataRows = [{id: "Estimates", values: predictions}]

    console.log(dataRows)
  })
}

function resetPlot() {
  d3.select("#station-plot").selectAll("*").remove()
}

createStationPlot(8)