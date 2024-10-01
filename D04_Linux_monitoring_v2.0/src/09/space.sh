#!/bin/bash

space() {
	echo "# HELP free_hd_space_in_bytes The total number of bytes free in home directory" >> /var/www/html/metrics/index.html
	echo "# TYPE free_hd_space_in_bytes gauge" >> /var/www/html/metrics/index.html
	echo "free_hd_space_in_bytes $(df -B1 /home | awk 'NR==2{print $4}')" >> /var/www/html/metrics/index.html
}