CC = gcc
FLAGS = -Werror -Wextra -Wall

LIB_MACOS = -L /usr/local/lib -lcheck
LIB_LINUX = -lcheck -lsubunit -lpthread -lrt -lm -D_GNU_SOURCE

OC = $(shell uname)
ifeq ($(OC), Darwin)
OPEN = open gcov_report/index.html
LIB = $(LIB_MACOS)
LEAK = leaks --atExit -- ./test
endif

ifeq ($(OC), Linux)
OPEN = open gcov_report/index.html
LIB = $(LIB_LINUX)
LEAK = valgrind --leak-check=full --show-leak-kinds=all -s ./test
endif

all: s21_math.a test

test: s21_math.a
	$(CC) -c $(FLAGS) test.c
	$(CC) -o tests *.o $(LIB)
	./tests

s21_math.a:
	$(CC) -c $(FLAGS) s21_fmod.c
	ar rcs s21_math.a s21*.o
	cp s21_math.a libs21_math.a

gcov_report: clean
	$(CC) -c $(FLAGS) s21_math.c --coverage
	ar rcs gcov_s21_math.a *.o

	$(CC) -c $(FLAGS) test.c
	$(CC) -o test_with_gcov test.o gcov_s21_math.a $(LIBS) -lgcov
	./test_with_gcov

	lcov -t 'gcov_report' -o gcov_report.info -c -d .
	genhtml -o gcov_report gcov_report.info
	$(OPEN)

clean:
	rm -rf *.o
	rm -rf *.a
	rm -rf tests test_with_gcov
	rm -rf *.gcno *.gcda *.info
	rm -rf gcov_report

