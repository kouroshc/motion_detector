$(document).ready(function () {
    console.log("asds")
    var options2 = {
        chart: {
            height: 350, type: 'line', animations: {
                enabled: true, easing: 'ease', dynamicAnimation: {
                    speed: 1000
                }
            }, toolbar: {
                show: false
            }, zoom: {
                enabled: true
            }
        }, stroke: {
            curve: 'smooth', colors: '#140152ff', width: [2, 0]
        }, plotOptions: {
            bar: {

                horizontal: false, borderRadius: 5, columnWidth: '30%', colors: {
                    ranges: [{
                        from: 0, to: 100, color: 'rgba(20,1,82,0.47)'
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
            }, tickAmount: 4, floating: true,

            labels: {
                style: {
                    colors: '#140152ff',
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
            }, fixed: {
                enabled: false, position: 'topRight'
            }, shared: true

        }, grid: {
            column: {
                colors: ['#140152ff', 'transparent'], opacity: 0.2
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
            text: 'در حال بارگذاری...'
        }
    };

    var chart = new ApexCharts(document.querySelector("#chart"), options2);

    chart.render();

    var url = "static/scripts/chart.json";
    $.getJSON(url, function (response) {
        console.log(response[1])
        console.log(response.Body_Angles_Chart)
        chart.updateSeries([{
            name: 'Temperature', type: 'line', data: response.Body_Angles_Chart.left_elbow_list
        }, {
            name: 'Humidity', type: 'line', data: response.Body_Angles_Chart.left_knee_list
        },]);
        humidityChart.updateSeries([55]);

    });
    $("#showHumid").click(function () {
        console.log(chart.data.seriesGoals.length)
        chart.toggleSeries('Humidity');
    });
    $("#showTemp").click(function () {
        console.log(chart.data.seriesGoals.length)
        chart.toggleSeries('Temperature');
    });

});