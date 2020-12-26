# THIS IS DIGITIME
With the rising importance of electronic devices and social media, your digital wellbeing has never been more important than now.
Hi, I’m Thomas Roth from Germany and **this is DigiTime**; *the* website to manage your digital health and productivity.

## What is DigiTime?
Primarily, it's an automatic time tracking application for your PC. It saves the amount of time you spent on various programs in a database as soon as your computer starts, given that you made a shortcut to the EXE file and dropped that shortcut in your startup directory.

To access the collected information, the project includes a responsive and dark-mode-friendly website that visualizes your spent time in graphs and gives you the ability to time your work and your breaks.

The **homepage** consists of two “timer”-buttons (found in the navbar) and a section containing a randomly generated suggestion provided by an API for an activity in times of boredom. The first button, called Focus timer, opens up a form in the center of the page, in which you are able to input a time. The website will inform you if that time has passed, either via an alert or, if selected, an audible “ding”-sound. The second button, called Break timer, opens up a form with the same functionality as the first button, just meant for your breaks.

The page **“Program usage”** consists of a “Filters” dropdown button in the navbar, a donut chart and an at first invisible table below the chart. The donut chart displays the time you spent by splitting it up into the top 10 programs you have used. It can be filtered using the “Filters” dropdown located in the navbar, which gives you the options to filter for today’s spent time, the combined spent time of the last 7 or even the last 30 days or a custom start- and custom end-time. Clicking on one of the items in the legend of the chart will bring up a table showing all entries of the clicked-on program with timestamps and the full name of the opened window.

The page **“General usage”** consists, just like the previous page, of a “Filters” dropdown button and a chart, although this time a vertical bar chart mixed with a line chart. The bar chart displays the combined time spent each day on your PC and the line chart the average spent time for the selected timeframe. Clicking on one of the bars will redirect you to the “Program usage” page filtered for the clicked-on day. The filter options for the chart remain the same as on the page “Program usage” except for the today-filter. 

## What does the application use?
### Programming languages
DigiTime uses Python and SQLite for its time tracking application and a mix of Python, SQLite, Flask, JavaScript and CSS for its website.
### Libraries & APIs
DigiTime uses PyWin32 and PySimpleGUI for its time tracking application and Bootstrap, Chart.js, JQuery and the BoredAPI for its website.

## References
[Youtube link](https://www.youtube.com/watch?v=lGH193uL1hs)

[Github repository](https://github.com/crispyLok/DigiTime)

# This was CS50.