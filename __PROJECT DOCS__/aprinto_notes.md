
WORKFLOW:

Post received by server.
Task 1 is assigned to Celery w/ delayed action.
File Uploaded to server.
Client receives http response.

<< -- Assigned Task 1

Extract all text.
Assign Task 2 w/ delayed action.
Upload text to database.

<< -- Assigned Task 2

Extract relevant data.
Assign Task 3 w/ delayed action.
Upload data to database.

<< -- Assigned Task 3

Process Route...


--->>  TODO ON SERVER
install pdftohtml
syncdb


## Workflow for Aprinto/Apronto

All order and device updates should go to apronto.

	. from randomly generated dataset,
    	run small script to post contents to server via url requests.
    	. These requests will be timed according to the dataset and rate of increase,
            i.e., 20 seconds real time could equal 1 minute of simulated time.

    . a django application receives the post request and, via a celery task,
        . RD-pandas incorporates the new Device and Order variables,
        . distances between

    .


Google Distance API provides
https://developers.google.com/maps/documentation/distancematrix/#Introduction

pgRouting!! http://workshop.pgrouting.org/chapters/about.html
QGIS RoadGraph plugin, and more http://gis.stackexchange.com/questions/73250/how-to-calculate-distances-between-addresses-and-cities-and-coast-line


