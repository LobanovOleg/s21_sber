#!/bin/bash

user=$(whoami)

generate_name() {
    local chars="$1"
    local min_length=5
    local name=""

    for ((i=0; i<$min_length; i++)); do
        name="${name}${chars:$((RANDOM % ${#chars})):1}"
    done

    echo "${name}"
}

create_folders_and_files() {
    local folder_chars="$1"
    local file_chars="$2"
    local ext_chars="${file_chars:0:3}"
    local file_size_mb="$3"
    local log_file="$4"
    local date_suffix=$(date '+%d%m%y')

    for ((i=0; i<100; i++)); do
    

        local folder_name="$(generate_name "$folder_chars")_${date_suffix}"
        local folder_path="/Users/lowban/Desktop/DO4_LinuxMonitoring_v2.0-1/src/02/${folder_name}"
        mkdir -p "$folder_path"

        local num_files=$((RANDOM % 100 + 1))

        for ((j=0; j<$num_files; j++)); do
        

            local file_name="$(generate_name "$file_chars")_${date_suffix}"
            local file_ext="$(generate_name "$ext_chars")"
            local file_path="${folder_path}/${file_name}.${file_ext}"

            fallocate -l "${file_size_mb}M" "$file_path"
            echo "$(date '+%Y-%m-%d %H:%M:%S') | Created: ${file_path} | Size: ${file_size_mb}M" >> "$log_file"
        done
    done
}

main() {
    if [[ $# -ne 3 ]]; then
        echo "Usage: $0 <folder_chars> <file_chars> <file_size_mb>"
        exit 1
    fi

    local folder_chars="$1"
    local file_chars="$2"
    local file_size_mb="$3"

    if [[ $file_size_mb -gt 100 ]]; then
        echo "File size should not exceed 100MB."
        exit 1
    fi

    local log_file="/Users/lowban/Desktop/DO4_LinuxMonitoring_v2.0-1/src/02/creation_log_$(date '+%d%m%y').txt"
    echo "$log_file"
    local start_time=$(date '+%Y-%m-%d %H:%M:%S')
    local start_seconds=$(date +%s)

    create_folders_and_files "$folder_chars" "$file_chars" "$file_size_mb" "$log_file"

    local end_time=$(date '+%Y-%m-%d %H:%M:%S')
    local end_seconds=$(date +%s)
    local total_time=$((end_seconds - start_seconds))

    echo "Start time: $start_time" >> "$log_file"
    echo "End time: $end_time" >> "$log_file"
    echo "Total running time: ${total_time} seconds" >> "$log_file"

    echo "Start time: $start_time"
    echo "End time: $end_time"
    echo "Total running time: ${total_time} seconds"
}

main "$@"