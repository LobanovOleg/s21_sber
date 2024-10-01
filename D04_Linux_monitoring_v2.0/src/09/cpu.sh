#!/bin/bash

cpu() {
	echo "# HELP cpu_used_in_percent The total CPU used as percent value" >> /var/www/html/metrics/index.html
	echo "# TYPE cpu_used_in_percent gauge" >> /var/www/html/metrics/index.html
	echo "cpu_used_in_percent $(ps -eo pcpu | awk '{s+=$1} END {print s}')" >> /var/www/html/metrics/index.html
}