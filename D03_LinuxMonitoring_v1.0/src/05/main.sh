#!/bin/bash

start=`date +%s`

counting_folders() {
    echo "Total number of folders (including all nested ones) = $(find $1 -type d | wc -l)"
    echo "TOP 5 folders of maximum size arranged in descending order (path and size):"
    du -h $1 2>/dev/null | sort -hr | head -5 | awk 'BEGIN{i=1}{printf "%d - %s, %s\n", i, $2, $1; i++}'
}

counting_files() {
    echo "Total number of files = $(ls -laR $1 2>/dev/null | grep ^- | wc -l)"
    echo "Number of:"
    echo "Configuration files (with the .conf extension) = $(find $1 2>/dev/null -type f -name "*.conf" | wc -l | awk '{print $1}')"
    echo "Text files = $(find $1 2>/dev/null -type f -name "*.txt" | wc -l | awk '{print $1}')"
    echo "Executable files = $(find $1 2>/dev/null -type f -executable | wc -l | awk '{print $1}')"
    echo "Log files (with the extension .log) = $(find $1 2>/dev/null -type f -name "*.log" | wc -l | awk '{print $1}')"
    echo "Archive files = $(find $1 2>/dev/null -type f -name "*.zip" -o -name "*.7z" -o -name "*.tar" -o -name "*.rar" | wc -l | awk '{print $1}')"
    echo "Symbolic links = $(find $1 2>/dev/null -type l | wc -l | awk '{print $1}')"
    echo "TOP 10 files of maximum size arranged in descending order (path, size and type):"
    for x in {1..10}
    do
        file=$(find $1 2>/dev/null -type f -exec du -h {} + | sort -rh | head -10 | sed "${x}q;d")
        if ! [[ -z $file ]]; then
            echo "$x - $(echo $file | awk '{print $2}'), $(echo $file | awk '{print $1}'), $(echo $file | grep -m 1 -o -E "\.[^/.]+$" | awk -F. '{print $2}')"
        fi
    done
}

executable_files() {
    echo "TOP 10 executable files of the maximum size arranged in descending order (path, size and MD5 hash of file)"
    for x in {1..10}
    do
        file=$(find $1 2>/dev/null -type f -executable -exec du -h {} + | sort -rh | head -10 | sed "${x}q;d")
        if ! [[ -z $file ]]; then
            path=$(echo $file | awk '{print $2}')
            MD5=$(md5sum $path | awk '{print $1}')
            echo "$x - $(echo $file | awk '{print $2}'), $(echo $file | awk '{print $1}'), $(echo $MD5)"
        fi
    done
}

counting_time() {
    end=`date +%s`
    echo "Script execution time (in seconds) = $(($end-$1))"
}

if [[ $# == 1 ]]; then
    if [[ -d $1 ]]; then
        if [[ ${1: -1} = "/" ]]; then
            counting_folders $1
            counting_files $1
            executable_files $1
            counting_time $start
        else
            echo "Error, symbol '/'' have to be at the end of the path."
        fi
    else
        echo "Error, directory not exist."
    fi
else
    echo "Error, invalid number of arguments."
fi