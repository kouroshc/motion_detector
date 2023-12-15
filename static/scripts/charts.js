$(document).ready(function () {

  var options = {
        chart: {
            height: 350, type: 'line',
            animations: {
                enabled: true, easing: 'ease', dynamicAnimation: {
                    speed: 1000
                }
            }, toolbar: {
                show: false
            }, zoom: {
                enabled: true
            }
        }, stroke: {
            curve: 'smooth', colors: '#f7fff7ff', width: [2, 0]
        }, plotOptions: {
            bar: {

                horizontal: false, borderRadius: 5, columnWidth: '30%', colors: {
                    ranges: [{
                        from: 0, to: 100, color: '#f7fff7ff'
                    }],
                }
            }
        },

        series: [], dataLabels: {

            enabled: false
        }, xaxis: {

            type: 'datetime', tickPlacement: 'on', axisBorder: {
                show: true
            }, lines: {
                show: true,
            }, axisTicks: {
                show: true
            }
        },

        yaxis: [{
            seriesName: 'Temperature', title: {
                text: "Temperature"
            }, tickAmount: 4,
            floating: true,

            labels: {
                style: {
                    colors: '#f7fff7ff',
                }, offsetY: 0, offsetX: 0,
            }, axisBorder: {
                show: true,
            }, axisTicks: {
                show: true
            }
        }, {
            opposite: true, seriesName: 'Humidity', min: 0, max: 100, title: {
                text: "Humidity"
            }
        }],

        tooltip: {

            x: {
                format: "yyyy-mm-dd hh-mm-ss ",
            }, style: {
                    colors: '#f7fff7ff'}, fixed: {
                enabled: false, position: 'topRight'
            }, shared: true

        }, grid: {
            column: {
                colors: ['#f7fff7ff', 'transparent'], opacity: 0.2
            }, xaxis: {
                lines: {
                    show: true
                }
            }, yaxis: {
                lines: {
                    offsetX: -320, show: true
                }
            }, padding: {
                left: 0
            }
        }, noData: {
            text: 'در حال بارگذاری...',
          style: {
                    colors: '#f7fff7ff'}
        }
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options);

    chart.render();

    var url = "static/scripts/chart.json";
    $.getJSON(url, function (response) {
        chart.updateSeries([{
            name: 'Temperature', type: 'line', data: response[0].Temp
        }]);
        humidityChart.updateSeries([55
        ]);

    });

});