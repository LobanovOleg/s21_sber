CC = gcc -Wall -Wextra -Werror
GCOVFLAGS = -L. --coverage
OS = $(shell uname)

ifeq ($(OS), Linux)
	FLAGS = -lcheck -pthread -lrt -lm -lsubunit
else
	FLAGS = -lcheck
endif

all: s21_decimal.a

s21_decimal.a:
	$(CC) s21_is_equal.c s21_add.c s21_mul.c s21_div.c s21_sub.c s21_is_not_equal.c s21_is_less.c s21_is_less_or_equal.c s21_is_greater.c s21_is_greater_or_equal.c s21_truncate.c s21_negate.c s21_round.c s21_floor.c helpers.c s21_from_decimal_to_int.c s21_from_decimal_to_float.c s21_from_int_to_decimal.c s21_from_float_to_decimal.c -c
	ar r s21_decimal.a *.o
	rm *.o

test:
	$(CC) *.c $(FLAGS) -o test
	./test

gcov_report: s21_decimal.a test
	$(CC) -w *.c s21_decimal.a $(FLAGS) $(GCOVFLAGS) -o test
	./test
	lcov -t test -o test.info -c -d .
	genhtml -o test_html test.info
	open ./test_html/index.html

clean:
	rm -rf *.o *.a *.gch *.gcno *.gcna *.gcda *.info *.out test test_html 