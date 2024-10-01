CC = gcc
CFLAGS = -std=c11 -Wall -Werror -pedantic -Wextra -Wfloat-equal -Wfloat-conversion -Wvla
UNITFLAGS = -lcheck
TT = tests/tests.o
OBJS = tests/edges.o tests/figure.o tests/point.o tests/points.o tests/faces.o
GCOV_FLAGS =

OS:=$(shell uname -s)
ifeq ($(OS), Darwin)
	UNITFLAGS += $(shell pkg-config --cflags --libs check)
else
	UNITFLAGS += -lsubunit -lrt -lm -lpthread
endif


.PHONY: all clean fclean test install uninstall dvi dist gcov_report style_change style_check

all: clean install

install:
	@echo "Start installation"
	@mkdir -p build
	@cd 3DViewer && qmake > /dev/null && make > /dev/null && rm -rf Makefile && rm -rf ../build/3DViewer.app && mv 3DViewer.app ../build/3DViewer.app 
	@cp -R build/3DViewer.app ~/Desktop/3DViewer.app
	@echo "┏=========================================┓"
	@echo "┃    The installation was successful.     ┃"
	@echo "┃     The project is located in the       ┃"
	@echo "┃    build folder and on the desktop.     ┃"
	@echo "┗=========================================┛"

uninstall:
	@rm -rf ~/Desktop/3DViewer.app
	@rm -rf build/3DViewer.app
	@echo "┏==================================┓"
	@echo "┃ Uninstall completed successfully ┃"
	@echo "┗==================================┛"

dvi:
	@open ../README_RUS.md

dist:
	@mkdir -p dist
	@cp -R build/3DViewer.app dist
	@cp ../README_RUS.md dist && cp ../README.md dist
	@cd dist && tar cvzf 3DViewer.tgz *
	@cd dist && rm -rf 3DViewer.app README.md README_RUS.md
	@echo "The build was successfully archived"

test: clean s21_3dviewer_test.a
	@checkmk tests/my.check > tests/tests.c
	@$(CC) tests/tests.c -L. s21_3dviewer_test.a -o test $(UNITFLAGS) -fprofile-arcs -ftest-coverage
	@./test
	@echo "┏==================================┓"
	@echo "┃  Testing completed successfully  ┃"
	@echo "┗==================================┛"

s21_3dviewer_test.a: $(OBJS)
	@ar rc s21_3dviewer_test.a $(OBJS)
	@ranlib s21_3dviewer_test.a

gcov_report: GCOV_FLAGS += --coverage
gcov_report: clean test
	@echo "┏=========================================┓"
	@echo "┃     Generating your html report ...     ┃"
	@echo "┗=========================================┛"
	@lcov -t test -o test.info -c -d . --exclude '*/tests/*' --ignore-errors source
	@genhtml --ignore-errors unmapped -o test_html test.info
	@rm -rf *.gc* tests/*.gc*
	@rm -rf *.gd* tests/*.gd*
	@open ./test_html/index.html


tests/%.o: 3DViewer/C/%.c
	@$(CC) $(CFLAGS) -c $< -o $@ $(GCOV_FLAGS) $(UNITFLAGS)

style_check:
	@echo "┏=========================================┓"
	@echo "┃  Checking your code for Google Style    ┃"
	@echo "┗=========================================┛"
	@cp ../materials/linters/.clang-format .
	@clang-format -n 3DViewer/C/*.c 3DViewer/C/*.h 3DViewer/*.cpp
	@rm ./.clang-format

style_change:
	@echo "┏=========================================┓"
	@echo "┃  Checking your code for Google Style    ┃"
	@echo "┗=========================================┛"
	@cp ../materials/linters/.clang-format .
	@clang-format -i 3DViewer/C/*.c 3DViewer/C/*.h 3DViewer/*.cpp
	@rm ./.clang-format

clean:
	@rm -rf tests/testing test_with_gcov *.gcno *.gcov 3DViewer/*.o *.gcda *.info gcov_report
	@rm -rf 3DViewer/.qmake.stash 3DViewer/*.user 3DViewer/moc_*
	@rm -rf tests/tests.c
	@rm -rf tests/*.gcno tests/*.o tests/*gcda
	@rm -rf test tests.gcda tests.gcno s21_3dviewer_test.a


fclean: clean
	@rm -rf dist ~/Desktop/3DViewer.app build test_html
