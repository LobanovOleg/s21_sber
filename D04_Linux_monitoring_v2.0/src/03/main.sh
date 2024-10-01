#!/bin/bash


delete_path() {
    local file_path="$1"

    if [[ -f "$file_path" ]]; then
        rm -f "$file_path"
        echo "Deleted file: $file_path"
    elif [[ -d "$file_path" ]]; then
        rm -rf "$file_path"
        echo "Deleted directory: $file_path"
    fi
}

delete_by_log_file() {
    local log_file="$1"

    if [[ ! -f "$log_file" ]]; then
        echo "Log file not found: $log_file"
        exit 1
    fi

    # Declare an associative array to store the directories
    declare -A directories

    while read -r line; do
        local file_path=$(echo "$line" | awk -F'|' '{print $2}' | awk '{print $2}')
        local parent_dir=$(dirname "$file_path")

        if [[ -e "$file_path" ]]; then
            delete_path "$file_path"
        fi

        # Add the parent directory to the associative array
        directories["$parent_dir"]=1
    done < "$log_file"

    # Remove the directories
    for dir in "${!directories[@]}"; do
        if [[ -d "$dir" ]]; then
            delete_path "$dir"
        fi
    done

    rm -f "$log_file"
}

delete_by_creation_date_and_time() {
    local start_time="$1"
    local end_time="$2"

    # Convert the start and end times to Unix timestamps
    local start_timestamp=$(date -j -f "$start_time" +%s)
    local end_timestamp=$(date -j -f "$end_time" +%s)
    find $(pwd)/../02/creation_log_*.txt -type f,d -printf "%Ts|%p\n" 2>/dev/null | while read -r line; do
        local created_timestamp=$(echo "$line" | awk -F'|' '{print $1}')
        local file_path=$(echo "$line" | awk -F'|' '{print $2}')

        if [[ "$created_timestamp" -gt "$start_timestamp" && "$created_timestamp" -lt "$end_timestamp" ]]; then
            if [[ -e "$file_path" ]]; then
                delete_path "$file_path"
            fi
        fi
    done
}

delete_by_name_mask() {
    local name_mask="$1"
    
    find / -not \( -path /bin -prune -o -path /sbin -prune \) -type f,d -name "${name_mask}*" 2>/dev/null | while read -r file_path; do
        if [[ -e "$file_path" ]]; then
            delete_path "$file_path"
        fi
    done
}

main() {
    if [[ $# -ne 1 ]]; then
        echo "Usage: $0 <cleaning_method>"
        echo "Cleaning method: 1 (by log file), 2 (by creation date and time), 3 (by name mask)"
        exit 1
    fi

    local cleaning_method="$1"

    if [[ $cleaning_method -eq 1 ]]; then
        echo "Enter the log file path:"
        read -r log_file
        delete_by_log_file "$log_file"
        elif [[ $cleaning_method -eq 2 ]]; then
        echo "Enter the start date and time (format: YYYY-MM-DD HH:MM):"
        read -r start_time
        echo "Enter the end date and time (format: YYYY-MM-DD HH:MM):"
        read -r end_time
        delete_by_creation_date_and_time "$start_time" "$end_time"
        elif [[ $cleaning_method -eq 3 ]]; then
        echo "Enter the name mask (format: characters_date, e.g. aaazz_021121):"
        read -r name_mask
        delete_by_name_mask "$name_mask"
    else
        echo "Invalid cleaning method. Use 1, 2, or 3."
        exit 1
    fi
}

main "$@"