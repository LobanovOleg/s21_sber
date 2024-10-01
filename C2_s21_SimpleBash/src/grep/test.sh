#!/bin/bash

SUCCESS=0
FAIL=0
COUNTER=0
DIFF_RES=""

declare -a tests=(
"s test_0.txt VAR"
"for s21_grep.c Makefile VAR"
"for s21_grep.c VAR"
"-e for -e ^int s21_grep.c Makefile VAR"
"-e regex -e ^print s21_grep.c VAR -f test_ptrn.txt"
"-e while -e void s21_grep.c Makefile VAR -f test_ptrn.txt"
)

declare -a extra=(
"-n for test_1.txt test_2.txt"
"-n for test_1.txt"
"-n -e ^\} test_1.txt"
"-c -e \} test_1.txt"
"-ce ^int test_1.txt test_2.txt"
"-e ^int test_1.txt"
"-nivh = test_1.txt test_2.txt"
"-e"
"-ie INT test_5.txt"
"-echar test_1.txt test_2.txt"
"-ne = -e out test_5.txt"
"-iv int test_5.txt"
"-in int test_5.txt"
"-c -l aboba test_1.txt test_5.txt"
"-v test_1.txt -e ank"
"-noe ) test_5.txt"
"-l for test_1.txt test_2.txt"
"-o -e int test_4.txt"
"-e = -e out test_5.txt"
"-noe ing -e as -e the -e not -e is test_6.txt"
"-e ing -e as -e the -e not -e is test_6.txt"
"-c -e . test_1.txt -e '.'"
"-l for no_file.txt test_2.txt"
"-f test_3.txt test_5.txt"
)

testing()
{
     t=$(echo $@ | sed "s/VAR/$var/")
    ./s21_grep $t > 1.txt
    grep $t > 2.txt
    DIFF_RES="$(diff -s 1.txt 2.txt)"
    (( COUNTER++ ))
    if [ "$DIFF_RES" == "Files 1.txt and 2.txt are identical" ]
    then
      (( SUCCESS++ ))
      echo "\033[31m$FAIL\033[0m/\033[32m$SUCCESS\033[0m/$COUNTER \033[32msuccess\033[0m grep $t"
    else
      (( FAIL++ ))
      echo "\033[31m$FAIL\033[0m/\033[32m$SUCCESS\033[0m/$COUNTER \033[31mfail\033[0m grep $t"
    fi
}

# спецефические тесты
for i in "${extra[@]}"
do
    var="-"
    testing $i
done

# 1 параматр 

for var1 in v c l n h o
do
    for i in "${tests[@]}"
    do
        var="-$var1"
        testing $i
    done
done

# 2 параметра
for var1 in v c l n h o
do
    for var2 in v c l n h o
    do
        if [ $var1 != $var2 ]
        then
            for i in "${tests[@]}"
            do
                var="-$var1 -$var2"
                testing $i
            done
        fi
    done
done

# 3 параметра
for var1 in v c l n h o
do
    for var2 in v c l n h o
    do
        for var3 in v c l n h o
        do
            if [ $var1 != $var2 ] && [ $var2 != $var3 ] && [ $var1 != $var3 ]
            then
                for i in "${tests[@]}"
                do
                    var="-$var1 -$var2 -$var3"
                    testing $i
                done
            fi
        done
    done
done

# 2 сдвоенных параметра
for var1 in v c l n h o
do
    for var2 in v c l n h o
    do
        if [ $var1 != $var2 ]
        then
            for i in "${tests[@]}"
            do
                var="-$var1$var2"
                testing $i
            done
        fi
    done
done

# 3 строенных параметра
for var1 in v c l n h o
do
    for var2 in v c l n h o
    do
        for var3 in v c l n h o
        do
            if [ $var1 != $var2 ] && [ $var2 != $var3 ] && [ $var1 != $var3 ]
            then
                for i in "${tests[@]}"
                do
                    var="-$var1$var2$var3"
                    testing $i
                done
            fi
        done
    done
done

echo "\033[31mFAIL: $FAIL\033[0m"
echo "\033[32mSUCCESS: $SUCCESS\033[0m"
echo "ALL: $COUNTER"
