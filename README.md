
This code is used to generate optimal path for m drivers given a set of lat/long and origin lat/long.

There are five arguments required for executing the code.

argument1 is number of drivers available
argument2 is origin latitude
argument3 is origin longitude
argument4 is input file location
argument5 is output file location

sample execution is python calculate_path.py 25 11.552931 104.933636 locations.csv output.csv

The input file should be of two columns the first one representing latitude and the second one representing longitude

The output file will contain the two columns from the input file i.e. the latitude and longitude and in addition to that it will contain two more columns
The third column will be the driverid (driverids will start from 0..m-1) assigned to that location and the fourth column will be the pickup index for that driver of 
that location. The location index will start from 1. So if the location index is 4 it means this location is to be picked up at 4th order by the driver.


