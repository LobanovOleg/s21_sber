#!/bin/bash/

. ./check_input
. ./check_empty_space
. ./create_folders
. ./create_files

check_input $@


free_space=$(check_empty_space)
if [[ $free_space == "Enough free space" ]]; then

	path=$1
	num_folders=$2
	folder_names=$3
	create_folders $path $num_folders $folder_names
	num_files=$4
	file_names=$5
	file_size=$6
	create_files $num_files $file_names $file_size
else
	echo "There isn't enough free space left"
	echo "Should be over 1GB left to run the script"
fi