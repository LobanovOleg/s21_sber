CC = gcc -Wall -Wextra -Werror
GFLAGS = -L. --coverage
OS = $(shell uname)

ifeq ($(OS), Linux)
	FLAGS = -lcheck -pthread -lrt -lm -lsubunit
else
	FLAGS = -lcheck
endif

all: s21_matrix.a

s21_matrix.a:
	$(CC) helpers.c s21_calc_complements.c s21_create_matrix.c s21_determinant.c s21_eq_matrix.c s21_inverse_matrix.c s21_mult_matrix.c s21_mult_number.c s21_remove_matrix.c s21_sub_matrix.c s21_sum_matrix.c s21_transpose.c -c
	ar r s21_matrix.a *.o
	rm *.o

test:
	$(CC) *.c $(FLAGS) -o test
	./test

gcov_report: s21_matrix.a test
	$(CC) -w *.c s21_matrix.a $(FLAGS) $(GFLAGS) -o test
	./test
	lcov -t test -o test.info -c -d .
	genhtml -o test_html test.info
	open ./test_html/index.html

code_style:
	clang-format -n *.c

clean:
	rm -rf *.o *.a *.gch *.gcno *.gcda *.info *.out test test_html