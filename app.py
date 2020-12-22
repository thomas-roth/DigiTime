from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime
import json

# Configure application
app = Flask(__name__)

# Connect to the database
db = sqlite3.connect('digitalWellbeing.db')
dbCursor = db.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/programUsage")
def programUsage():
    # = Overview of program usage
    return render_template("programUsage.html")

@app.route("/programUsage/dataChart/<startTime>&<endTime>")
def programDataChart(startTime, endTime):
    # Get the whole durationEntries view (in seconds)
    durationEntries = dbCursor.execute(' SELECT entryName, duration, "sec" AS format' +
        ' FROM' +
        ' (' +
        ' 		SELECT *' +
        ' 		FROM' +
        ' 		(' +
        ' 			SELECT 1 AS log, entryName, SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS duration' +
        ' 			FROM timeEntries' +
        ' 			WHERE DATE(startTime) >= DATE(?, "localtime")' +
        ' 				AND' +
        ' 				DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        ' 			GROUP BY entryName' +
        ' 			ORDER BY duration DESC LIMIT 10' +
        ' 		)' +
        ' 	UNION' +
        ' 		SELECT 2 AS log, "other" as entryName, SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 As INTEGER)) AS duration' +
        ' 		FROM timeEntries' +
        ' 		WHERE DATE(startTime) >= DATE(?, "localtime")' +
        ' 					AND' +
        ' 					DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        ' 		AND entryName NOT IN' +
        ' 		(' +
        ' 			SELECT entryName' +
        ' 			FROM' +
        ' 			(' +
        ' 				SELECT entryName, SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS duration' +
        ' 				FROM timeEntries' +
        ' 				WHERE DATE(startTime) >= DATE(?, "localtime")' +
        ' 					AND' +
        ' 					DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        ' 				GROUP BY entryName' +
        ' 				ORDER BY duration DESC LIMIT 10' +
        ' 			)' +
        ' 		)' +
        ' 	ORDER BY log, duration DESC' +
        ' )', (startTime, endTime, startTime, endTime, startTime, endTime)).fetchall()

    return jsonify(durationEntries)

@app.route("/programUsage/dataTable/<searchedEntryName>")
def programDataTable(searchedEntryName):
    # Get the rows which match the searched entryName from the timeEntries table
    if searchedEntryName == "other":
        timeEntries = dbCursor.execute('').fetchall()
    else:
        timeEntries = dbCursor.execute('SELECT entryName, strftime("%H:%M:%S %d/%m/%Y",startTime) AS startTimeText, strftime("%H:%M:%S %d/%m/%Y",endTime) AS endTimeText, windowName FROM timeEntries WHERE entryName = ? ORDER BY startTime DESC', (searchedEntryName, )).fetchall()

    return jsonify(timeEntries)

@app.route("/generalUsage")
def generalUsage():
    # = Overview of general usage
    return render_template("generalUsage.html")

@app.route("/generalUsage/dataChart/<startTime>&<endTime>")
def generalDataChart(startTime, endTime):
    # Get the combined time spent each day for a selected time frame from the table
    durationEntries = dbCursor.execute('SELECT date, IFNULL(SUM(time), 0) AS time' +
        ' FROM' +
        ' (' +
        ' 	SELECT DATE(startTime) AS date, ROUND(CAST(SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS REAL) / 3600, 2) AS time' +
        ' 	FROM timeEntries' +
        ' 	WHERE DATE(startTime) >= DATE(?, "localtime")' +
        '   AND' +
        '   DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        ' 	GROUP BY DATE(startTime)' +
        ' 	UNION ALL' +
        ' 	SELECT DATE(?, "-" || CAST(number AS STRING) || " days", "localtime") AS date, null AS time' +
        ' 	FROM number' +
        ' 	WHERE number < (julianday(DATE(?, "+1 days", "localtime")) - julianday(DATE(?, "localtime")))' +
        ' )' +
        ' GROUP BY date', (startTime, endTime, endTime, endTime, startTime)).fetchall()

    # Get the average amount of time spent each day
    averageDurationEntries = dbCursor.execute('SELECT ROUND(AVG(time), 2) FROM' +
        ' (	' +
        ' 	SELECT IFNULL(SUM(time), 0) AS time' +
        ' 	FROM' +
        ' 	(' +
        ' 		SELECT DATE(startTime) AS date, ROUND(CAST(SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS REAL) / 3600, 2) AS time' +
        ' 	    FROM timeEntries' +
        ' 	    WHERE DATE(startTime) >= DATE(?, "localtime")' +
        '       AND' +
        '       DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        ' 	    GROUP BY DATE(startTime)' +
        ' 	    UNION ALL' +
        ' 	    SELECT DATE(?, "-" || CAST(number AS STRING) || " days", "localtime") AS date, null AS time' +
        ' 	    FROM number' +
        ' 	    WHERE number < (julianday(DATE(?, "+1 days", "localtime")) - julianday(DATE(?, "localtime")))' +
        ' 	)' +
        ' 	GROUP BY date' +
        ' )', (startTime, endTime, endTime, endTime, startTime)).fetchall()

    return jsonify((durationEntries, averageDurationEntries))
