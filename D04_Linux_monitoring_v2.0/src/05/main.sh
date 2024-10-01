#!/bin/bash

log_file="$(pwd)/../04/nginx_log_day_1.log"

sort_by_response_code() {
    awk '{print $4, $0}' "$log_file" | sort -n | cut -d ' ' -f2-
}

unique_ips() {
    awk '{print $1}' "$log_file" | sort -u
}

error_requests() {
    awk '($4 >= 400 && $4 < 600) {print}' "$log_file"
}

unique_ips_with_errors() {
    awk '($4 >= 400 && $4 < 600) {print $1}' "$log_file" | sort -u
}

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <option>"
    echo "Options:"
    echo "1 - Все записи отсортированы по коду ответа"
    echo "2 - Все уникальные IP-адреса, найденные в записях"
    echo "3 - Все запросы с ошибками (код ответа — 4хх или 5ххх)"
    echo "4 - Все уникальные IP, найденные среди ошибочных запросов"
    exit 1
fi

option="$1"

case "$option" in
    1) sort_by_response_code ;;
    2) unique_ips ;;
    3) error_requests ;;
    4) unique_ips_with_errors ;;
    *)
        echo "Invalid option. Choose 1, 2, 3, or 4."
        exit 1
        ;;
esac