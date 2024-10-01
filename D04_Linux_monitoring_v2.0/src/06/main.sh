#!/bin/bash

if [ $# != 0 ]
then
    echo "Invalid number of arguments (should be 0)"
else
    goaccess $(pwd)/../04/nginx_log_day_*.log --log-format='%h %^ %^ %s "%r" %d "%R" "%u"' --date-format=%Y-%m-%d --time-format=%T -o report.html
    open report.html
fi