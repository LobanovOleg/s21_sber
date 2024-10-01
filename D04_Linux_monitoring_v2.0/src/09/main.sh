#!/bin/bash

. ./cpu.sh
. ./space.sh
. ./mem.sh

if [ $# != 0 ]; then
	echo "Script takes no arguments"
	exit 1
else

	while true; do
		if [[ -f "/var/www/html/metrics/index.html" ]]; then
			rm /var/www/html/metrics/index.html
		fi
		cpu
		space
		mem
		sleep 5;
	done
fi