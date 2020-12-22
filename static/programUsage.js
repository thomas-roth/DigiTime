// Create chart
var ctx = document.getElementById("donutChart").getContext('2d');
var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: [],
        datasets: [{
            label: 'Spent Time',
            data: [],
            backgroundColor: [
                'rgba(255, 89, 89, 0.4)',
                'rgba(255, 172, 89, 0.4)',
                'rgba(255, 255, 89, 0.4)',
                'rgba(172, 255, 89, 0.4)',
                'rgba(89, 255, 89, 0.4)',
                'rgba(89, 255, 172, 0.4)',
                'rgba(89, 255, 255, 0.4)',
                'rgba(89, 172, 255, 0.4)',
                'rgba(89, 89, 255, 0.4)',
                'rgba(172, 89, 255, 0.4)',
                'rgba(255, 89, 255, 0.4)',
                'rgba(255, 89, 172, 0.4)'
            ],
            borderColor: [
                'rgba(255, 89, 89, 1)',
                'rgba(255, 172, 89, 1)',
                'rgba(255, 255, 89, 1)',
                'rgba(172, 255, 89, 1)',
                'rgba(89, 255, 89, 1)',
                'rgba(89, 255, 172, 1)',
                'rgba(89, 255, 255, 1)',
                'rgba(89, 172, 255, 1)',
                'rgba(89, 89, 255, 1)',
                'rgba(172, 89, 255, 1)',
                'rgba(255, 89, 255, 1)',
                'rgba(255, 89, 172, 1)'
            ],
            borderWidth: 1.5
        }]
    },
    options: {
        
        // General settings
        cutoutPercentage: 58, 
        maintainAspectRatio: true,
        responsive: true,
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
            display: true,
            position: 'right',
            // Show timeEntries of selected data in table
            onClick: showTable,
            labels: {
                fontSize: 16,
                fontColor: "#999999",
                fontFamily: "'Roboto', sans-serif",
                padding: 10
            }
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
            displayColors: true,
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
                    console.log("Tooltip data: " + elementData + " s");
                    
                    // Determine time format
                    let timeFormat;
                    if (elementData < 5 * 60) {
                        timeFormat = "s";
                    }
                    else if (elementData < 2 * 3600) {
                        timeFormat = "min";
                        elementData = Math.round(100 * elementData / 60) / 100;
                    }
                    else {
                        timeFormat = "h";
                        elementData = Math.round(100 * elementData / 3600) / 100;
                    }

                    // Build label
                    var label = "Time: " + elementData + " " + timeFormat;

                    return label;
                }
            }
        }
    }
});

// Fill chart with data
function fillChart(startTime, endTime) {
    if (endTime == null) {
        // Get default dates
        var currentDatetime1 = new Date();
        var endTime = new Date(currentDatetime1.getFullYear(), currentDatetime1.getMonth(), currentDatetime1.getDate(), 0, 0, 0);
    }
    if (startTime == null) {
        var startTime = endTime;
    }

    var startTimeString = startTime.toISOString();
    var endTimeString = endTime.toISOString();
    
    var requestUrl = "/programUsage/dataChart/" + startTimeString + "&" + endTimeString;
    $.ajax({url: requestUrl, success: function(durationEntries) {
        // Remove old data
        myChart.data.datasets[0].data = [];
        myChart.data.labels = [];
        // Add new data
        for (let i = 0; i < durationEntries.length; i++) {
            function addData(chart, label, data) {
                chart.data.labels.push(label);
                chart.data.datasets.forEach((dataset) => {
                    dataset.data.push(data);
                });
                chart.update();
            }
            addData(myChart, durationEntries[i][0], durationEntries[i][1]);
        }
    }});
}
// Fill chart on page reload (null to get default date (today))
fillChart(null, null);

// Length of previous table
var previousLength = 0;
// Onclick event for chart legend (shows table with corresponding data)
function showTable(event, legendItem) {
    var clickedData = legendItem['text'];
    
    // Request data for clicked on name
    var requestUrl = "programUsage/dataTable/" + clickedData;
    console.log("Request URL: " + requestUrl);
    $.ajax({url: requestUrl, success: function(timeEntries) {
        // Get table from id
        var table = document.getElementById('table');
        // Delete previous table
        console.log("Previous length of table: " + previousLength);
        for (let i = 0; i < previousLength; i++) {
            table.deleteRow(0);
        }
        // Create table header
        var header = table.createTHead();
        var headerRow = header.insertRow(0);
        var headerCell1 = headerRow.insertCell(0);
        headerCell1.innerHTML = "ENTRY NAME";
        var headerCell2 = headerRow.insertCell(1);
        headerCell2.innerHTML = "START TIME";
        var headerCell3 = headerRow.insertCell(2);
        headerCell3.innerHTML = "END TIME";
        var headerCell4 = headerRow.insertCell(3);
        headerCell4.innerHTML = "WINDOW NAME";
        // Create table body
        var body = table.createTBody();
        for (let i = 0; i < timeEntries.length; i++) {
            var row = body.insertRow(-1);
            var bodyCell1 = row.insertCell(0);
            bodyCell1.innerHTML = timeEntries[i][0];
            var bodyCell2 = row.insertCell(1);
            bodyCell2.innerHTML = timeEntries[i][1];
            var bodyCell3 = row.insertCell(2);
            bodyCell3.innerHTML = timeEntries[i][2];
            var bodyCell4 = row.insertCell(3);
            bodyCell4.innerHTML = timeEntries[i][3];
        }
        // Set previousLength
        previousLength = timeEntries.length + 1;
    }});
}
