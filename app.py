from flask import Flask, render_template, jsonify
import sqlite3

# Configure application
app = Flask(__name__)

# Constants for subjects
global subject1
global subject2
global subject3
global subject4
global defaultSubject
subject1 = "GBI"
subject2 = "LA1"
subject3 = "Proggen 1"
subject4 = "Proggen 2"
defaultSubject = "no subject"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/programUsage")
def programUsage():
    # = Overview of program usage
    return render_template("programUsage.html")

@app.route("/programUsage/dataChart/<startTime>&<endTime>")
def programDataChart(startTime, endTime):
    db = sqlite3.connect("digitalWellbeing.db")
    dbCursor = db.cursor()

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
    db = sqlite3.connect("digitalWellbeing.db")
    dbCursor = db.cursor()

    # Get the rows which match the searched entryName from the timeEntries table
    if searchedEntryName == "other":
        timeEntries = dbCursor.execute('').fetchall()
    else:
        timeEntries = dbCursor.execute('SELECT entryName, strftime("%H:%M:%S %d/%m/%Y",startTime) AS startTimeText, strftime("%H:%M:%S %d/%m/%Y",endTime) AS endTimeText, windowName ' +
            'FROM timeEntries WHERE entryName = ? ORDER BY startTime DESC', (searchedEntryName, )).fetchall()

    return jsonify(timeEntries)

@app.route("/generalUsage")
def generalUsage():
    # = Overview of general usage
    return render_template("generalUsage.html")

@app.route("/generalUsage/dataChart/<startTime>&<endTime>")
def generalDataChart(startTime, endTime):
    db = sqlite3.connect("digitalWellbeing.db")
    dbCursor = db.cursor()

    # Get the combined time spent each day on subject1 for a selected time frame from the table
    durationEntries_subject1 = dbCursor.execute('SELECT date, ? as subject, IFNULL(SUM(time), 0) AS time' +
        ' FROM' +
        ' (' +
        ' 	SELECT DATE(startTime) AS date, ROUND(CAST(SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS REAL) / 3600, 2) AS time' +
        ' 	FROM timeEntries' +
        ' 	WHERE DATE(startTime) >= DATE(?, "localtime")' +
        '   AND' +
        '   DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        '   AND' +
        '   subject = ?' +
        ' 	GROUP BY DATE(startTime)' +
        ' 	UNION ALL' +
        ' 	SELECT DATE(?, "-" || CAST(number AS STRING) || " days", "localtime") AS date, null AS time' +
        ' 	FROM number' +
        ' 	WHERE number < (julianday(DATE(?, "+1 days", "localtime")) - julianday(DATE(?, "localtime")))' +
        ' )' +
        ' GROUP BY date', (subject1, startTime, endTime, subject1, endTime, endTime, startTime)).fetchall()

    # Get the combined time spent each day on subject2 for a selected time frame from the table
    durationEntries_subject2 = dbCursor.execute('SELECT date, ? as subject, IFNULL(SUM(time), 0) AS time' +
        ' FROM' +
        ' (' +
        ' 	SELECT DATE(startTime) AS date, ROUND(CAST(SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS REAL) / 3600, 2) AS time' +
        ' 	FROM timeEntries' +
        ' 	WHERE DATE(startTime) >= DATE(?, "localtime")' +
        '   AND' +
        '   DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        '   AND' +
        '   subject = ?' +
        ' 	GROUP BY DATE(startTime)' +
        ' 	UNION ALL' +
        ' 	SELECT DATE(?, "-" || CAST(number AS STRING) || " days", "localtime") AS date, null AS time' +
        ' 	FROM number' +
        ' 	WHERE number < (julianday(DATE(?, "+1 days", "localtime")) - julianday(DATE(?, "localtime")))' +
        ' )' +
        ' GROUP BY date', (subject2, startTime, endTime, subject2, endTime, endTime, startTime)).fetchall()

    # Get the combined time spent each day on subject3 for a selected time frame from the table
    durationEntries_subject3 = dbCursor.execute('SELECT date, ? as subject, IFNULL(SUM(time), 0) AS time' +
        ' FROM' +
        ' (' +
        ' 	SELECT DATE(startTime) AS date, ROUND(CAST(SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS REAL) / 3600, 2) AS time' +
        ' 	FROM timeEntries' +
        ' 	WHERE DATE(startTime) >= DATE(?, "localtime")' +
        '   AND' +
        '   DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        '   AND' +
        '   subject = ?' +
        ' 	GROUP BY DATE(startTime)' +
        ' 	UNION ALL' +
        ' 	SELECT DATE(?, "-" || CAST(number AS STRING) || " days", "localtime") AS date, null AS time' +
        ' 	FROM number' +
        ' 	WHERE number < (julianday(DATE(?, "+1 days", "localtime")) - julianday(DATE(?, "localtime")))' +
        ' )' +
        ' GROUP BY date', (subject3, startTime, endTime, subject3, endTime, endTime, startTime)).fetchall()

    # Get the combined time spent each day on subject4 for a selected time frame from the table
    durationEntries_subject4 = dbCursor.execute('SELECT date, ? as subject, IFNULL(SUM(time), 0) AS time' +
        ' FROM' +
        ' (' +
        ' 	SELECT DATE(startTime) AS date, ROUND(CAST(SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS REAL) / 3600, 2) AS time' +
        ' 	FROM timeEntries' +
        ' 	WHERE DATE(startTime) >= DATE(?, "localtime")' +
        '   AND' +
        '   DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        '   AND' +
        '   subject = ?' +
        ' 	GROUP BY DATE(startTime)' +
        ' 	UNION ALL' +
        ' 	SELECT DATE(?, "-" || CAST(number AS STRING) || " days", "localtime") AS date, null AS time' +
        ' 	FROM number' +
        ' 	WHERE number < (julianday(DATE(?, "+1 days", "localtime")) - julianday(DATE(?, "localtime")))' +
        ' )' +
        ' GROUP BY date', (subject4, startTime, endTime, subject4, endTime, endTime, startTime)).fetchall()

# Get the combined time spent each day on default subject for a selected time frame from the table
    durationEntries_defaultSubject = dbCursor.execute('SELECT date, ? as subject, IFNULL(SUM(time), 0) AS time' +
        ' FROM' +
        ' (' +
        ' 	SELECT DATE(startTime) AS date, ROUND(CAST(SUM(CAST ((julianday(endTime) - julianday(startTime))* 24 * 60 * 60 AS INTEGER)) AS REAL) / 3600, 2) AS time' +
        ' 	FROM timeEntries' +
        ' 	WHERE DATE(startTime) >= DATE(?, "localtime")' +
        '   AND' +
        '   DATE(endTime) < DATE(?, "+1 days", "localtime")' +
        '   AND' +
        '   (' +
        '       subject = ?' +
        '       OR' +
        '       subject is NULL' +
        '   )' +
        ' 	GROUP BY DATE(startTime)' +
        ' 	UNION ALL' +
        ' 	SELECT DATE(?, "-" || CAST(number AS STRING) || " days", "localtime") AS date, null AS time' +
        ' 	FROM number' +
        ' 	WHERE number < (julianday(DATE(?, "+1 days", "localtime")) - julianday(DATE(?, "localtime")))' +
        ' )' +
        ' GROUP BY date', (defaultSubject, startTime, endTime, defaultSubject, endTime, endTime, startTime)).fetchall()

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

    return jsonify((durationEntries_subject1, durationEntries_subject2, durationEntries_subject3, durationEntries_subject4, durationEntries_defaultSubject, averageDurationEntries))
