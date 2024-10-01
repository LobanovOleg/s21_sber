#!/bin/bash

source ./configuration.conf

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

color() {
    echo ""
    echo "Column 1 background = $column1_background ($num_col1)"
    echo "Column 1 font color = $column1_font_color ($num_col2)"
    echo "Column 2 background = $column2_background ($num_col3)"
    echo "Column 2 font color = $column2_font_color ($num_col4)"
}

if [ $# -ne 0 ]
then
    echo "Error, invalid nuber of argumetns."
else
    export num1=$column1_background
    export num2=$column1_font_color
    export num3=$column2_background
    export num4=$column2_font_color
    if [[ $num1 = [1-6] && $num2 = [1-6] && $num3 = [1-6] && $num4 = [1-6] ]]; then
        if [[ $num1 -eq $num2 || $num3 -eq $num4 ]]; then
            echo "Error, front and back should be different."
        else
            end='\033[0m'
            case $num1 in
                "1") col1=$white_back; num_col1='white';;
                "2") col1=$red_back; num_col1='red';;
                "3") col1=$green_back; num_col1='green';;
                "4") col1=$blue_back; num_col1='blue';;
                "5") col1=$purple_back; num_col1='purple';;
                "6") col1=$black_back; num_col1='black';;
                *) col1=$red_back; num_col1='red'; flag1="1";;
            
            esac

            case $num2 in
                "1") col2=$white_front; num_col2='white';;
                "2") col2=$red_front; num_col2='red';;
                "3") col2=$green_front; num_col2='green';;
                "4") col2=$blue_front; num_col2='blue';;
                "5") col2=$purple_front; num_col2='purple';;
                "6") col2=$black_front; num_col2='black';;
                *) col2=$blue_front; num_col2='blue'; flag2="2";;
            
            esac

            case $num3 in
                "1") col3=$white_back; num_col3='white';;
                "2") col3=$red_back; num_col3='red';;
                "3") col3=$green_back; num_col3='green';;
                "4") col3=$blue_back; num_col3='blue';;
                "5") col3=$purple_back; num_col3='purple';;
                "6") col3=$black_back; num_col3='black';;
                *) col3=$red_back; num_col3='red'; flag3="3";;
            
            esac

            case $num4 in
                "1") col4=$white_front; num_col4='white';;
                "2") col4=$red_front; num_col4='red';;
                "3") col4=$green_front; num_col4='green';;
                "4") col4=$blue_front; num_col4='blue';;
                "5") col4=$purple_front; num_col4='purple';;
                "6") col4=$black_front; num_col4='black';;
                *) col4=$blue_front; num_col4='blue'; flag4="4";;
            
            esac

            if [[ $flag1 -eq 1 ]]; then
                echo -e "Error, column1_background should be 1-6\n"
                column1_background="default"
            fi

            if [[ $flag2 -eq 2 ]]; then
                echo -e "Error, column1_font_color should be 1-6\n"
                column1_font_color="default"
            fi

            if [[ $flag3 -eq 3 ]]; then
                echo -e "Error, column2_background should be 1-6\n"
                column2_background="default"
            fi

            if [[ $flag4 -eq 4 ]]; then
                echo -e "Error, column2_font_color should be 1-6\n"
                column2_font_color="default"
            fi
            info
            color
        fi
    else 
        end='\033[0m'
            case $num1 in
                "1") col1=$white_back; num_col1='white';;
                "2") col1=$red_back; num_col1='red';;
                "3") col1=$green_back; num_col1='green';;
                "4") col1=$blue_back; num_col1='blue';;
                "5") col1=$purple_back; num_col1='purple';;
                "6") col1=$black_back; num_col1='black';;
                *) col1=$black_back; num_col1='black'; flag1="1";;
            
            esac

            case $num2 in
                "1") col2=$white_front; num_col2='white';;
                "2") col2=$red_front; num_col2='red';;
                "3") col2=$green_front; num_col2='green';;
                "4") col2=$blue_front; num_col2='blue';;
                "5") col2=$purple_front; num_col2='purple';;
                "6") col2=$black_front; num_col2='black';;
                *) col2=$white_front; num_col2='white'; flag2="2";;
            
            esac

            case $num3 in
                "1") col3=$white_back; num_col3='white';;
                "2") col3=$red_back; num_col3='red';;
                "3") col3=$green_back; num_col3='green';;
                "4") col3=$blue_back; num_col3='blue';;
                "5") col3=$purple_back; num_col3='purple';;
                "6") col3=$black_back; num_col3='black';;
                *) col3=$black_back; num_col3='black'; flag3="3";;
            
            esac

            case $num4 in
                "1") col4=$white_front; num_col4='white';;
                "2") col4=$red_front; num_col4='red';;
                "3") col4=$green_front; num_col4='green';;
                "4") col4=$blue_front; num_col4='blue';;
                "5") col4=$purple_front; num_col4='purple';;
                "6") col4=$black_front; num_col4='black';;
                *) col4=$white_front; num_col4='white'; flag4="4";;
            
            esac

            if [[ $flag1 -eq 1 ]]; then
                echo -e "Error, column1_background should be 1-6\n"
                column1_background="default"
            fi

            if [[ $flag2 -eq 2 ]]; then
                echo -e "Error, column1_font_color should be 1-6\n"
                column1_font_color="default"
            fi

            if [[ $flag3 -eq 3 ]]; then
                echo -e "Error, column2_background should be 1-6\n"
                column2_background="default"
            fi

            if [[ $flag4 -eq 4 ]]; then
                echo -e "Error, column2_font_color should be 1-6\n"
                column2_font_color="default"
            fi
            info
            color
    fi
fi