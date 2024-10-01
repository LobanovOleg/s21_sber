.PHONY: clean uninstall dvi

CC = g++
WWW = -Wall -Wextra -Werror -std=c++17 -pedantic
FLAGS= -lgtest -lgtest_main -lpthread
PATH_TEST = ./test_model/test_model.cpp ./test_model/main.cpp ./model/smartCalculModel.cpp
PATH_APP = ./build/
APP=$(PATH_APP)Calculator.app

SOURCES = ./model/smartCalculModel.cpp \
			./controller/smartCalculModel.cpp \
			./view/main.cpp \
			./view/mainwindow.cpp \
			./view/qcustomplot.cpp \
			./view/stylehelper.cpp

HEDERS = ./model/smartCalculModel.h \
			./controller/smartCalculModel.h \
			./view/mainwindow.h \
			./view/qcustomplot.h \
			./view/stylehelper.h

all: install tests

install:
	@echo "┏================┓"
	@echo "┃  Installing... ┃"
	@echo "┗================┛"
	@mkdir $(PATH_APP)
	@cd $(PATH_APP) && qmake ../view/Calculator.pro
	@make -C $(PATH_APP)

uninstall: clean
	@echo "┏=====================┓"
	@echo "┃  Uninstalling...    ┃"
	@echo "┗=====================┛"
	@rm -rf ./build

dvi:
	@open ../README_RUS.md

dist:
	@echo "┏==========================┓"
	@echo "┃  Making an Archive...    ┃"
	@echo "┗==========================┛"
	@rm -rf Archive_SmartCalc_v2.0/
	@mkdir Archive_SmartCalc_v2.0/
	@mkdir Archive_SmartCalc_v2.0/src
	@cp ./build/Calcul.app/Contents/MacOS/Calculator* Archive_SmartCalc_v2.0/src/
	@tar cvzf Archive_SmartCalc_v2.0.tgz Archive_SmartCalc_v2.0/
	@rm -rf Archive_SmartCalc_v2.0/

tests:
	@echo "┏=====================┓"
	@echo "┃  Making tests...    ┃"
	@echo "┗=====================┛"
	@$(CC) $(WWW) $(PATH_TEST) $(FLAGS) -o ./test_model/test_result
	./test_model/test_result

style_check:
	@echo "┏=========================================┓"
	@echo "┃  Checking your code for Google Style    ┃"
	@echo "┗=========================================┛"
	@cp ../materials/linters/.clang-format ./.clang-format
	@clang-format -i controller/*.h controller/*.cpp
	@clang-format -i view/*.h view/*.cpp
	@clang-format -i model/*.h model/*.cpp

style_change:
	@echo "┏=========================================┓"
	@echo "┃  Changing your code for Google Style    ┃"
	@echo "┗=========================================┛"
	@clang-format -n model/*.h model/*.cpp
	@clang-format -n controller/*.h controller/*.cpp
	@clang-format -n view/*.h view/*.cpp

clean:
	@rm -rf ./test_model/test_result
	@rm -rf ./test_result
	@rm -rf ./test.info
	@rm -rf .qmake.stash
	@rm -rf ./.clang-format
	@rm -rf ./*gcda
	@rm -rf ./html/
	@rm -rf Archive_SmartCalc_v2.0.tgz
	@rm -rf .clang-format
