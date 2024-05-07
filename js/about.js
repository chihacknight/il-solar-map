function format_number(val) {
    const parsed = parseInt(val);
    if (isNaN(parsed)) { return 0 }
    return parseInt(val).toLocaleString("en-US")
}

CsvToHtmlTable.init({
    csv_path: "/data/final/all_projects_summary.csv",
    element: "table-summary",
    allow_download: false,
    csv_options: {
        separator: ",",
        delimiter: '"'
    },
    datatables_options: {
        paging: false,
        info: false,
        searching: false,
        ordering: false,
    },
});

Highcharts.setOptions({
  lang: {
      thousandsSep: ','
  }
});

$.when($.get("/data/final/all_projects_summary.csv")).then(
  function (data) {
    var csvData = $.csv.toArrays(data)

    Highcharts.chart('projects-chart', {
      chart: {
        type: 'pie'
      },
      title: {
        text: 'kW installed by category'
      },
      credits: {
        enabled: false
      },
      plotOptions: {
        series: {
          allowPointSelect: true,
          cursor: 'pointer',
        }
      },
      tooltip: {
        format: '<b>{point.name}</b>: {point.y:.1f}%',
      },
      series: [
        {
          name: 'kW installed',
          colorByPoint: true,
          data: [
            {
              name: csvData[1][0],
              y: parseFloat(csvData[1][2])
            },
            {
              name: csvData[2][0],
              y: parseFloat(csvData[2][2])
            },
            {
              name: csvData[3][0],
              y: parseFloat(csvData[3][2])
            },
            {
              name: csvData[4][0],
              y: parseFloat(csvData[4][2])
            }
          ]
        }
      ]
    });
  });

  $.when($.get("/data/final/monthly-aggregate.csv")).then(
  function (data) {
      var csvData = $.csv.toArrays(data)
      csvData.shift()

      var utilitySeries = []
      var smSeries = []
      var lgSeries = []
      var csSeries = []

      // convert the first element of each array into a DateTime
      // store each series in its own array for Highcharts
      csvData.forEach(function (row) {
        var dateparts = row[0].split('-')
        row[0] = Date.UTC(dateparts[0], dateparts[1] - 1, dateparts[2])

        csSeries.push([row[0], parseInt(row[1])])
        lgSeries.push([row[0], parseInt(row[2])])
        smSeries.push([row[0], parseInt(row[3])])
        utilitySeries.push([row[0], parseInt(row[4])])
      })

      console.log(csvData)

      Highcharts.chart('timeseries-chart', {
        chart: {
            type: 'area',
            height: 500,
        },
        credits: {
          enabled: false
        },
        title: {
            text: 'Cumulative kW of solar installed over time'
        },
        xAxis: {
            type: 'datetime',
            min: Date.UTC(2018, 0, 1),
            labels: {
              format: '{value:%b %Y}'
            }
        },
        yAxis: {
            title: {
                text: 'kilowatts'
            }
        },
        tooltip: {
            shared: true,
            valueSuffix: ' kW',
        },
        plotOptions: {
            area: {
              stacking: "normal",
                marker: {
                    enabled: false,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [{
          name: "Utility",  
          data: utilitySeries
        }, {
          name: "Small DG",  
          data: smSeries
        }, {
          name: "Large DG",  
          data: lgSeries
        }, {
          name: "Community Solar",  
          data: csSeries
        }]
    });
  });