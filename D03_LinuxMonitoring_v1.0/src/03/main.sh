#!/bin/bash

white_front="\033[107m"
red_front="\033[41m"
green_front="\033[42m"
blue_front="\033[44m"
purple_front="\033[45m"
black_front="\033[40m"

white_back="\033[97m"
red_back="\033[31m"
green_back="\033[32m"
blue_back="\033[34m"
purple_back="\033[35m"
black_back="\033[30m"


info() { 
  echo -e $col1$col2 HOSTNAME'       ' = $col3$col4$(hostname)'                     '$end
  echo -e $col1$col2 TIMEZONE'       ' = $col3$col4$(timedatectl | awk 'NR == 4' | awk '{print $3}') UTC $(date +%-:::z)'          '$end
  echo -e $col1$col2 USER'           ' = $col3$col4$(whoami)'                      '$end
  echo -e $col1$col2 OS'             ' = $col3$col4$(cat /etc/issue | awk '{print $1,$2,$3}' | tr -s '\r\n')'           '$end
  echo -e $col1$col2 DATE'           ' = $col3$col4$(date +%d' '%B' '%Y' '%T)'     '$end
  echo -e $col1$col2 UPTIME'         ' = $col3$col4$(uptime -p | awk '{print $2,$3,$4,$5}')'                   '$end
  echo -e $col1$col2 UPTIME_SEC'     ' = $col3$col4$(cat /proc/uptime | awk '{print $1}')'                        '$end
  echo -e $col1$col2 IP'             ' = $col3$col4$(ip a | awk 'NR == 3' | awk '{print $2}')'                   '$end
  echo -e $col1$col2 MASK'           ' = $col3$col4$(ifconfig | awk 'NR == 2' | awk '{print $2}')'                     '$end
  echo -e $col1$col2 GATEWAY'        ' = $col3$col4$(ip route | grep default | awk '{print $3}')'                      '$end
  echo -e $col1$col2 RAM_TOTAL'      ' = $col3$col4$(free --mega | awk 'NR == 2' | awk '{printf "%.3f GB", $2 / 1000}')'                      '$end
  echo -e $col1$col2 RAM_USED'       ' = $col3$col4$(free --mega | grep Mem | awk '{printf "%.3f GB", $3 / 1000}')'                      '$end
  echo -e $col1$col2 RAM_FREE'       ' = $col3$col4$(free --mega | grep Mem | awk '{printf "%.3f GB", $4 / 1000}')'                      '$end
  echo -e $col1$col2 SPACE_ROOT'     ' = $col3$col4$(df -m | awk 'NR == 3' | awk '{printf "%.2f MB", $2}')'                    '$end
  echo -e $col1$col2 SPACE_ROOT_USED = $col3$col4$(df -m | awk 'NR == 3' | awk '{printf "%.2f MB", $3}')'                    '$end
  echo -e $col1$col2 SPACE_ROOT_FREE = $col3$col4$(df -m | awk 'NR == 3' | awk '{printf "%.2f MB", $4}')'                    '$end
}

if [[ $# -ne 4 ]]; then
    echo "Error, invalid number of argumetns."
else
    if [[ $1 != [1-6] || $2 != [1-6] || $3 != [1-6] || $4 != [1-6] ]]; then
        echo "Error, invalid number from 1 to 6"
    else
        if [[ $1 -eq $2 ]] || [[ $3 -eq $4 ]]; then
            echo "Error, front and back should be different."
        else
            end="\033[0m"
            case $1 in
                "1") col1=$white_front;;
                "2") col1=$red_front;;
                "3") col1=$green_front;;
                "4") col1=$blue_front;;
                "5") col1=$purple_front;;
                "6") col1=$black_front;;
            
            esac

            case $2 in
                "1") col2=$white_back;;
                "2") col2=$red_back;;
                "3") col2=$green_back;;
                "4") col2=$blue_back;;
                "5") col2=$purple_back;;
                "6") col2=$black_back;;
            
            esac

            case $3 in
                "1") col3=$white_front;;
                "2") col3=$red_front;;
                "3") col3=$green_front;;
                "4") col3=$blue_front;;
                "5") col3=$purple_front;;
                "6") col3=$black_front;;
            
            esac

            case $4 in
                "1") col4=$white_back;;
                "2") col4=$red_back;;
                "3") col4=$green_back;;
                "4") col4=$blue_back;;
                "5") col4=$purple_back;;
                "6") col4=$black_back;;
            
            esac
            info
        fi
    fi
fi

