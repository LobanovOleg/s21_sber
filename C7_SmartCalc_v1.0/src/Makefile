TARGET = SmartCalc

CC = gcc
CFLAGS = -Wall -Werror -Wextra
OS = $(shell uname)
CONTROLLER = smart_calc_controller
MODULES = $(wildcard modules/*.c)
OBJECTS = $(patsubst %.c, %.o, $(MODULES))
OS = $(shell uname)

ifeq ($(OS), Darwin)
LDLIBS = -L /usr/local/lib -lcheck
OPEN = open ./test_with_gcov_html/index.html
endif

ifeq ($(OS), Linux)
LDLIBS = -lcheck_pic -pthread -lrt -lm -lsubunit
OPEN = open ./test_with_gcov_html/index.html
endif


all: clean install

install:
	@echo "Start installation"
	@mkdir -p build
	@cd view && qmake && make && make clean && rm -rf Makefile && mv S21_SmartCalc_GUI.app ../build/$(TARGET).app
	@cp -R build/$(TARGET).app ~/Desktop/$(TARGET).app
	@echo "┏=========================================┓"
	@echo "┃    The installation was successful.     ┃"
	@echo "┃     The project is located in the       ┃"
	@echo "┃    build folder and on the desktop.     ┃"
	@echo "┗=========================================┛"

uninstall:
	@rm -rf ~/Desktop/SmartCalc.app build
	@echo "┏==================================┓"
	@echo "┃ Uninstall completed successfully ┃"
	@echo "┗==================================┛"

dvi:
	@open ../README_RUS.md

dist:
	@mkdir -p dist
	@cp -R build/$(TARGET).app dist
	@cp ../README_RUS.md dist && cp ../README.md dist
	@cd dist && tar cvzf $(TARGET)_v1.0.tgz *
	@cd dist && rm -rf $(TARGET).app README.md README_RUS.md
	@echo "The build was successfully archived"

smart_calc.a:
	@$(CC) -c $(CFLAGS) smart_calc_controller.c mechanic/*.c
	@ar rc smart_calc.a *.o
	@ranlib smart_calc.a

test: smart_calc.a
	@$(CC) $(CFLAGS) test_calc.c -o test_calc *.o $(LDLIBS)
	@echo "┏================================┓"
	@echo "┃     		Testing...	 ┃"
	@echo "┗================================┛"
	./test_calc
	@rm *.o

gcov_report: clean
	@echo "┏=========================================┓"
	@echo "┃     Generating your html report ...     ┃"
	@echo "┗=========================================┛"
	@$(CC) smart_calc_controller.c mechanic/*.c test_calc.c -lcheck -o gcov_report --coverage -lcheck -lm
	@./gcov_report
	@rm -rf *test*.gc*
	@gcov *.c
	@lcov -d . -o gcov_report.info -c
	@genhtml -o report gcov_report.info
	@open report/index.html
	@rm -rf test_calc test_with_gcov *.gcno *.gcov *.o *.a *.gcda *.info gcov_report

style_check:
	@echo "┏=========================================┓"
	@echo "┃  Checking your code for Google Style    ┃"
	@echo "┗=========================================┛"
	@cp ../materials/linters/.clang-format .
	@clang-format -n *.c *.h **/*.c **/*.h **/*.cpp
	@rm ./.clang-format

style_change:
	@echo "┏=========================================┓"
	@echo "┃  Changing your code for Google Style    ┃"
	@echo "┗=========================================┛"
	@cp ../materials/linters/.clang-format .
	@clang-format -i *.c *.h **/*.c **/*.h **/*.cpp
	@rm ./.clang-format

clean:
	@rm -rf test_calc test_with_gcov *.gcno *.gcov *.o *.a *.gcda *.info gcov_report

fclean: clean
	@rm -rf dist ~/Desktop/$(TARGET).app report build