#!/bin/bash

COUNTER_SUCCESS=0
COUNTER_FAIL=0
DIFF_RES=""
TEST_FILE="bytes.txt"

for var in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
do
          TEST1="$var $TEST_FILE"
          echo "$TEST1"
          ./s21_cat $TEST1 > 1.txt
          cat $TEST1 > 2.txt
          DIFF_RES="$(diff -s 1.txt 2.txt)"
          if [ "$DIFF_RES" == "Files 1.txt and 2.txt are identical" ]
            then
              (( COUNTER_SUCCESS++ ))
              echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[32msuccess\033[0m cat $TEST1"
            else
              (( COUNTER_FAIL++ ))
              echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[31mfail\033[0m cat $TEST1"
          fi
          rm 1.txt 2.txt
done

for var in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
do
  for var2 in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
  do
        if [ $var != $var2 ]
        then
          TEST1="$var $var2 $TEST_FILE"
          echo "$TEST1"
          ./s21_cat $TEST1 > 1.txt
          cat $TEST1 > 2.txt
          DIFF_RES="$(diff -s 1.txt 2.txt)"
          if [ "$DIFF_RES" == "Files 1.txt and 2.txt are identical" ]
            then
              (( COUNTER_SUCCESS++ ))
              echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[32msuccess\033[0m cat $TEST1"
            else
              (( COUNTER_FAIL++ ))
              echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[31mfail\033[0m cat $TEST1"
          fi
          rm 1.txt 2.txt
        fi
  done
done

for var in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
do
  for var2 in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
  do
      for var3 in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
      do
        if [ $var != $var2 ] && [ $var2 != $var3 ] && [ $var != $var3 ]
        then
          TEST1="$var $var2 $var3 $TEST_FILE"
          echo "$TEST1"
          ./s21_cat $TEST1 > 1.txt
          cat $TEST1 > 2.txt
          DIFF_RES="$(diff -s 1.txt 2.txt)"
          if [ "$DIFF_RES" == "Files 1.txt and 2.txt are identical" ]
            then
              (( COUNTER_SUCCESS++ ))
              echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[32msuccess\033[0m cat $TEST1"
            else
              (( COUNTER_FAIL++ ))
              echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[31mfail\033[0m cat $TEST1"
          fi
          rm 1.txt 2.txt

        fi
      done
  done
done

for var in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
do
  for var2 in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
  do
      for var3 in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
      do
          for var4 in -b -e -n -s -t -v # -E -T --number-nonblank --number --squeeze-blank
          do
            if [ $var != $var2 ] && [ $var2 != $var3 ] && [ $var != $var3 ] && [ $var != $var4 ] && [ $var2 != $var4 ] && [ $var3 != $var4 ]
            then
              TEST1="$var $var2 $var3 $var4 $TEST_FILE"
              echo "$TEST1"
              ./s21_cat $TEST1 > 1.txt
              cat $TEST1 > 2.txt
              DIFF_RES="$(diff -s 1.txt 2.txt)"
              if [ "$DIFF_RES" == "Files 1.txt and 2.txt are identical" ]
                then
                  (( COUNTER_SUCCESS++ ))
                  echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[32msuccess\033[0m cat $TEST1"
                else
                  (( COUNTER_FAIL++ ))
                  echo "\033[31m$COUNTER_FAIL\033[0m/\033[32m$COUNTER_SUCCESS\033 \033[31mfail\033[0m cat $TEST1"
              fi
              rm 1.txt 2.txt

            fi
          done
      done
  done
done

echo "\033[32mSUCCESS: $COUNTER_SUCCESS\033[0m"
echo "\033[31mFAIL: $COUNTER_FAIL\033[0m"