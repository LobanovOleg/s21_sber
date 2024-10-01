#!/bin/bash

declare -a response_codes=("200" "201" "400" "401" "403" "404" "500" "501" "502" "503")
declare -a methods=("GET" "POST" "PUT" "PATCH" "DELETE")
declare -a user_agents=("Mozilla" "Google Chrome" "Opera" "Safari" "Internet Explorer" "Microsoft Edge" "Crawler and bot" "Library and net tool")

generate_url() {
    WORDS=(some really cool site awesome dude chicks happy interesting wonderful thing)
    DOMAIN_ZONE=(ru com biz info com org net)
    PAGE=(index omg rtfm lol asap btw p2p acab gtfo)
    
    for (( i=0; i<3; i++ ))
    do
        SITE=${SITE}${WORDS[$(( $RANDOM % 11 ))]}
    done

    echo "http://www.$SITE.${DOMAIN_ZONE[$(( $RANDOM % 7 ))]}/${PAGE[$(( $RANDOM % 9 ))]}.html"
}

for i in {1..5}; do
  log_file="nginx_log_day_${i}.log"
  touch "$log_file"
  num_entries=$((RANDOM % 901 + 100))

  for ((j = 0; j < num_entries; j++)); do
    ip="$(shuf -i 1-255 -n 1).$(shuf -i 1-255 -n 1).$(shuf -i 1-255 -n 1).$(shuf -i 1-255 -n 1)"
    response_code="${response_codes[RANDOM % ${#response_codes[@]}]}"
    method="${methods[RANDOM % ${#methods[@]}]}"
    date="$(date '+%Y-%m-%d')"
    request_url=$(generate_url)
    user_agent="${user_agents[RANDOM % ${#user_agents[@]}]}"

    echo "$ip - - $response_code \"$method $request_url HTTP/1.1\" "$date" \"-\" \"$user_agent\"" >> "$log_file"
  done
done

# Response codes
# 200: OK
# 201: Created
# 400: Bad Request
# 401: Unauthorized
# 403: Forbidden
# 404: Not Found
# 500: Internal Server Error
# 501: Not Implemented
# 502: Bad Gateway
# 503: Service Unavailable