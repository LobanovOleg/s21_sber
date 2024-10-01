GCC = gcc -Wall -Werror -Wextra -std=c11
FLAG_O_TEST = -o s21_test
FLAG_C = -c
FLAG_GCOV = --coverage

CLEAN_FILES = *.o *.out *.a *.gcno *.gcda test *.html *.gcov *.css
C_FILES = s21_*.c
OBJ_FILES = s21_*.o
TEST_C = test.c
TEST_O = test.o
GCOV_FILES = *.gcda

all: clean s21_string.a

clean:
	rm -rf $(CLEAN_FILES)

s21_string.a:
	$(GCC) $(FLAG_C) $(C_FILES)
	ar rc s21_string.a $(OBJ_FILES)
	ranlib s21_string.a
	rm $(OBJ_FILES)

test: clean s21_string.a
	$(GCC) $(FLAG_C) $(TEST_C)
	ar rc suite_tests.a $(TEST_O)
	ranlib suite_tests.a
	$(GCC) $(FLAG_GCOV) $(FLAG_O) s21_string.a suite_tests.a $(C_FILES) -lcheck -o test
	./test

gcov_report: test
	gcov $(GCOV_FILES)
	gcovr --html-details -o report.html

style_test: clean
	clang-format -n *.c *.h
