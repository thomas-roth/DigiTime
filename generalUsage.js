// Create chart
var ctx = document.getElementById("barChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Spent Time',
            data: [],

            barPercentage: 1,
            minBarLength: 15,
            maxBarThickness: 150,
            backgroundColor: 'rgba(197, 154, 111, 0.4)',
            borderColor: 'rgba(197, 154, 111, 1)',
            borderWidth: 1.5
        }
        , {
            type: 'line',
            label: 'Average Spent Time',
            data: [],

            borderColor: 'rgba(197, 154, 111, 1)',
            fill: false,
            pointRadius: 0,
            cubicInterpolationMode: 'monotone',
            spanGaps: false,
            steppedLine: true,
        }
        ]
    },
    options: {
        // General settings
        responsive: true,
        maintainAspectRatio: false,
        // Animation settings
        responsiveAnimationDuration: 1500,
        animation: {
            easing: 'easeInOutQuint',
            animateScale: true
        },
        // Padding settings
        layout: {
            padding: {
                left: 25,
                right: 25,
                top: 25,
                bottom: 25
            }
        },
        // Legend settings
        legend: {
            display: false
        },
        // Title settings
        title: {
            display: false
        },
        // Tooltip settings
        tooltips: {
            enabled: true,
            backgroundColor: 'rgba(30, 30, 30, 0.8)',
            titleFontFamily: "'Roboto', sans-serif",
            titleFontSize: 16,
            titleFontStyle: 'bold',
            titleFontColor: '#CCCCCC',
            titleAlign: 'left',
            titleSpacing: 2,
            titleMarginBottom: 6,
            bodyFontFamily: "'Roboto', sans-serif",
            bodyFontSize: 16,
            bodyFontStyle: 'normal',
            bodyFontColor: '#CCCCCC',
            bodyAlign: 'left',
            bodySpacing: 2,
            footerFontFamily: "'Roboto', sans-serif",
            footerFontSize: 16,
            footerFontStyle: 'normal',
            footerFontColor: '#CCCCCC',
            footerAlign: 'left',
            footerSpacing: 2,
            footerMarginTop: 6,
            xPadding: 10,
            yPadding: 10,
            caretPadding: 2,
            caretSize: 7,
            cornerRadius: 5,
            displayColors: false,
            borderWidth: 0,
            callbacks: {
                title: function(tooltipItems, data) {
                    // Get index of element hovered over
                    let elementIndex = tooltipItems[0].index;
                    console.log("Tooltip index: " + elementIndex);
                    // Get name at index
                    let elementName = data.labels[elementIndex];
                    console.log("Tooltip name: " + elementName);

                    return elementName;
                },
                label: function(tooltipItem, data) {                   
                    // Get index of element hovered over
                    let elementIndex = tooltipItem.index;
                    // Get data at index
                    let elementData = data.datasets[tooltipItem.datasetIndex].data[elementIndex];
                    console.log("Tooltip data: " + elementData);
                    
                    // Determine time format
                    let timeFormat = "h";

                    // Build label
                    var label = "Time: " + elementData + " " + timeFormat;

                    return label;
                }
            }
        },
        scales: {
            xAxes: [{
                gridLines: {
                    display: true,
                    lineWidth: 0,
                    drawBorder: true,
                    zeroLineColor: 'rgba(197, 154, 111, 1)',
                    zeroLineWidth: 2,
                },
                ticks: {
                    fontColor: '#CCCCCC',
                    fontSize: 16,
                    fontStyle: 'bold',
                }
            }],
            yAxes: [{
                gridLines: {
                    display: true,
                    color: 'rgba(193, 193, 193, 0.25)',
                    drawBorder: true,
                    zeroLineColor: 'rgba(197, 154, 111, 1)',
                    zeroLineWidth: 2,
                },
                ticks: {
                    fontColor: '#CCCCCC',
                    fontSize: 16,
                    fontStyle: 'bold',
                    padding: 10
                },
                scaleLabel: {
                    display: true,
                    labelString: 'hours',
                    fontColor: '#CCCCCC',
                    fontSize: 16,
                    fontStyle: 'bold',
                }
            }]
        },
        onClick: showProgramUsage
    }
});

// Function to fill chart with data
function fillChart(startTime, endTime) {
    if (endTime == null) {
        // Get default dates
        var currentDatetime = new Date();
        var endTime = new Date(currentDatetime.getFullYear(), currentDatetime.getMonth(), currentDatetime.getDate(), 0, 0, 0);
    }
    if (startTime == null) {
        var startTime = new Date(endTime.getFullYear(), endTime.getMonth(), endTime.getDate() - 6, 0, 0, 0);
    }

    var startTimeString = startTime.toISOString();
    var endTimeString = endTime.toISOString();
    
    var requestUrl = "/generalUsage/dataChart/" + startTimeString + "&" + endTimeString;
    $.ajax({url: requestUrl, success: function(durationEntries) {
        console.log("Amount of days: " + durationEntries[0].length);
        // Remove old data
        myChart.data.datasets[0].data = [];
        myChart.data.datasets[1].data = [];
        myChart.data.labels = [];
        // Add new data
        for (let i = 0; i < durationEntries[0].length; i++) {
            function addData(chart, label, dataBar, dataAvg) {
                chart.data.labels.push(label);
                chart.data.datasets[0].data.push(dataBar);
                chart.data.datasets[1].data.push(dataAvg);
                chart.update();
            }

            addData(myChart, durationEntries[0][i][0], durationEntries[0][i][1], durationEntries[1][0][0]);
        }
    }});
}
// Call function on page load (null to get default dates)
fillChart(null, null);

// Function to show the programUsage page with clicked on day (onClick function)
function showProgramUsage(event, activeElements) {
    var date = activeElements[0]["_model"]["label"];
    console.log("Date: " + date);

    // Open donut chart page
    var url = "/programUsage?date=" + date;
    window.open(url, "_self");
}
